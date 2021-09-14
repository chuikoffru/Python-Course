import hh
import stackoverflow

hh_jobs = hh.get_jobs()
so_jobs = stackoverflow.get_jobs()

jobs = hh_jobs + so_jobs

print(jobs)