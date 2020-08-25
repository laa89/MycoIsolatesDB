from collections import OrderedDict

from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for)

from MycoIsolatesDB import alchemy

bp = Blueprint("induction", __name__)

@bp.route("/induction")
def induction_index(filters=""):
    db_filter = alchemy.build_filter()
    db_filter.key = "induction.InductionID"

    if filters != "":
        db_filter.add(filters)
    db_filter.values = db_filter.build_values(
                                    where=db_filter.build_where_clauses())

    victims = db_filter.transpose("induction.Victim")
    induction_data_dicts = build_induction_data_dicts(db_filter, victims)

    return render_template("induction/data.html", victims=victims, 
                           induction_data_dicts=induction_data_dicts)

def build_induction_data_dicts(db_filter, victims):
    surrogates = db_filter.transpose("induction.Surrogate")

    induction_data_dicts = []
    for isolate in surrogates:
        db_filter.values = [isolate]
        db_filter.key = "induction.Surrogate"

        induction_data_dict = OrderedDict()
        induction_data_dict["Surrogate"] = isolate

        induction_data = db_filter.select(["induction.Infects", "induction.Victim"])
        for data_dict in induction_data:
            induction_data_dict[data_dict["Victim"]] = data_dict["Infects"] 

        for victim in victims:
            infects = induction_data_dict.get(victim, "")
            induction_data_dict[victim] = infects

        induction_data_dicts.append(induction_data_dict)
    
    return induction_data_dicts

