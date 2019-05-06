"""
    Process 'com.duckduckgo.mobile.android/app_webview/Cache/*'
"""

import os
import re
import gzip
import struct
from modules.helpers.ddg_path_handler import process_directory_paths
from modules.helpers.ddg_extension_handler import process_file_types


def process_appwv_cache(duckduckgo_path, output_path):
    """ Process files from DDG 'app_webview/Cache' """
    # Create directory for cached content output
    if not os.path.exists(output_path + 'appwv_cache'):
        os.mkdir(output_path + 'appwv_cache')
    with open(os.path.join(output_path, 'appwv_cache_output.txt'), 'w') as o:
        o.write("Processed: 'com.duckduckgo.mobile.android/app_webview/Cache/*'")
    # Parse cached content
    path = duckduckgo_path + 'app_webview/Cache/'
    tree = os.walk(path)
    for dir_entry in tree:
        files = dir_entry[2]
        for file in sorted(files):
            try:
                if file != 'index':
                    # HTTP Request
                    with open(os.path.join(output_path, 'appwv_cache_output.txt'), 'a') as o:
                        o.write("\n--\nCache File: %s" % file)
                        with open(os.path.join(path, file), 'rb') as f:
                            content = f.read()
                            file_len = len(content)
                            # Retrieve URL
                            url_len = struct.unpack_from('i', content, 12)[0]
                            f.seek(20, 0)
                            url = f.read(url_len).decode("utf-8")
                            o.write("\nURL: %s" % url)
                            # Retrieve HTTP Header Content
                            s = re.search(b'\x00\x00HTTP', content).start()
                            f.seek(s+2, 0)
                            header = b''
                            counter = 0
                            while f.tell() < file_len:
                                next_byte = f.read(1)
                                if next_byte != b'\x00':
                                    header += next_byte
                                    counter = 0
                                else:
                                    if counter == 1:
                                        header = header[:len(header)-1]
                                        break
                                    else:
                                        header += next_byte
                                        counter = 1
                            extension = 'other'
                            gz = False
                            for item in header.split(b'\x00'):
                                i = item.decode("utf-8")
                                o.write("\n")
                                o.write(i)
                                if 'Content-Type:' in i:
                                    extension = process_file_types(i)
                                if 'gzip' in i:
                                    gz = True
                            content_len = struct.unpack_from('i', content, (s - 30))[0]
                            output_file = "%s.%s" % (file, extension)
                            with open(os.path.join(output_path, 'appwv_cache', output_file), 'wb') as out:
                                data = content[(url_len + 20):(url_len + 20 + content_len)]
                                if gz is True:
                                    out.write(gzip.decompress(data))
                                else:
                                    out.write(data)
            except FileNotFoundError as e:
                print("File Not Found: %s" % file)
                print(e)
        break


if __name__ == '__main__':
    # Process artifacts
    ddg_path, out_path = process_directory_paths()
    process_appwv_cache(ddg_path, out_path)
