import csv


def save_to_file(jobs, term):
    file = open(f"{term}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "link"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return
