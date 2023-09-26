from flask import Flask, jsonify, render_template, request

from database import add_application_to_db, load_job_from_db, load_jobs_from_db

app= Flask(__name__)

@app.route("/")
def web_site_training():
    jobs=load_jobs_from_db()
    return render_template("home.html",jobs=jobs)

@app.route("/api/jobs")
def list_jobs():
  jobs=load_jobs_from_db()
  return jsonify(jobs)

@app.route("/job/<id>")
def show_job(id):
  job=load_job_from_db(id)
  if not job:
    return "Not found", 404
  return render_template("jobpage.html",job=job)


@app.route("/job/<id>/apply", methods=['post']) ##post is to avoid passing the arguments in the url due to this it also requires
##request.form to display the info in the post
def apply_to_job(id):
  #store in the db
  #send an email
  #acknewlodgement page
  application_data=request.form 
  job=load_job_from_db(id)
  add_application_to_db(id,application_data)
  return render_template('application_submitted.html',application=application_data, job=job)
  


if __name__=="__main__":
  app.run(host='0.0.0.0', debug=True, port=81)
  
