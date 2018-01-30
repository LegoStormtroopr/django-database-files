import base64
from database_files import models
from django.core.files.base import File
from django.core.files.storage import Storage
# from django.urls import reverse
from io import StringIO, BytesIO


class DBFile(File):

    """
    A file returned from the database.
    """

    def __init__(self, file, name, storage):
        super().__init__(file, name)
        self._storage = storage

    def open(self, mode="rb"):
        # if self.closed:
        self.file = self._storage.open(self.name, mode).file
        return super().open(mode)


class DatabaseStorage(Storage):

    def _make_name(self, name):
        name = "/" + name.lstrip("/")
        return name

    def _open(self, name, mode='rb'):
        name = self._make_name(name)
        try:
            f = models.FileInDatabase.objects.get(name=name)
        except models.FileInDatabase.DoesNotExist:
            return None

        if 'b' in mode:
            fh = BytesIO(base64.b64decode(f.content))
        else:
            fh = StringIO(base64.b64decode(f.content).decode('utf-8'))
        fh.name = name
        fh.mode = mode
        fh.size = f.size
        return DBFile(fh, name, self)

    def _save(self, name, content):
        name = self._make_name(name)
        if 'b' in content.mode:
            _content = content.read()
        else:
            _content = content.read().encode('utf-8')

        models.FileInDatabase.objects.create(
            content=base64.b64encode(_content),
            size=content.size,
            name=name,
        )

        return name

    def exists(self, name):
        name = self._make_name(name)
        return models.FileInDatabase.objects.filter(name=name).exists()

    def delete(self, name):
        name = self._make_name(name)
        try:
            models.FileInDatabase.objects.get(name=name).delete()
        except models.FileInDatabase.DoesNotExist:
            pass

    # def url(self, name):
    #     return reverse('database_file', kwargs={'name': name})

    def size(self, name):
        name = self._make_name(name)
        try:
            return models.FileInDatabase.objects.get(name=name).size
        except models.FileInDatabase.DoesNotExist:
            return 0

    def listdir(self, path):
        path = self._make_name(path)

        path = path.rstrip("/") + "/"
        results = list(
            models.FileInDatabase.objects.filter(name__startswith=path).values_list("name", flat=True)
        )

        _files = []
        dirs = []
        path = path.rstrip("/")
        sub_path = len(path.split("/"))
        for r in results:
            parts = r.split("/")[sub_path:]
            # If there is only one more part its a file
            if len(parts) == 1:
                _files.append(parts[0])
            else:
                dirs.append(parts[0])
        dirs = list(set(dirs))
        _files.sort()
        dirs.sort()
        return dirs, _files

    def get_created_time(self, name):
        name = self._make_name(name)
        try:
            f = models.FileInDatabase.objects.get(name=name)
            return f.created_at
        except models.FileInDatabase.DoesNotExist:
            return None

    def get_modified_time(self, name):
        name = self._make_name(name)
        try:
            f = models.FileInDatabase.objects.get(name=name)
            return f.modified_at
        except models.FileInDatabase.DoesNotExist:
            return None
