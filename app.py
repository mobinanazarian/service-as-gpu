from flask import Flask, jsonify, request

app = Flask(__name__)

class Job:
    def __init__(self, job_id, name, hours):
        self.job_id = job_id
        self.name = name
        self.hours = hours
        self.status = "PENDING"

    def run(self):
        self.status = "COMPLETED"


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


@app.route("/jobs/<int:job_id>/run", methods=["POST"])
def run_job(job_id):
    for job in jobs:
        if job.job_id == job_id:
            job.run()
            return jsonify({
                "message": "Job executed",
                "status": job.status
            })

    return jsonify({"error": "Job not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
