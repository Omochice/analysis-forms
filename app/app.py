import json
import os
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from .models import analysis_form, is_allowed_file

app = Flask(__name__)
app.config["DEBUG"] = True
pwd = Path("./")    #

UPLOAD_DIR = pwd / "uploaded"
ALLOWED_EXT = {"xlsx", "xlx", "csv"}
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)

app.secret_key = os.environ["SEC_WORD"]


@app.route("/")
def root():
    return render_template("index.html", excel_files=list(pwd.glob("*.xlsx")))


@app.route("/show")
def show_all():
    analysised_groups = sorted(
        [p.stem for p in (pwd / "app" / "static" / "messages").glob("*.json")])
    return render_template("show_all.html", groups=analysised_groups)


@app.route("/show/<int:groupname>")
def show(groupname: int):
    with open(pwd / "app" / "static" / "messages" / f"{groupname}.json") as f:
        data = json.load(f)
    return render_template("analysis.html",
                           name=groupname,
                           positives=data["comments"]["positive"],
                           negatives=data["comments"]["negative"],
                           data=data["scores"],
                           n_data=[[i, i + 1]
                                   for i in range(0, len(data["scores"]), 2)])


@app.route("/upload", methods=["POST"])
def upload_file():
    if "upload_file" not in request.files:
        flash("No file part")
        return redirect(url_for("root"))
    else:
        file = request.files["upload_file"]
        n_groups = int(request.form["n_groups"])
        if file.filename == "":
            flash("No selecterd file")
            return redirect(url_for("root"))
        elif file and is_allowed_file(file.filename, ALLOWED_EXT):
            filename = secure_filename(file.filename)
            dst = UPLOAD_DIR / filename
            file.save(dst)
            analysis_form(dst, n_groups)
            return redirect(url_for("show_all"))


@app.route("/delete", methods=["POST", "DELETE"])
def delete():
    # remove files
    # rm uploaded/* app/static/img/*.png app/static/*.json
    for p in (pwd / "uploaded").glob("*"):
        if p.is_file():
            os.remove(str(p))

    # for p in (pwd / "app" / "static" / "img").glob("*.png"):
    #     if p.is_file():
    #         os.remove(str(p))

    for p in (pwd / "app" / "static" / "messages").glob("*.json"):
        if p.is_file():
            os.remove(str(p))

    return redirect(url_for("root"))


if __name__ == "__main__":
    app.run()
