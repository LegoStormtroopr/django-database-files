import base64
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control
import mimetypes
from database_files.models import FileInDatabase
import os
# from PIL import Image
# from io import StringIO


def get_image(name):
    pk, file_ext = os.path.splitext(name)
    try:
        pk = int(pk)
    except ValueError:
        raise Http404('Filename is not an integer')
    f = get_object_or_404(FileInDatabase, pk=pk)
    return f


@cache_control(max_age=86400)
def serve(request, name):
    f = get_image(name)
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
