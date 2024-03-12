import sqlite3
from flask import json

def search_aadhaar(uid_value):
    conn = sqlite3.connect('aadhaar.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM details WHERE uid=?", (uid_value,))
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
                    "loc": result[5],
                    "pc": result[6],
                    "yob": result[7],
                    "state": result[8],
                    "dist": result[9]
                        }
            json.dump(data, json_file, indent=4, separators=(',', ': '))
            json_file.write('\n')
        return True
    else:
        return False
