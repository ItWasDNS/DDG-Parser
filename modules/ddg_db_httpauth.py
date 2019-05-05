"""
    Process 'com.duckduckgo.mobile.android/databases/http_auth.db'
"""

import os
import sqlite3
from modules.helpers.ddg_path_handler import process_directory_paths

query_httpauth = """
SELECT 
  host,
  realm,
  username,
  password
FROM httpauth;
"""
httpauth_template = """--
Host: %s
Realm: %s
Username: %s
Password: %s
"""


def process_db_httpauth(duckduckgo_path, output_path):
    """ Process DDG 'http_auth.db' database """
    path = duckduckgo_path + 'databases/http_auth.db'
    with open(os.path.join(output_path, 'db_httpauth_output.txt'), 'w') as o:
        o.write("Processed: 'com.duckduckgo.mobile.android/databases/http_auth.db'\n")
        try:
            conn = sqlite3.connect(path)
            answer = conn.execute(query_httpauth).fetchall()
            conn.close()
        except sqlite3.OperationalError as e:
            o.write("Error: %s" % str(e))
            return None
        if len(answer) == 0:
            o.write("None")
        else:
            for result in answer:
                o.write(httpauth_template % result)


if __name__ == '__main__':
    # Set DDG application data path for testing
    ddg_path, out_path = process_directory_paths()
    # Process artifacts
    process_db_httpauth(ddg_path, out_path)
