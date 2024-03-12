import sqlite3
from flask import json

def search_voter(uid_value):
    conn = sqlite3.connect('voters.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM list WHERE uid=?", (uid_value,))
    result = cursor.fetchone()
    conn.close()
    if result:
        with open(f"{uid_value}.json", 'w') as json_file:
            data = {
                "uid": result[0],
                "name": result[1],
                "gender": result[2],
                "co": result[3],
                "house": result[4],
                "yob": result[5]
            }
            json.dump(data, json_file, indent=4, separators=(',', ': '))
            json_file.write('\n')
        return True
    else:
        return False
