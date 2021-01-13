from flask import Flask, render_template, request, session, url_for, redirect
import json
from pathlib import Path
from .models import analysis, analysis_form

app = Flask(__name__)
app.config["DEBUG"] = True
pwd = Path("./") # 


@app.route("/")
def root():
    return render_template("index.html", excel_files=list(pwd.glob("*.xlsx")))

@app.route("/post", methods=["POST"])
def post():
    name = request.form["file"]
    n_groups = request.form["n_groups"]
    analysis_form(pwd.resolve()/name, int(n_groups))
    return redirect(url_for("show_all"))
    # return render_template("index.html")

@app.route("/show")
def show_all():
    analysised_groups = sorted([p.stem for p in  (pwd/ "app" / "static" /"messages").glob("*.json")])
    return render_template("show_all.html", groups=analysised_groups)


@app.route("/show/<int:groupname>")
def show(groupname: int):
    with open(pwd/"app"/"static"/ "messages" / f"{groupname}.json") as f:
        data = json.load(f)
    return render_template("analysis.html", name=groupname, imgnames=data["images"], messages=data["messages"])



if __name__ == "__main__":
    app.run(debug=True)
