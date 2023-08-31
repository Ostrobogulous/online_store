import os
from OffbeatStore.utility_functions.operations import next_product_id_operation


def save_image(image_file, location=None, id=None):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    upload_folder = os.path.join(parent_dir, 'static', 'media')
    path = "/static/media/"

    if image_file is None or image_file.filename == '':
        if location is None:
            image_location = path + "default.png"
        else:
            image_location = location
    else:
        if location is not None:
            delete_image(location)
        if id is None:
            filename = str(next_product_id_operation()) + '.' + image_file.filename.rsplit('.', 1)[1].lower()
        else:
            filename = str(id) + '.' + image_file.filename.rsplit('.', 1)[1].lower()
        image_file.save(os.path.join(upload_folder, filename))
        image_location = path + filename
    return image_location


def fix_location(location):
    i = len(location) - 1
    ans = ""
    while location[i] != '/':
        ans += location[i]
        i -= 1
    ans = ans[::-1]
    return ans


def delete_image(location):
    if location != "/static/media/default.png":
        current_dir = os.path.abspath(os.path.dirname(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
        location = fix_location(location)
        path = os.path.join(parent_dir, 'static', 'media', location)
        os.remove(path)
