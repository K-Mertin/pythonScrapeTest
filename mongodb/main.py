import DataAccess as da


db = da.get_db()
da.add_country(db)
print(da.get_country(db))
