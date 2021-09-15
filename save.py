import csv

def save_to_csv(keyword, jobs):
  file = open(f"{keyword}.csv", mode = "w")
  writer = csv.writer(file)
  writer.writerow(["link", "title", "company", "location", "salary"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return file.name
  