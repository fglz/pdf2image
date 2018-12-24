import os
import sys
import tempfile
import unittest
import time
import subprocess

# polyfill for python27
try:
    from tempfile import TemporaryDirectory
except ImportError:
    import shutil

    class TemporaryDirectory(object):
        def __init__(self):
            self.name = tempfile.mkdtemp()

        def __enter__(self):
            return self.name

        def __exit__(self, exc, value, tb):
            shutil.rmtree(self.name)

from memory_profiler import profile as profile_memory

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf2image import convert_from_bytes, convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

from functools import wraps

PROFILE_MEMORY = False

try:
    subprocess.call(["pdfinfo", "-h"], stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
    POPPLER_INSTALLED = True
except OSError as e:
    if e.errno == os.errno.ENOENT:
        POPPLER_INSTALLED = False

def profile(f):
    if PROFILE_MEMORY:
        @wraps(f)
        @profile_memory
        def wrapped(*args, **kwargs):
            r = f(*args, **kwargs)
            return r
        return wrapped
    else:
        @wraps(f)
        def wrapped(*args, **kwargs):
            r = f(*args, **kwargs)
            return r
        return wrapped

class PDFConversionMethods(unittest.TestCase):
    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes(self):
        start_time = time.time()
        with open('./tests/test.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read())
            self.assertTrue(len(images_from_bytes) == 1)
        print('test_conversion_from_bytes: {} sec'.format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test.pdf')
        self.assertTrue(len(images_from_path) == 1)
        print('test_conversion_from_path: {} sec'.format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path)
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir: {} sec'.format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test.pdf', output_folder=path)
            self.assertTrue(len(images_from_path) == 1)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir: {} sec'.format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_14(self):
        start_time = time.time()
        with open('./tests/test_14.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read())
            self.assertTrue(len(images_from_bytes) == 14)
        print('test_conversion_from_bytes_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_14.pdf')
        self.assertTrue(len(images_from_path) == 14)
        print('test_conversion_from_path_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_14(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test_14.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path)
                self.assertTrue(len(images_from_bytes) == 14)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_14(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test_14.pdf', output_folder=path)
            self.assertTrue(len(images_from_path) == 14)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_conversion_from_bytes_241(self): # pragma: no cover
        start_time = time.time()
        with open('./tests/test_241.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read())
            self.assertTrue(len(images_from_bytes) == 241)
        print('test_conversion_from_bytes_241: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_conversion_from_path_241(self): # pragma: no cover
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_241.pdf')
        self.assertTrue(len(images_from_path) == 241)
        print('test_conversion_from_path_241: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_conversion_from_bytes_using_dir_241(self): # pragma: no cover
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test_241.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path)
                self.assertTrue(len(images_from_bytes) == 241)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_241: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_conversion_from_path_using_dir_241(self): # pragma: no cover
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test_241.pdf', output_folder=path)
            self.assertTrue(len(images_from_path) == 241)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_241: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_empty_if_not_pdf(self):
        start_time = time.time()
        with self.assertRaises(Exception):
            convert_from_path('./tests/test.jpg')
        print('test_empty_if_not_pdf: {} sec'.format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_empty_if_file_not_found(self):
        start_time = time.time()
        with self.assertRaises(Exception):
            convert_from_path('./tests/totally_a_real_file_in_folder.xyz')
        print('test_empty_if_file_not_found: {} sec'.format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_empty_if_corrupted_pdf(self):
        start_time = time.time()
        with self.assertRaises(Exception):
            convert_from_path('./tests/test_corrupted.pdf')
        print('test_empty_if_corrupted_pdf: {} sec'.format(time.time() - start_time))

    ## Test first page

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_14_first_page_12(self):
        start_time = time.time()
        with open('./tests/test_14.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), first_page=12)
            self.assertTrue(len(images_from_bytes) == 3)
        print('test_conversion_from_bytes_14_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_first_page_12(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_14.pdf', first_page=12)
        self.assertTrue(len(images_from_path) == 3)
        print('test_conversion_from_path_14_first_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_14_first_page_12(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test_14.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, first_page=12)
                self.assertTrue(len(images_from_bytes) == 3)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_14_first_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_14_first_page_12(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test_14.pdf', output_folder=path, first_page=12)
            self.assertTrue(len(images_from_path) == 3)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_14_first_page_12: {} sec'.format((time.time() - start_time) / 14.))

    ## Test last page

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_14_last_page_12(self):
        start_time = time.time()
        with open('./tests/test_14.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), last_page=12)
            self.assertTrue(len(images_from_bytes) == 12)
        print('test_conversion_from_bytes_14_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_last_page_12(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_14.pdf', last_page=12)
        self.assertTrue(len(images_from_path) == 12)
        print('test_conversion_from_path_14_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_14_last_page_12(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test_14.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, last_page=12)
                self.assertTrue(len(images_from_bytes) == 12)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_14_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_14_last_page_12(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test_14.pdf', output_folder=path, last_page=12)
            self.assertTrue(len(images_from_path) == 12)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_14_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    ## Test first and last page

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_14_first_page_2_last_page_12(self):
        start_time = time.time()
        with open('./tests/test_14.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), first_page=2, last_page=12)
            self.assertTrue(len(images_from_bytes) == 11)
        print('test_conversion_from_bytes_14_first_page_2_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_first_page_2_last_page_12(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_14.pdf', first_page=2, last_page=12)
        self.assertTrue(len(images_from_path) == 11)
        print('test_conversion_from_path_14_first_page_2_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_14_first_page_2_last_page_12(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test_14.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, first_page=2, last_page=12)
                self.assertTrue(len(images_from_bytes) == 11)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_14_first_page_2_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_14_first_page_2_last_page_12(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test_14.pdf', output_folder=path, first_page=2, last_page=12)
            self.assertTrue(len(images_from_path) == 11)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_14_first_page_2_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    ## Test output as jpeg

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_jpeg_from_bytes(self):
        start_time = time.time()
        with open('./tests/test.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), fmt='jpg')
            self.assertTrue(images_from_bytes[0].format == 'JPEG')
        print('test_conversion_to_jpeg_from_bytes_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_jpeg_from_path_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test.pdf', output_folder=path, fmt='jpeg')
            self.assertTrue(images_from_path[0].format == 'JPEG')
            [im.close() for im in images_from_path]
        print('test_conversion_to_jpeg_from_path_using_dir_14: {} sec'.format((time.time() - start_time) / 14.))

    ## Test output as png

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_png_from_bytes(self):
        start_time = time.time()
        with open('./tests/test.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), fmt='png')
            self.assertTrue(images_from_bytes[0].format == 'PNG')
        print('test_conversion_to_png_from_bytes_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_png_from_path_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test.pdf', output_folder=path, fmt='png')
            self.assertTrue(images_from_path[0].format == 'PNG')
            [im.close() for im in images_from_path]
        print('test_conversion_to_png_from_path_using_dir_14: {} sec'.format((time.time() - start_time) / 14.))

    ## Test output with not-empty output_folder

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_non_empty_output_folder(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test.pdf', output_folder='./tests/')
        self.assertTrue(len(images_from_path) == 1)
        [os.remove(im.filename) for im in images_from_path]
        print('test_non_empty_output_folder: {} sec'.format((time.time() - start_time) / 14.))

    ## Test format that starts with a dot

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_format_that_starts_with_a_dot(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, fmt='.jpg')
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print('test_format_that_starts_with_a_dot: {} sec'.format(time.time() - start_time))

    ## Test locked PDF

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_locked_pdf_with_userpw_only(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test_locked_user_only.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, fmt='.jpg', userpw='pdf2image')
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print('test_locked_pdf_with_userpw_only: {} sec'.format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_not_locked_pdf(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, fmt='.jpg', userpw='pdf2image')
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print('test_locked_pdf_with_userpw_only: {} sec'.format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_locked_pdf_with_ownerpw_only(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test_locked_owner_only.pdf', 'rb') as pdf_file:
                # No need to pass a ownerpw because the absence of userpw means we can read it anyway
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, fmt='.jpg')
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print('test_locked_pdf_with_ownerpw_only: {} sec'.format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_locked_pdf_with_ownerpw_and_userpw(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test_locked_both.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, fmt='.jpg', userpw='pdf2image')
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print('test_locked_pdf_with_ownerpw_and_userpw: {} sec'.format(time.time() - start_time))

    ## Tests cropbox

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_cropbox(self):
        start_time = time.time()
        with open('./tests/test.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), use_cropbox=True)
            self.assertTrue(len(images_from_bytes) == 1)
        print('test_conversion_from_bytes_using_cropbox: {} sec'.format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_cropbox(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test.pdf', use_cropbox=True)
        self.assertTrue(len(images_from_path) == 1)
        print('test_conversion_from_path_using_cropbox: {} sec'.format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_and_cropbox(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, use_cropbox=True)
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_and_cropbox: {} sec'.format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_and_cropbox(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test.pdf', output_folder=path, use_cropbox=True)
            self.assertTrue(len(images_from_path) == 1)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_and_cropbox: {} sec'.format(time.time() - start_time))

    ## Tests multithreading

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_14_with_4_threads(self):
        start_time = time.time()
        with open('./tests/test_14.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), thread_count=4)
            self.assertTrue(len(images_from_bytes) == 14)
        print('test_conversion_from_bytes_14_with_4_thread: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_with_4_threads(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_14.pdf', thread_count=4)
        self.assertTrue(len(images_from_path) == 14)
        print('test_conversion_from_path_14_with_4_thread: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_14_with_15_threads(self):
        start_time = time.time()
        with open('./tests/test_14.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), thread_count=15)
            self.assertTrue(len(images_from_bytes) == 14)
        print('test_conversion_from_bytes_14_with_15_thread: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_with_0_threads(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_14.pdf', thread_count=0)
        self.assertTrue(len(images_from_path) == 14)
        print('test_conversion_from_path_14_with_4_thread: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_14_with_4_threads(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test_14.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, thread_count=4)
                self.assertTrue(len(images_from_bytes) == 14)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_14_with_4_thread: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_14_with_4_threads(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test_14.pdf', output_folder=path, thread_count=4)
            self.assertTrue(len(images_from_path) == 14)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_14_with_4_thread: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_241_with_4_threads(self): # pragma: no cover
        start_time = time.time()
        with open('./tests/test_241.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), thread_count=4)
            self.assertTrue(len(images_from_bytes) == 241)
        print('test_conversion_from_bytes_241_with_4_thread: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_241_with_4_threads(self): # pragma: no cover
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_241.pdf', thread_count=4)
        self.assertTrue(len(images_from_path) == 241)
        print('test_conversion_from_path_241_with_4_thread: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_241_with_4_threads(self): # pragma: no cover
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open('./tests/test_241.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, thread_count=4)
                self.assertTrue(len(images_from_bytes) == 241)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_241_with_4_thread: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_241_with_4_threads(self): # pragma: no cover
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test_241.pdf', output_folder=path, thread_count=4)
            self.assertTrue(len(images_from_path) == 241)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_241_with_4_thread: {} sec'.format((time.time() - start_time) / 241.))

    # Testing custom exceptions

    @unittest.skipIf(POPPLER_INSTALLED, "Poppler is installed, skipping.")
    def test_pdfinfo_not_installed_throws(self):
        start_time = time.time()
        try:
            images_from_path = convert_from_path('./tests/test_14.pdf')
            raise Exception("This should not happen")
        except PDFInfoNotInstalledError as ex:
            pass

        print('test_pdfinfo_not_installed_throws: {} sec'.format((time.time() - start_time) / 14.))

    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_missingfonterror_throws(self):
        start_time = time.time()        
        try:
            images_from_path = convert_from_path('./tests/test_strict.pdf', strict=True)
            raise Exception("This should not happen")
        except PDFSyntaxError as ex:
            pass

        print('test_syntaxerror_throws: {} sec'.format(time.time() - start_time))

if __name__=='__main__':
    unittest.main()
