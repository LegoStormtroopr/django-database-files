import base64
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control
import mimetypes
from database_files.models import FileInDatabase
# import os
# from PIL import Image
# from io import StringIO


def get_file(name):
    name = "/" + name.lstrip("/")
    f = get_object_or_404(FileInDatabase, name=name)
    return f


@cache_control(max_age=86400)
def serve(request, name):
    f = get_file(name)
    return return_image_response(name, base64.b64decode(f.content), f.size)


# @cache_control(max_age=86400)
# def serve_thumb(request, name, x, y):
#     f = get_image(name)
#     stream = StringIO(base64.b64decode(f.content))
#     output = StringIO()
#     thumb = Image.open(stream)
#     thumb.thumbnail((int(x),int(y)))
#     thumb.save(output, format='JPEG')
#     return return_image_response(name, output.getvalue(), len(output.getvalue()))


def return_image_response(name, content, size):
    mimetype = mimetypes.guess_type(name)[0] or 'application/octet-stream'
    response = HttpResponse(content, content_type=mimetype)
    response['Content-Length'] = size
    return response
