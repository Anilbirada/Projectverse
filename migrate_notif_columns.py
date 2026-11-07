import sqlite3

conn = sqlite3.connect('projectverse.db')
cur = conn.cursor()
cols = [r[1] for r in cur.execute('PRAGMA table_info(notifications)').fetchall()]
if 'type' not in cols:
    cur.execute("ALTER TABLE notifications ADD COLUMN type TEXT DEFAULT 'general'")
    print("Added type column to notifications.")
if 'link_url' not in cols:
    cur.execute("ALTER TABLE notifications ADD COLUMN link_url TEXT DEFAULT ''")
    print("Added link_url column to notifications.")
conn.commit()
conn.close()
print("Notifications schema up to date.")
