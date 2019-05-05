"""
    Process 'com.duckduckgo.mobile.android/cache/*'
"""

import os
import re
import gzip
from modules.helpers.ddg_path_handler import process_directory_paths
from modules.helpers.ddg_extension_handler import process_file_types

cache_request = """--
File: %s
%s: %s
Version: %s
Status Code: %s
Content Type: %s
Content Encoding: %s
"""


def process_cache(duckduckgo_path, output_path):
    """ Process files from DDG Cache """
    if not os.path.exists(output_path + 'cache'):
        os.mkdir(output_path + 'cache')
    path = duckduckgo_path + 'cache/'
    tree = os.walk(path)
    with open(os.path.join(output_path, 'cache_output.txt'), 'w') as o:
        o.write("Processed: 'com.duckduckgo.mobile.android/cache/*'\n")
        for dir_entry in tree:
            files = dir_entry[2]
            for file in sorted(files):
                try:
                    if file != 'journal':
                        # HTTP Request
                        if file[len(file)-1] == '0':
                            with open(os.path.join(path, file), 'r') as f:
                                lines = f.readlines()
                            url = lines[0].strip()
                            request = lines[1].strip()
                            version = "Not Parsed"
                            status = "Not Parsed"
                            content_type = "Not Parsed"
                            content_encoding = "N/A"
                            for line in lines:
                                if re.search('^HTTP', line):
                                    version = line.strip().split(' ')[0]
                                    status = line.strip().split(' ')[1]
                                elif re.search('^content-type', line.lower()):
                                    content_type = line.strip()
                                elif re.search('^content-encoding', line.lower()):
                                    content_encoding = line.strip()
                            o.write(cache_request % (file,
                                                     request, url,
                                                     version, status,
                                                     content_type,
                                                     content_encoding))
                            # Corresponding HTTP Content (Simplify)
                            file = file[:len(file)-1] + '1'
                            full_path = os.path.join(path, file)
                            data = open(full_path, 'rb').read()
                            extension = process_file_types(content_type)
                            output_file = "%s.%s" % (file, extension)
                            with open(os.path.join(output_path, 'cache', output_file), 'wb') as out:
                                if 'gzip' in content_encoding:
                                    out.write(gzip.decompress(data))
                                else:
                                    out.write(data)
                except FileNotFoundError:
                    o.write("File does not exist: %s\n" % (path + file))
                except Exception:
                    o.write("Error Processing File: %s\n" % file)
            break


if __name__ == '__main__':
    # Set DDG application data path for testing
    ddg_path, out_path = process_directory_paths()
    # Process artifacts
    process_cache(ddg_path, out_path)
