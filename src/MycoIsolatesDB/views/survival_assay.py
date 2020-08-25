from collections import OrderedDict

from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for)

from MycoIsolatesDB import alchemy

bp = Blueprint("survival_assay", __name__)

@bp.route("/survival_assays", methods=("GET",))
def survival_assays_index(filters=""):
    filters = request.args.get("filters")
    if not filters:
        filters = ""

    day = request.args.get("day")
    if not day:
        day = 2
    else:
        day = int(day)

    db_filter = alchemy.build_filter()
    db_filter.key = "survival_assay.AssayID"

    if filters != "":
        db_filter.add(filters)
    db_filter.values = db_filter.build_values(
                                where=db_filter.build_where_clauses()) 

    phages_assay_map = get_distinct_phage_groups(db_filter)
    phages = list(phages_assay_map.keys())

    survival_data_dicts = build_survival_data_dicts(db_filter, phages_assay_map, 
                                                    day)

    return render_template("survival_assay/data.html", phages=phages,
                            survival_data_dicts=survival_data_dicts)

def get_distinct_phage_groups(db_filter):
    phage_data = db_filter.retrieve("survival_assay_phage.PhageID")

    phages_assay_map = OrderedDict()
    for assay, data_dict in phage_data.items():
        phages = data_dict["PhageID"]
        phages = "+".join(phages)

        assay_list = phages_assay_map.get(phages, [])
        assay_list.append(assay)
        phages_assay_map[phages] = assay_list

    return phages_assay_map

def build_survival_data_dicts(db_filter, phages_assay_map, day):
    isolate_data = db_filter.retrieve(["survival_assay.IsolateID", f"survival_assay.Day{day}"])

    isolate_assay_phages_map = OrderedDict()
    for phages, assay_list in phages_assay_map.items():
        for assay in assay_list:
            isolate = isolate_data[assay]["IsolateID"][0] 
            result = isolate_data[assay][f"Day{day}"][0]

            isolate_dict = isolate_assay_phages_map.get(isolate, {}) 
            isolate_dict[phages] = result

            isolate_assay_phages_map[isolate] = isolate_dict

    survival_data_dicts = []
    for isolate, phages_data in isolate_assay_phages_map.items():
        data_dict = {}

        data_dict["isolate"] = isolate
        for phages, result in phages_data.items():
            data_dict[phages] = result

        survival_data_dicts.append(data_dict)

    return survival_data_dicts
