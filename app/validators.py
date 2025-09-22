from django.core.exceptions import ValidationError
import os
import uuid
from django.conf import settings

def get_unique_file_path(filename, directory):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    filepath = os.path.join(settings.MEDIA_ROOT, directory, filename)
    while os.path.exists(filepath):
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(settings.MEDIA_ROOT, directory, filename)
    return os.path.join(directory, filename)


def get_candidate_image_path(instance, filename):
    return get_unique_file_path(filename, "candidate")

def get_flag_image_path(instance, filename):
    return get_unique_file_path(filename, "flag")

megabyte_limit = 10
def image_validate(file):
    filesize = file.size
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))