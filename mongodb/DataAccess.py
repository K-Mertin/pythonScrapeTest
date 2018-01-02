import pymongo

def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.testDB

    return db

def add_country(db):
    return db.countries.insert({"name":"taiwan"})

def get_country(db):
    return db.countries.find_one()

if __name__ == "__main__":
    db = get_db()
    add_country(db)
    print(get_country(db))

