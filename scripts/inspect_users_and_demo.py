import sqlite3

conn = sqlite3.connect('projectverse.db')
cur = conn.cursor()

print("--- USERS ---")
cur.execute("SELECT id, full_name, email, role FROM users WHERE email NOT LIKE '%example.test%'")
rows = cur.fetchall()
for r in rows:
    print(r)

print("\n--- ORDERS ---")
cur.execute("SELECT * FROM orders")
for r in cur.fetchall():
    print(r)

print("\n--- DEMO RECORDS TABLE COUNT ---")
cur.execute("SELECT entity_type, COUNT(*) FROM demo_records GROUP BY entity_type")
for r in cur.fetchall():
    print(r)

conn.close()
