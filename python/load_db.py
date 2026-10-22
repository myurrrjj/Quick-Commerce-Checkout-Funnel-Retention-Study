import os
import sqlite3
import pandas as pd

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(root, "data")
db = os.path.join(root, "qc.db")
sqldir = os.path.join(root, "sql")

if os.path.exists(db):
    os.remove(db)

con = sqlite3.connect(db)
with open(os.path.join(sqldir, "01_schema.sql")) as f:
    con.executescript(f.read())

for t in ["users", "sessions", "events", "orders"]:
    df = pd.read_csv(os.path.join(d, t + ".csv"))
    df.to_sql(t, con, if_exists="append", index=False)
con.commit()

for fn in ["02_funnel.sql", "03_segments.sql", "04_cohort_retention.sql"]:
    print("=" * 60)
    print(fn)
    print("=" * 60)
    sql = open(os.path.join(sqldir, fn)).read()
    stmts = [x.strip() for x in sql.split(";") if x.strip()]
    for st in stmts:
        try:
            out = pd.read_sql_query(st, con)
            print(out.to_string(index=False))
            print("-" * 40)
        except Exception as ex:
            print("ERR:", ex)
con.close()
