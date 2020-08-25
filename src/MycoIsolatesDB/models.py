from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import

db = SQLAlchemy()

# Models    
class IsolateStage(db.Model):
    stage = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Binary)

class Contact(db.Model):
    contact_id = db.Column(db.String(25), primary_key=True)
    name = db.Column(db.String(45))
    email = db.Column(db.String(65))
    institution = db.Column(db.String(65))
    location = db.Column(db.String(65))

class Phage(db.Model):
    phage_id = db.Column(db.String(35), primary_key=True)
    accession = db.Column(db.String(15))
    cluster = db.Column(db.String(5))
    subcluster = db.Column(db.String(5))

class ClinicalIsolate(db.Model):
    isolate_id = db.Column(db.String(35), primary_key=True)
    strain = db.Column(db.String(35))
    species = db.Column(db.String(35))
    subspecies = db.Column(db.String(35))
    genus = db.Column(db.String(35))
    morphotype = db.Column(db.String(15))

    stage = db.Column(db.Integer)
    wgs = db.Column(db.Boolean)
    nanopore = db.Column(db.Boolean)
    unicyler = db.Column(db.Boolean)
    complete = db.Column(db.Boolean)
    barcode = db.Column(db.String(45))

    parent_id = db.Column(db.String(35), 
                          db.ForeignKey("clinicalisolate.isolate_id"))

    mutant = db.relationship("ClinicalIsolate", backref="Parent", lazy=True)
    antibiotic_assays = db.relationship("Antibiotic", backref="ClinicalIsolate",
                                        lazy=True)

class ClinicalIsolateContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.String(25), nullable=False)
    isolate_id = db.Column(db.String(35), 
                           db.ForeignKey("clinicalisolate.isolate_id"),
                           nullable=False) 

class Replicon(db.Model):
    replicon_id = db.Column(db.String(35), primary_key=True) 
    length = db.Column(db.BigInteger)
    sequence = db.Column(db.LargeBinary)
    gc = db.Column(db.Float)
    notes = db.Column(db.Binary)

    isolate_id = db.Column(db.String(35), 
                           db.ForeignKey("clinicalisolate.isolate_id"),
                           nullable=False)

class Gene(db.Model):
    gene_id = db.Column(db.String(35), primary_key=True)
    locus_tag = db.Column(db.String(35))
    length = db.Column(db.Integer)
    translation = db.Column(db.LargeBinary)
    start = db.Column(db.Integer)
    stop = db.Column(db.Integer)
    orientation = db.Column(db.String(1))
    Notes = db.Column(db.Binary)
    
    replicon_id = db.Column(db.String(35), 
                            db.ForeignKey("replicon.replicon_id"), 
                            nullable=False)

class PhageCocktail(db.Model):
    cocktail_id = db.Column(db.Integer, primary_key=True)
    endotoxin = db.Column(db.Boolean)
    accugen = db.Column(db.Boolean)
    sent = db.Column(db.Boolean)

    isolate_id = db.Column(db.String(35),
                           db.ForeignKey("clinicalisolate.isolateid"),
                           nullable=False)

class CocktailContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phage_id = db.Column(db.String(35), db.ForeignKey("phage.phage_id"),
                         nullable=False)
    cocktail_id = db.Column(db.String(35), 
                            db.ForeignKey("phagecocktail.cocktail_id"),
                            nullable=False)

class Induction(db.Model):
    induction_id = db.Column(db.String(35), primary_key=True)
    surrogate = db.Column(db.String(35), 
                          db.ForeignKey("clinicalisolate.isolate_id"),
                          nullable=False) 
    victim = db.Column(db.String(35), 
                       db.ForeignKey("clinicalisolate.isolate_id"),
                       nullable=False)
    infects = db.Column(db.Boolean)

class Plating(db.Model):
    plating_id = db.Column(db.String(35), primary_key=True)
    eop = db.Column(db.Float)
    infects = db.Column(db.Boolean) 
    turbid = db.Column(db.Boolean)

    isolate_id = db.Column(db.String(35), 
                           db.ForeignKey("clinicalisolate.isolate_id"),
                           nullable=False)
    phage_id = db.Column(db.String(35),
                         db.ForeignKey("phage.phage_id"),
                         nullable=False)
    relhost = db.Column(db.String(35),
                        db.ForeignKey("clinicalisolate.isolate_id"))

class Antibiotic(db.Model):
    antibiotic_id = db.Column(db.String(35), primary_key=True)
    efficacy = db.Column(db.String(1))
    name = db.Column(db.String(25))
    MIC = db.Column(db.String(5))

    isolate_id = db.Column(db.String(35), 
                           db.ForeignKey("clinicalisolate.isolate_id"), 
                           nullable=False)

class Prophage(db.Model):
    prophage_id = db.Column(db.String(35), primary_key=True)
    replicon_id = db.Column(db.String(35), 
                            db.ForeignKey("replicon.replicon_id"),
                            nullable=False)
    phage_id = db.Column(db.String(35),
                         db.ForeignKey("phage.phage_id"),
                         nullable=False)

class ProphageInduction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prophage_id = db.Column(db.String(35),
                            db.ForeignKey("prophage.prophage_id"),
                            nullable=False)
    induction_id = db.Column(db.String(35),
                            db.ForeignKey("induction.induction_id"))


class SurvivalAssay(db.Model):
    assay_id = db.Column(db.String(35), primary_key=True)
    day2 = db.Column(db.String(5))
    day5 = db.Column(db.String(5))

    isolate_id = db.Column(db.String(35), 
                           db.ForeignKey("clinicalisolate.isolate_id"),
                           nullable=False)

class SurvivalAssayPhage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assay_id = db.Column(db.String(35),
                         db.ForeignKey("survivalassay.assay_id"),
                         nullable=False)
    phage_id = db.Column(db.String(35),
                         db.ForeignKey("phage.phage_id"),
                         nullable=False)


