#!/usr/bin/python3
from flask import Flask, request, render_template
import string
import subprocess
import re


app = Flask(__name__)


def filter(formula):
    w_list = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    w_list.extend([" ", ".", "(", ")", "+"])

    if re.search("(system)|(curl)|(flag)|(subprocess)|(popen)", formula, re.I):
        return True
    for c in formula:
        if c not in w_list:
            return True


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        formula = request.form.get("formula", "")
        if formula != "":
            if filter(formula):
                return render_template("index.html", result="Filtered")
            else:
                try:
                    formula = eval(formula)
                    return render_template("index.html", result=formula)
                except subprocess.CalledProcessError:
                    return render_template("index.html", result="Error")
                except:
                    return render_template("index.html", result="Error")
        else:
            return render_template("index.html", result="Enter the value")


app.run(host="0.0.0.0", port=8000)
