from flask import Flask, render_template, request, redirect, send_file
import hh
import save

#hh_jobs = hh.get_jobs()
#so_jobs = stackoverflow.get_jobs()

#jobs = hh_jobs + so_jobs

#save.save_to_csv(jobs)

app = Flask("JobScrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  keyword = request.args.get("keyword")
  if keyword is not None:
    keyword = keyword.lower()
    dump = db.get(keyword)
    if dump:
      jobs = dump
    else:
      jobs = hh.get_jobs(keyword)
      db[keyword] = jobs
    print(jobs)
  else:
    return redirect("/")
  return render_template("report.html", keyword=keyword, jobs = jobs)

@app.route("/export")
def export():
  try:
    keyword = request.args.get("keyword")
    if not keyword:
      raise Exception()
    keyword = keyword.lower()
    jobs = db.get(keyword)
    if not jobs:
      raise Exception()
    filename = save.save_to_csv(keyword, jobs)
    return send_file(filename)
  except:
    redirect("/")

app.run(host = '0.0.0.0')