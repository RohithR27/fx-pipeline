import csv
import io
import sqlite3

# ---------- EXTRACT ----------
raw = """currency,rate,date
eur,0.92,2026-11-17
GBP,0.79,2026-11-17
JPY,,2026-11-17
 cad ,1.36,2026-11-17
EUR,abc,2026-11-17
"""

rows = list(csv.DictReader(io.StringIO(raw)))
print("Rows read:", len(rows))


# ---------- TRANSFORM ----------
def clean_row(row):
    currency = row["currency"].strip().upper()
    try:
        rate = float(row["rate"])
    except ValueError:
        return None
    return {"currency": currency, "rate": rate, "date": row["date"]}


clean = []
rejected = 0

for row in rows:
    result = clean_row(row)
    if result is None:
        rejected += 1
    else:
        clean.append(result)

print("Clean rows:", len(clean))
print("Rejected rows:", rejected)
# clean.append({"currency": "EUR", "rate": 0.92, "date": "2026-11-17"})

# ---------- LOAD ----------
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE rates (currency TEXT, rate REAL, date TEXT)")
conn.executemany("INSERT INTO rates VALUES (:currency, :rate, :date)", clean)
conn.commit()

print(conn.execute("SELECT COUNT(*) FROM rates").fetchall())
print(conn.execute("SELECT currency, rate FROM rates WHERE rate > 1").fetchall())

# TODO (your turn): add a query for AVG(rate)
print(conn.execute("SELECT ROUND(AVG(rate),2) FROM rates").fetchall())

# duplicates
# clean.append({"currency": "EUR", "rate": 0.92, "date": "2026-11-17"})
print(conn.execute(
    """
    SELECT currency, COUNT(*) FROM rates
    GROUP BY currency
    HAVING COUNT(*) > 1
    """).fetchall())

# # Why do we insert only the clean rows, not the raw ones?
# clean rows will have the correct column_name and data, whereas if we insert raw ones might have null and incorrect datatype error.
# # What does commit() do?
# commit - save the changes done till that process in sqlite3