"""
    Handle file extensions for data extracted from caches
"""


def process_file_types(content_type):
    """ Handle naming of files extracted from cache """
    if 'css' in content_type:
        end = 'css'
    elif 'gif' in content_type:
        end = 'gif'
    elif 'html' in content_type:
        end = 'html'
    elif 'javascript' in content_type:
        end = 'js'
    elif 'jpeg' in content_type:
        end = 'jpeg'
    elif 'json' in content_type:
        end = 'json'
    elif 'mp4' in content_type:
        end = 'mp4'
    elif 'octet-stream' in content_type:
        end = 'raw'
    elif 'png' in content_type:
        end = 'png'
    elif 'text/plain' in content_type:
        end = 'txt'
    else:
        end = 'other'
    return end
