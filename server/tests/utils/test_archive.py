import arrow
import os
import shutil
import pathlib
import unittest

from cartaro.utils.archive import Archive
class ArchiveTest(unittest.TestCase):

    TEST_DIR = pathlib.Path(F"{os.path.dirname(__file__)}/..").resolve()
    ARCHIVE_PATH = os.path.join(TEST_DIR, 'tmp', 'archive')

    @classmethod
    def setUpClass(cls):
        os.makedirs(cls.ARCHIVE_PATH)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.ARCHIVE_PATH)

    def setUp(self):
        self.archive = Archive(self.ARCHIVE_PATH)

    def tearDown(self):
        self.archive.remove_all()

    def test_construct(self):
        with self.assertRaisesRegex(ValueError, "Path must be a directory and must exist."):
            Archive('test_archive.py')

    def test_add_file(self):
        files = self.archive.files()
        self.assertEqual(len(files), 0)

        self.archive.add(F'{self.TEST_DIR}/test_config.py')
        files = self.archive.files()
        self.assertEqual(len(files), 1)
        self.assertRegex(files[0], r'test_config-\d{8,8}_\d{4,4}\.py')

    def test_add_dir(self):
        files = self.archive.files()
        self.assertEqual(len(files), 0)

        self.archive.add(F'{self.TEST_DIR}/data')
        files = self.archive.files()
        self.assertEqual(len(files), 1)
        self.assertRegex(files[0], r'data-\d{8,8}_\d{4,4}\.zip')

    def test_add_error(self):
        with self.assertRaisesRegex(ValueError, "Unsupported Src Type or Invalid Path"):
            self.archive.add('/dev/null')


    def test_clean(self):
        self.archive.add(F'{self.TEST_DIR}/controller')
        self.archive.add(F'{self.TEST_DIR}/data')
        self.archive.add(F'{self.TEST_DIR}/model')

        files = self.archive.files()
        self.assertEqual(len(files), 3)

        # Set the A & M times of the first file to 8 days ago
        new_time = arrow.get().shift(days=-8).datetime.timestamp()
        os.utime(os.path.join(self.ARCHIVE_PATH, files[0]), (new_time, new_time))

        self.archive.clean()
        files = self.archive.files()
        self.assertEqual(len(files), 2)










# 
