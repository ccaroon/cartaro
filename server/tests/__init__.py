import os

# Delete all DB files
db_dir = "tests/tmp"
for file in os.listdir(db_dir):
    if file.endswith(".json"):
        os.remove(F"{db_dir}/{file}")
