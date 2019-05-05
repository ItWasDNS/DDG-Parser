"""
    Process 'com.duckduckgo.mobile.android/databases/app.db'
"""

import os
import sqlite3
from modules.helpers.ddg_path_handler import process_directory_paths

query_app_usage = "SELECT date FROM app_days_used;"
query_app_bookmarks = "SELECT id, title, url FROM bookmarks;"
query_app_sites = "SELECT domain FROM site_visited;"
query_app_tabs = """
SELECT 
  tabs.url,
  tabs.title,
  tabs.viewed,
  tabs.position,
  tab_selection.id
FROM tabs
  LEFT JOIN tab_selection
    ON tabs.tabId = tab_selection.tabId;
"""
bookmarks_template = """--
Title: %s
URL: %s
"""
tabs_template = """--
URL: %s
URL Viewed: %s
Current Tab: %s
"""


def process_db_app(duckduckgo_path, output_path):
    """ Process DDG 'app.db' database """
    # Query Database
    path = duckduckgo_path + 'databases/app.db'
    with open(os.path.join(output_path, 'db_app_output.txt'), 'w') as o:
        o.write("Processed: 'com.duckduckgo.mobile.android/databases/app.db'\n")
        try:
            conn = sqlite3.connect(path)
            answer_usage = conn.execute(query_app_usage).fetchall()
            answer_bookmarks = conn.execute(query_app_bookmarks).fetchall()
            answer_leaderboard = conn.execute(query_app_sites).fetchall()
            answer_tabs = conn.execute(query_app_tabs).fetchall()
            conn.close()
        except sqlite3.OperationalError as e:
            o.write("Error: %s" % str(e))
            return None
        # Display Results
        o.write("#========================================#\n")
        o.write("DuckDuckGo Days Used:\n")
        if len(answer_usage) == 0:
            o.write("None\n")
        for result in answer_usage:
            # Days Used is relative to UTC
            o.write("%s\n" % result[0])
        o.write("#========================================#\n")
        o.write("DuckDuckGo Bookmarks:\n")
        if len(answer_bookmarks) == 0:
            o.write("None\n")
        for result in answer_bookmarks:
            o.write(bookmarks_template % (result[1], result[2]))
        o.write("#========================================#\n")
        o.write("DuckDuckGo Tabs:\n")
        if len(answer_tabs) == 0:
            o.write("None\n")
        # Fix Handling
        elif len(answer_tabs) >= 1:
            for result in answer_tabs:
                o.write(tabs_template % (result[0],
                                         "Yes" if result[2] == 1 else "No",
                                         "Yes" if result[4] == 1 else "No"))
        else:
            o.write("None\n")
        o.write("#========================================#\n")
        o.write("DuckDuckGo Sites Visited:\n")
        if len(answer_leaderboard) == 0:
            o.write("None\n")
        for result in answer_leaderboard:
            o.write("%s\n" % result[0])
        o.write("#========================================#\n")


if __name__ == '__main__':
    # Set DDG application data path for testing
    ddg_path, out_path = process_directory_paths()
    # Process artifacts
    process_db_app(ddg_path, out_path)
