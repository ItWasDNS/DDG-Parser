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

### <u>Analysis of DuckDuckGo's Underlying Storage</u>
In my testing, the majority of the user data for DuckDuckGo was stored in: `/data/data/com.duckduckgo.mobile.android`

Within the above directory, DuckDuckGo data is broken up into 5 subdirectories with a specific purpose:
 - databases: DuckDuckGo application databases
 - cache: duckduckgo.com cache
 - app_webview: web browsing cache and databases
 - shared_prefs: DuckDuckGo application configuration files
 - files: DuckDuckGo application support files (trackers whitelist, helper scripts, etc.)

### <u>Artifacts of Interest</u>
Having examined the data pulled back from the device, I found the following artifacts to be of potential forensic interest:
1. 'databases/app.db' - SQLite3 database containing tables for artifacts such as bookmarks, tabs, sites visited, and app
usage
2. 'databases/http_auth.db' - SQLite3 database containing a table for authentication information for successful HTTP
authentication attempts
3. 'cache/*' - The primary cache for duckduckgo.com interaction
4. 'app_webview/Cache/*' - The cache for all other sites interacted with through the DuckDuckGo app
5. 'app_webview/Cookies' - SQLite3 database containing cookies from web browsing
6. 'app_webview/Web Data' - SQLite3 database containing autofill data from web browsing
7. 'shared_prefs/*.xml' - XML formatted files which contain summary data about the DuckDuckGo application to include the
installation time and the last cleared time

### <u>Python Parser</u>
To aid in analysis of DuckDuckGo data, I wrote a parser in Python 3 which provides summary data about DuckDuckGo and
artifacts of potential interest. All of the above artifacts are currently parsed[2]. This has been manually tested and
verified with HxD and DB Browser for SQLite. 

The parser can be found on GitHub at [https://github.com/ItWasDNS/DDG-Parser] and is structured as a set of modules
which can be ran individually or as a group for bulk processing. Future work could include processing additional tables
from the databases and enhancing the cache extraction to parse more data.

To run all modules, run the below command and follow the prompt:
```
python3 process_duckduck.py
```

Note: User will be prompted for DuckDuckGo application data directory. This directory does not need to be
com.duckduckgo.mobile.android but should contain DDG application data.

### <u>Footnotes</u>
1. [Viewing extracted Android app data using an emulator](
https://abrignoni.blogspot.com/2017/08/viewing-extracted-android-app-data.html)
2. <u>Note</u>: All 7 artifacts listed above are parsed but there may be additional items of interest within each artifact which can be parsed to a greater extent
