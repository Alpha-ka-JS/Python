from flask import Flask, render_template, request, redirect, send_file
from stackoverflow import get_jobs as get_stackoverflow_jobs
from remoteok import get_jobs as get_remoteok_jobs
from wework import get_jobs as get_wework_jobs

from exporter import save_to_file

"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

app = Flask("Day Thirteen and Fourteen")
db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    jobs = []
    try:
        term = request.args.get("term")
        if not term:
            raise Exception()
        term = term.lower()
    except:
        return redirect("/")

    jobs = db.get(term)
    if not jobs:
        jobs = get_stackoverflow_jobs(term)
        jobs += get_wework_jobs(term)
        jobs = get_remoteok_jobs(term)
        db[term] = jobs
    else:
        print("Data already exist")

    return render_template("search.html", jobs=jobs, job_length=len(jobs), term=term)


@app.route("/export")
def export():
    try:
        term = request.args.get("term")
        if not term:
            raise Exception()
        term = term.lower()
        jobs = db.get(term)
        if not jobs:
            raise Exception()
        save_to_file(jobs, term)
        return send_file(f"./{term}.csv", as_attachment=True)
    except:
        return redirect("/")


# app.run(host="0.0.0.0")
app.run()
