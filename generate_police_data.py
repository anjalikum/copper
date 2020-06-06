from google.cloud import datastore
import math

client = datastore.Client()

file = open("/tmp/police-data/27681-0001-Data.txt", "r")
lines = [l.strip() for l in file.readlines()]

departments = [{
    "name": line[432:504].strip(),
    "city": line[618:644].strip(),
    "state": line[668:688].strip(),
    "zip": line[646:668].strip(),
    "county": line[688:713].strip()
} for line in lines if int(line[8:12].strip()) <= 5]

for i in range(math.ceil(len(departments) / 500)):
    entities = []

    for d in range(i*500, i*500 + 500):
        try:
            department = departments[d]
        except IndexError:
            break

        key = client.key("Department")
        entity = datastore.Entity(key)
        entity.update(department)

        entities.append(entity)

    client.put_multi(entities)
    print(len(entities))
