from flask import ( 
        Blueprint, flash, g, redirect, render_template, request, url_for)
from pdm_utils.functions import basic

from MycoIsolatesDB import alchemy
bp = Blueprint("isolate", __name__)

@bp.route("/isolates", methods=("GET", "POST"))
def isolates_index(def_size=20):
    size = request.args.get("size")
    if not size:
        size = def_size
    else:
        size = int(size)

    page = request.args.get("page")
    if not page:
        page = 1
    else:
        page = int(page)

    filters = request.args.get("filters")
    if not filters:
        filters = ""

    db_filter = alchemy.build_filter()

    db_filter.key = "clinical_isolate.IsolateID"
    db_filter.add(filters)
    db_filter.values = db_filter.build_values(
                                 where=db_filter.build_where_clauses())

    isolates = db_filter.query("clinical_isolate")
    isolates = sorted(isolates, key=alchemy.isolate_sorting)

    chunked_isolates = basic.partition_list(isolates, size) 
    page_max = len(chunked_isolates)

    if page >= page_max:
        page = page_max

    return render_template("isolate/index.html", 
                            chunked_isolates=chunked_isolates, 
                            page=page, page_max=page_max)

@bp.route("/isolates/<isolate_id>", methods=("GET",))
def isolate_page(isolate_id):
    alchemist = alchemy.alchemist
    
    isolate_map = alchemist.mapper.classes["clinical_isolate"]
    isolate = alchemist.session.query(isolate_map)\
                               .filter_by(IsolateID=isolate_id).scalar()
    
    if isolate is None:
        return render_template("entry404.html", entry_id=isolate.IsolateID)
    else:
        return render_template("isolate/isolate.html", isolate=isolate)


