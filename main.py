class Job:
    def init(self, name, hours):
        self.name = name
        self.hours = hours
        self.status = "PENDING"

    def run(self):
        self.status = "COMPLETED"


job1 = Job("test-job", 2)
print(job1.name)
print(job1.status)

job1.run()
print(job1.status)
