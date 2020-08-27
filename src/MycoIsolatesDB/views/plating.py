from collections import OrderedDict

from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for)

from MycoIsolatesDB import alchemy 

bp = Blueprint("plating", __name__)

@bp.route("/plating_assay_data", methods=("GET",))
def plating_assay_data():
    db_filter = alchemy.build_filter()
    db_filter.key = "plating.PlatingID"

    filters = request.args.get("filters")
    if filters != None:
        db_filter.add(filters)
    db_filter.values = db_filter.build_values(
                                where=db_filter.build_where_clauses())

    phages = db_filter.transpose("plating.PhageID")
    plating_data_dicts = build_plating_data_dicts(db_filter, phages)

    return render_template("plating/data.html", phages=phages, plating_data_dicts=plating_data_dicts)

def build_plating_data_dicts(db_filter, phages):
    isolates = db_filter.transpose("plating.IsolateID")

    plating_data_dicts = []
    values = db_filter.values
    for isolate in isolates:   
        db_filter.values = [isolate]
        db_filter.key = "plating.IsolateID"

        plating_data_dict = OrderedDict()
        plating_data_dict["Isolate"] = isolate
       
        plating_data = db_filter.select(["plating.EOP", "plating.PhageID"])
        for data_dict in plating_data:
            plating_data_dict[data_dict["PhageID"]] = data_dict["EOP"]

        for phage in phages:
            plating_EOP = plating_data_dict.get(phage, "")
            plating_data_dict[phage] = plating_EOP

        plating_data_dicts.append(plating_data_dict)

    return plating_data_dicts

#@bp.route("/EOP_Assays/<plating_id>")
def plating_assay_page(plating_id):
    alchemist = alchemy.build_dud_alchemist()

    plating_map = alchemist.mapper.classes["plating"]
    plating = alchemist.session.query(plating_map).filter_by(PlatingID=plating_id).scalar()

    if isolate is None:
        return render_template("/")
    else:
        return render_template("EOPs.EOP_page", plating=plating)

    
