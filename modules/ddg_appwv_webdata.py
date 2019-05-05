"""
    Process 'com.duckduckgo.mobile.android/app_webview/Web Data'
"""

import os
import time
import sqlite3
from modules.helpers.ddg_path_handler import process_directory_paths

query_autofill = """
SELECT 
  name,
  value,
  date_created,
  date_last_used,
  count
FROM autofill;
"""
autofill_template = """--
Name: %s
Value: %s
Date Created: %s
Date Last Used: %s
Count: %s
"""


def process_appwv_webdata(duckduckgo_path, output_path):
    """ Process DDG 'Web Data' database """
    path = duckduckgo_path + 'app_webview/Web Data'
    with open(os.path.join(output_path, 'appwv_webdata_output.txt'), 'w') as o:
        o.write("Processed: 'com.duckduckgo.mobile.android/app_webview/Web Data'\n")
        try:
            conn = sqlite3.connect(path)
            answer = conn.execute(query_autofill).fetchall()
            conn.close()
        except sqlite3.OperationalError as e:
            o.write("Error: %s" % str(e))
            return None
        if len(answer) == 0:
            o.write("None")
        else:
            for result in answer:
                o.write(autofill_template % (result[0], result[1],
                                             time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result[2])),
                                             time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result[3])),
                                             result[4]))


if __name__ == '__main__':
    # Set DDG application data path for testing
    ddg_path, out_path = process_directory_paths()
    # Process artifacts
    process_appwv_webdata(ddg_path, out_path)
