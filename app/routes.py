from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os

from app.models import neo4j
from app.utils import (
    import_file,
    get_graph_data,
    process_merge_operation,
    process_delete_operation,
)

main_blueprint = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"csv", "json", "rdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@main_blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@main_blueprint.route("/import/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit(".", 1)[1].lower()
            import_result = import_file(file, file_extension)
            return jsonify(import_result)
    return render_template("import/upload.html")


@main_blueprint.route("/import/result", methods=["GET"])
def import_result():
    result_data = request.args.get("result")
    if result_data:
        result = jsonify(result_data)
    else:
        result = None
    return render_template("import/result.html", result=result)


@main_blueprint.route("/graph/operations", methods=["GET", "POST"])
def graph_operations():
    if request.method == "POST":
        operation_type = request.form.get("operation-type")
        if operation_type == "merge":
            label = request.form.get("label")
            properties = request.form.get("properties")
            data = process_merge_operation(label, properties)
            return jsonify(data)
        elif operation_type == "delete":
            label = request.form.get("label")
            properties = request.form.get("properties")
            data = process_delete_operation(label, properties)
            return jsonify(data)
        elif operation_type == "query":
            query = request.form.get("query")
            data = get_graph_data(query)
            return jsonify(data)
    return render_template("graph/operations.html")


@main_blueprint.route("/graph/result", methods=["GET"])
def graph_result():
    result_data = request.args.get("result")
    if result_data:
        result = jsonify(result_data)
    else:
        result = None
    return render_template("graph/result.html", result=result)
