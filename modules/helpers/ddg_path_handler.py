"""
    Handle directory paths for DuckDuckGo Parser
"""

import os


def process_directory_paths():
    """ Process directory paths core """
    while True:
        ddg_path = input("Enter full path of com.duckduckgo.mobile.android: ")
        if os.path.exists(ddg_path):
            if ddg_path[-1:] != '/':
                ddg_path += '/'
            break
        else:
            print("Directory does not exist. Please try again.")

    while True:
        output_path = input("Enter full path to output results: ")
        if os.path.exists(output_path):
            if output_path[-1:] != '/':
                output_path += '/'
            print("Directory already exists. Continuing could overwrite existing data.")
            advance = input("Do you wish to continue (y/n): ")
            if advance.strip().lower() == 'y':
                break
        else:
            if output_path[-1:] != '/':
                output_path += '/'
            os.mkdir(output_path)
            break

    return ddg_path, output_path
