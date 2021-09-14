import csv

def save_to_csv(jobs):
  file = open("db.csv", mode = "w")
  writer = csv.writer(file)
  writer.writerow(["link", "title", "company", "location", "salary"])
  for job in jobs:
    writer.writerow(list(job.values()))
  