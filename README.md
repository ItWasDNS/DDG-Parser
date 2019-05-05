# <u>Examining DuckDuckGo on Android</u>
## A Mobile Forensics Perspective

### <u>Overview</u>
When people use the DuckDuckGo mobile app, they generally associate it with enhanced privacy while browsing the Internet.
With the easily accessible flame icon that allows users to "Clear All Tabs and Data", users may inherently believe their
browsing history is wiped the moment they see the flame animation clear their currently open tabs and history. From a
forensics perspective, we should be asking: How well does DuckDuckGo clear user data which could be useful in a mobile
forensics investigation?

By examining the DuckDuckGo application and its underlying storage on an emulated Android device, we can determine that
DuckDuckGo can still provide a variety of useful forensic artifacts to an examiner. In balancing user experience with
privacy, forensic examiners can recover artifacts such as application information, bookmarks, and residual user data even
after being "cleared" by the user.

To reach this determination, we can use the Nox Player Android emulator and a variety of tools to explore how
DuckDuckGo stores, persists, and clears user data. Special thanks to Jessica Hyde (@B1N2H3X) for her guidance and
advice over the course of this project and to Alexis Brignoni (@AlexisBrignoni) for his article on Android emulation[1]
which was the foundation used for testing DuckDuckGo on an emulated Android device.

### <u>Tools Utilized</u>
 - Nox Player (Version 6.2.8.0015)
 - Android (Version 5.1.1 - SM-G950N)
 - DuckDuckGo (Version 5.21.2 mk - 52102)
 - Android Debug Bridge (Version 1.0.36)
 - Notepad++ (Version 7.6.6)
 - HxD Hex Editor (Version 2.2.1.0)
 - DB Browser for SQLite (Version 3.11.2)
 - Windows PowerShell (Version 5.1.17134.590)

### <u>Testing Methodology</u>
In order to provide a more holistic picture of what data can be recovered from DuckDuckGo, we will periodically retrieve
the underlying storage under different conditions to determine what data is stored and when the data is cleared. These
conditions include:
 - Application Installed but not Used
 - Application Used but not Cleared
 - Application Used but Cleared
 - Application Used but Cleared and Used after being Cleared

### <u>Analysis of DuckDuckGo's Underlying Storage</u>
To retrieve DuckDuckGo data from the Nox Player, we can utilize the Android Debug Bridge to connect to the emulated
device. To connect to the device, we can run `adb.exe connect 127.0.0.1:62001` followed by `adb.exe devices` to ensure
the connection was successful. Once we have established a connection to the device[2], we can open a command shell on the
device using `adb.exe -s 127.0.0.1:62001 shell` and run use the find command to search for files with duck in their file
path `find / -type f | grep -i duck`.

In my testing, the majority of the user data for DuckDuckGo was stored in: `/data/data/com.duckduckgo.mobile.android`

Within the above directory, DuckDuckGo data is broken up into 5 subdirectories with a specific purpose:
 - databases: application databases
 - cache: duckduckgo.com cache
 - app_webview: web browsing cache and databases
 - shared_prefs: application configuration files
 - files: application support files (trackers whitelist, helper scripts, etc.)

To retrieve the data from the device, we can exit the shell and pull back each of the individual subdirectories:
```
adb.exe -s 127.0.0.1:62001 pull /data/data/com.duckduckgo.mobile.android/databases
adb.exe -s 127.0.0.1:62001 pull /data/data/com.duckduckgo.mobile.android/cache
adb.exe -s 127.0.0.1:62001 pull /data/data/com.duckduckgo.mobile.android/app_webview
adb.exe -s 127.0.0.1:62001 pull /data/data/com.duckduckgo.mobile.android/shared_prefs
adb.exe -s 127.0.0.1:62001 pull /data/data/com.duckduckgo.mobile.android/files
```

In examining the above subdirectories, we come across items of potential forensic interest to include:
1. `databases/app.db` - SQLite3 database containing tables for artifacts such as bookmarks, sites visited, and app usage.
2. `databases/http_auth.db` - SQLite3 database containing http authentication information.
3. `cache/*` - The primary cache for duckduckgo.com interaction. Each file in the duckduckgo.com cache is named in the
following format '{MD5 Hash of URL}.{File Type}' where the file type refers to whether the file is the HTTP request ('0')
or the HTTP content ('1') returned (see example below).
    ```
    File Name: 0ef3124400f18b4ac08607674469f816.0
    File Type: 0 (HTTP Request)
    URL: https://staticcdn.duckduckgo.com/https/https-mobile-bloom-spec.json?cache_version=1
    
    File Name: 0ef3124400f18b4ac08607674469f816.1
    File Type: 1 (HTTP Content)
    URL: https://staticcdn.duckduckgo.com/https/https-mobile-bloom-spec.json?cache_version=1
    ```
4. `app_webview/Cache/*` - The cache for all other sites interacted with through the app. This cache does not use the
same structure as the cache described previously. Instead, each file in the cache contains a combination of strings and
raw data which can be parsed. By examining the overall structure of these files, it is possible to define the format of
the data which can be parsed.
5. `app_webview/Cookies` - SQLite3 database containing cookies from web browsing.
6. `app_webview/Web Data` - SQLite3 database containing autofill data from web browsing.
7. `com.duckduckgo.mobile.android/shared_prefs/*.xml` - XML formatted files which contain summary data about the
DuckDuckGo application to include the installation time, the last cleared time, and if the application has been used
since it was last cleared.

### <u>Data Available to Forensic Examiners</u>
Using the previously discussed testing methodology on the artifacts identified, we can determine what data survives
DuckDuckGo's "Clear All Tabs and Data" feature. Based on my analysis, DuckDuckGo does a good job of clearing the cached
data as well as data from a large number of tables when the users clears it. That being said, tables such as
'site_visited', 'app_days_used', and 'bookmarks' survive the clearing process. 

If data has not been cleared, all of the artifacts discussed can be extracted with varying levels of difficulty. For
example, all of the SQLite3 databases and XML files are easily parsed with an assortment of free tools (Notepad++,
DB Browser for SQLite, etc.) whereas the core web cache `app_webview/Cache/*` required some time to reverse engineer a
small part of the structure of the cached data to help automate the overall extraction.

### <u>Python Parser</u>
To aid in analysis of DuckDuckGo data, I wrote a parser in Python which provides summary data about the application and
artifacts of potential interest. All of the above artifacts are currently parsed[3]. This has been manually tested and
verified with HxD and DB Browser for SQLite. 

The parser can be found on GitHub at [https://github.com/ItWasDNS/DDG-Parser] and is structured as a set of modules
which can be ran individually or as a group for bulk processing. Future work could include processing artifacts such as
the SQLite database write-ahead logs (*.db-wal), processing additional tables from the databases, and enhancing the cache
extraction to parse more data.

### <u>Python Parser Usage</u>
To run all modules, run the below command and follow the prompt:
```
python3 process_duckduck.py
```
To run an individual module, run the below command and follow the prompt:
```
python3 modules/{module_name}.py
```

Note: User will be prompted for DuckDuckGo application data directory. This directory does not need to be
com.duckduckgo.mobile.android but should contain DDG application data.

### <u>Footnotes</u>
1. [Viewing extracted Android app data using an emulator](
https://abrignoni.blogspot.com/2017/08/viewing-extracted-android-app-data.html)
2. <u>Note</u>: If multiple devices are present, we can use -s to specify the connection to the emulated device previously established
3. <u>Note</u>: All 7 artifacts listed above are parsed but there may be additional items of interest within each artifact which can be parsed to a greater extent
