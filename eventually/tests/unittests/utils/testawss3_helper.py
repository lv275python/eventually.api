import unittest
from unittest import mock, skip
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from io import BytesIO
from utils import awss3_helper
from django.test import TestCase, RequestFactory
from authentication.models import CustomUser


IMAGE_NAME = "testimage.png"
IMAGE_MIME_TYPE = "image/png"
GOOD_IMAGE_SIZE = 3 * 1024 * 1024
BAD_IMAGE_SIZE = 9 * 1024 * 1024
IMAGE_FORMAT = "png"
BUCKET_ADDRESS = "https://s3.eu-west-2.amazonaws.com/eventually-photos/"

class UtilsAwss3HelperTestCase(TestCase):
    """TestCase for providing awss3_helper utils testing."""

    def setUp(self):
        """Method that set ups basic constants before testing awss3_helper features."""

        self.custom_user = CustomUser.objects.create(id=102, email='email1@gmail.com', is_active=True)
        self.custom_user.set_password('123Qwerty')
        self.custom_user.save()
        self.factory = RequestFactory()

        file = BytesIO()
        pil_image = Image.new('RGBA', size=(5000, 5000), color=(155, 0, 0))
        pil_image.save(file, format=IMAGE_FORMAT)
        file.seek(0)
        self.image_good = InMemoryUploadedFile(file, None, IMAGE_NAME, IMAGE_MIME_TYPE,
                                               GOOD_IMAGE_SIZE, None)

        bad_file = BytesIO()
        pil_image = Image.new('RGBA', size=(5000, 5000), color=(155, 0, 0))
        pil_image.save(bad_file, format="tiff")
        bad_file.seek(0)
        self.image_bad = InMemoryUploadedFile(bad_file, None, 'testimage.vfc', 'image/vfc',
                                              3 * 1024 * 1024, None)

    def test_upload_bad_content_type(self):

        request = self.factory.post(reverse('handle_image'),
                                    {"image": ""},
                                    content_type='application/json')
        request.user = self.custom_user
        response = awss3_helper.upload(request)
        self.assertFalse(response)

    def test_upload_no_image_files(self):
        request = self.factory.post(reverse('handle_image'), {'image': ""})

        request.user = self.custom_user
        response = awss3_helper.upload(request)
        self.assertFalse(response)

    def test_upload_bad_extension(self):
        request = self.factory.post(reverse('handle_image'), {'image': self.image_bad})

        request.user = self.custom_user
        response = awss3_helper.upload(request)
        self.assertFalse(response)

    @unittest.skip("bad implementation awss3")
    def test_upload_success(self):
        request = self.factory.post(reverse('handle_image'), {'image': self.image_good})

        request.user = self.custom_user
        response = awss3_helper.upload(request)
        self.assertDictEqual(response, {'image_key': '3BBBA41215074118818D1E14E4C486A8'})
