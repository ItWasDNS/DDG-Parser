"""
    Process 'com.duckduckgo.mobile.android/app_webview/Cookies'
"""

import os
import sqlite3
from modules.helpers.ddg_path_handler import process_directory_paths

query_cookies = """
SELECT
  host_key,
  path,
  name,
  value,
  creation_utc,
  last_access_utc,
  expires_utc,
  secure,
  httponly,
  persistent,
  encrypted_value
FROM cookies;
"""
cookies_template = """--
Host: %s
Path: %s
Cookie Name: %s
Cookie Value: %s
Cookie Creation: %s
Cookie Expiration: %s
"""


def process_appwv_cookies(duckduckgo_path, output_path):
    """ Process DDG 'Cookies' database """
    with open(os.path.join(output_path, 'appwv_cookies_output.txt'), 'w') as o:
        o.write("Processed: 'com.duckduckgo.mobile.android/app_webview/Cookies'\n")
        try:
            conn = sqlite3.connect(duckduckgo_path + 'app_webview/Cookies')
            answer = conn.execute(query_cookies).fetchall()
            conn.close()
        except sqlite3.OperationalError as e:
            o.write("Error: %s" % str(e))
            return None
        if len(answer) == 0:
            o.write("No Cookies Found in app_webview/Cookies")
            return None
        for result in answer:
            o.write(cookies_template % (result[0], result[1], result[2], result[3], result[4],  result[5]))


if __name__ == '__main__':
    # Set DDG application data path for testing
    ddg_path, out_path = process_directory_paths()
    # Process artifacts
    process_appwv_cookies(ddg_path, out_path)
