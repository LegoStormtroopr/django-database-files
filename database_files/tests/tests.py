from tempfile import NamedTemporaryFile
from django.core import files
from django.test import TestCase
from database_files.models import FileInDatabase
from database_files.tests.models import Thing
import os
from django.core.files.storage import default_storage

this_dir = os.path.dirname(os.path.abspath(__file__))


class DatabaseFilesTestCase(TestCase):
    def test_adding_text_file(self):
        test_file = NamedTemporaryFile(
            mode="w+", suffix='.txt', delete=False
        )
        test_file.write('1234567890')
        test_file.close()

        f = open(test_file.name, mode="r+b")

        t = Thing.objects.create(
            upload=files.File(f, name=f.name.lstrip('/')),
        )
        self.assertEqual(FileInDatabase.objects.count(), 1)
        t = Thing.objects.get(pk=t.pk)

        self.assertEqual(t.upload.file.size, 10)
        self.assertTrue(t.upload.file.name.endswith('.txt'))

        t.upload.file.open(mode="rb")

        self.assertEqual(t.upload.file.read(), b'1234567890')

        t.upload.file.open(mode="rb")
        self.assertEqual(t.upload.file.read().decode('utf-8'), '1234567890')

        t.upload.file.open(mode="r")
        self.assertEqual(t.upload.file.read(), '1234567890')
        self.assertTrue(default_storage.exists(t.upload.file.name))
        t.upload.delete()
        self.assertEqual(FileInDatabase.objects.count(), 0)

        # discard file
        os.unlink(f.name)

    def test_adding_binary_file(self):
        lena = os.path.join(this_dir, "files", "lena.png")
        f = open(lena, mode="rb")
        size = os.path.getsize(lena)

        t = Thing.objects.create(
            upload=files.File(f, name="images/lena.png"),
        )
        self.assertEqual(FileInDatabase.objects.count(), 1)
        t = Thing.objects.get(pk=t.pk)

        self.assertEqual(t.upload.file.size, size)
        self.assertTrue(t.upload.file.name.endswith('.png'))
        self.assertEqual(t.upload.file.name, "/documents/images/lena.png")
        self.assertTrue(default_storage.exists("/documents/images/lena.png"))

        from PIL import Image

        t.upload.file.open(mode="rb")
        i1 = Image.open(t.upload.file)
        i2 = Image.open(lena)
        self.assertEqual(i1.size, i2.size)

    def test_listing_directory(self):
        files_dir = os.path.join(this_dir, "files")
        num_files = 0
        for subdir, dirs, _files in os.walk(files_dir):
            subdir = subdir[len(files_dir) + 1:]
            for fn in _files:
                num_files += 1
                with open(os.path.join(files_dir, subdir, fn), 'rb') as f:
                    path = os.path.join("mydocs", subdir, fn)
                    default_storage.save(name=path, content=f)

        for subdir, dirs, _files in os.walk(files_dir):
            subdir = subdir[len(files_dir) + 1:]
            path = os.path.join("mydocs", subdir)
            listed_dirs, listed_files = default_storage.listdir(path)
            self.assertEqual(listed_dirs, sorted(dirs))
            self.assertEqual(listed_files, sorted(_files))

    def test_access_times(self):
        qqq = os.path.join(this_dir, "files", "qq", "qqqq.qqq")
        f = open(qqq, mode="rb")

        t = Thing.objects.create(
            upload=files.File(f, name="qqqq.qqq"),
        )
        self.assertEqual(FileInDatabase.objects.count(), 1)
        t = Thing.objects.get(pk=t.pk)

        file_in_db = FileInDatabase.objects.get(name=t.upload.name)
        created = file_in_db.created_at
        modifed = file_in_db.modified_at

        self.assertEqual(
            default_storage.get_created_time(t.upload.name),
            created
        )
        self.assertEqual(
            default_storage.get_modified_time(t.upload.name),
            modifed
        )
