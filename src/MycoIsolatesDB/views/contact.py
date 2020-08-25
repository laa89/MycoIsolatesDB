from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for)
from pdm_utils.functions import basic

from MycoIsolatesDB import alchemy

bp = Blueprint("contact", __name__)

@bp.route("/contacts", methods=("GET", "POST"))
def contacts_index(def_size=20):
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

    db_filter.key = "contact.ContactID"
    db_filter.add(filters)
    db_filter.values = db_filter.build_values(
                                 where=db_filter.build_where_clauses())

    contacts = db_filter.query("contact")
    contacts = sorted(contacts, key=lambda contact: contact.Name)

    chunked_contacts = basic.partition_list(contacts, size) 
    page_max = len(chunked_contacts)

    if page >= page_max:
        page = page_max

    return render_template("contact/index.html", 
                           chunked_contacts=chunked_contacts, 
                           page=page, page_max=page_max)

