import hh
import stackoverflow
import save

hh_jobs = hh.get_jobs()
so_jobs = stackoverflow.get_jobs()

jobs = hh_jobs + so_jobs

save.save_to_csv(jobs)