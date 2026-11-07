import urllib.request
import json
import sqlite3

def run_test():
    # 1. Fetch with demo ON
    res = json.loads(urllib.request.urlopen('http://localhost:8000/api/stats').read().decode())
    print("Demo ON:", res["stats_badge"], "| Total Students:", res["total_students"], "| Demo Mode:", res["demo_mode"])

    # 2. Toggle to demo OFF
    c = sqlite3.connect('projectverse.db')
    c.execute("UPDATE admin_settings SET setting_value = '0' WHERE setting_key = 'demo_mode'")
    c.commit()
    c.close()

    res2 = json.loads(urllib.request.urlopen('http://localhost:8000/api/stats').read().decode())
    print("Demo OFF:", res2["stats_badge"], "| Total Students:", res2["total_students"], "| Demo Mode:", res2["demo_mode"])

    # 3. Restore demo ON
    c = sqlite3.connect('projectverse.db')
    c.execute("UPDATE admin_settings SET setting_value = '1' WHERE setting_key = 'demo_mode'")
    c.commit()
    c.close()
    print("Restored demo_mode = 1")

if __name__ == '__main__':
    run_test()
