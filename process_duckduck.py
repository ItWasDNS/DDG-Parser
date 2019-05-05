"""
    Maintainer: Matthew Sprengel
    Tested: Python 3.7
    Description: Parse DuckDuckGo Application Data on Android Devices
    Tested Versions Information:
     - Nox Player 6.2.8.0015
     - Android Version 5.1.1 (SM-G955N)
     - DuckDuckGo 5.21.2 mk (52102)
    Future Research:
     - Extract Additional Content from app_webview/Cache
"""

from modules.ddg_appwv_cache import process_appwv_cache
from modules.ddg_appwv_cookies import process_appwv_cookies
from modules.ddg_appwv_webdata import process_appwv_webdata
from modules.ddg_cache import process_cache
from modules.ddg_db_app import process_db_app
from modules.ddg_db_httpauth import process_db_httpauth
from modules.ddg_shared_prefs import process_sharedprefs

if __name__ == '__main__':
    # Prompt user for DuckDuckGo application data directory
    # Directory does not need to be com.duckduckgo.mobile.android
    # Directory should contain DDG app data
    from modules.helpers.ddg_path_handler import process_directory_paths_core
    ddg_path, output_path = process_directory_paths_core()

    # Process Application Data
    print("Processing: 'com.duckduckgo.mobile.android/shared_prefs/*.xml'")
    process_sharedprefs(ddg_path, output_path)
    print("Processing: 'com.duckduckgo.mobile.android/databases/app.db'")
    process_db_app(ddg_path, output_path)
    print("Processing: 'com.duckduckgo.mobile.android/databases/http_auth.db'")
    process_db_httpauth(ddg_path, output_path)
    print("Processing: 'com.duckduckgo.mobile.android/app_webview/Cookies'")
    process_appwv_cookies(ddg_path, output_path)
    print("Processing: 'com.duckduckgo.mobile.android/app_webview/Web Data'")
    process_appwv_webdata(ddg_path, output_path)
    print("Processing: 'com.duckduckgo.mobile.android/app_webview/Cache/*'")
    process_appwv_cache(ddg_path, output_path)
    print("Processing: 'com.duckduckgo.mobile.android/cache/*'")
    process_cache(ddg_path, output_path)

    # Processing Complete
    print("DuckDuckGo Processing Completed")
