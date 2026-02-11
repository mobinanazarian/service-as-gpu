from flask import Flask, jsonify, request

app = Flask(name)


class Job:
    def init(self, job_id, name, hours):
        self.job_id = job_id
        self.name = name
        self.hours = hours
        self.status = "PENDING"  

    def approve(self):
        self.status = "APPROVED"

    def run(self):
        if self.status != "APPROVED":
            return False
        self.status = "RUNNING"
        
        self.status = "COMPLETED"
        return True



jobs = []
job_counter = 1


@app.route("/")
def home():
    return "Service as GPU - Simulation"



@app.route("/jobs", methods=["POST"])
def create_job():
    global job_counter
    data = request.json

    job = Job(
        job_counter,
        data.get("name"),
        data.get("hours")
    )

    jobs.append(job)
    job_counter += 1

    return jsonify({
        "message": "Job created",
        "job_id": job.job_id,
        "status": job.status
    })



@app.route("/jobs", methods=["GET"])
def list_jobs():
    return jsonify([
        {
            "job_id": job.job_id,
            "name": job.name,
            "hours": job.hours,
            "status": job.status
        }
        for job in jobs
    ])



@app.route("/jobs/<int:job_id>/approve", methods=["POST"])
def approve_job(job_id):
    for job in jobs:
        if job.job_id == job_id:
            if job.status != "PENDING":
                return jsonify({"error": "Job already approved or executed"}), 400
            job.approve()
            return jsonify({
                "message": "Job approved",
                "status": job.status
            })
    return jsonify({"error": "Job not found"}), 404



@app.route("/jobs/<int:job_id>/run", methods=["POST"])
def run_job(job_id):
    for job in jobs:
        if job.job_id == job_id:
            result = job.run()
            if not result:
                return jsonify({"error": "Job not approved"}), 400

            return jsonify({
                "message": "Job executed",
                "status": job.status
            })

    return jsonify({"error": "Job not found"}), 404


if name == "main":
    app.run(debug=True)

