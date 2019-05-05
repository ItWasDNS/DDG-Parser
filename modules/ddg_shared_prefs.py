"""
    Process 'com.duckduckgo.mobile.android/shared_prefs/*.xml'
"""

import os
import time
import xml.etree.ElementTree as ET
from modules.helpers.ddg_path_handler import process_directory_paths


def process_sharedprefs(duckduckgo_path, output_path):
    """ Process xml files from DDG 'shared_prefs' """
    # Parse Installation Time
    try:
        install_raw = ET.parse(duckduckgo_path + 'shared_prefs/com.duckduckgo.app.install.settings.xml')
        install = float(install_raw.getroot()[0].attrib['value'])/1000
        install = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(install))
        i_found = True
    except FileNotFoundError:
        install = '[Error: File not Found]'
        i_found = False
    # Parse Last Cleared Time
    try:
        cleared_raw = ET.parse(duckduckgo_path + 'shared_prefs/com.duckduckgo.app.fire.unsentpixels.settings.xml')
        cleared = float(cleared_raw.getroot()[0].attrib['value'])/1000
        cleared = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cleared))
        c_found = True
    except FileNotFoundError:
        cleared = '[Error: File not Found]'
        c_found = False
    # Determine if Used Since Last Cleared
    try:
        activity_raw = ET.parse(duckduckgo_path + 'shared_prefs/com.duckduckgo.app.settings_activity.settings.xml')
        activity = activity_raw.getroot()[0].attrib['value']
    except FileNotFoundError:
        if i_found and c_found:
            activity = 'none'
        else:
            activity = '[Error: File not Found]'
    # Write Output to File
    with open(os. path.join(output_path, 'shared_prefs_output.txt'), 'w') as o:
        o.write("Processed: 'com.duckduckgo.mobile.android/shared_prefs/*.xml'\n")
        o.write("Installation Time: %s\nLast Cleared Time: %s\nApp Used Since Last Cleared: %s" %
                (install, cleared, activity))


if __name__ == '__main__':
    # Set DDG application data path for testing
    ddg_path, out_path = process_directory_paths()
    # Process artifacts
    process_sharedprefs(ddg_path, out_path)
