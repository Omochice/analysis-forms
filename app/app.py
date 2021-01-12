from flask import Flask, render_template, request
from pathlib import Path
from .models import analysis_form
app = Flask(__name__)


@app.route("/")
def root():
    pwd = Path("./")
    print(pwd.resolve())
    return render_template("index.html", excel_files=list(pwd.glob("*.xlsx")))

@app.route("/index", methods=["POST"])
def index():
    name = request.form["name"]
    print(request.form)
    # 引数のxlsxファイルを分析する

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
