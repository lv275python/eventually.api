"""
Amazons3 view test
==================
"""

import json
from io import BytesIO
from unittest import mock
from PIL import Image
from django.test import TestCase, Client
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from authentication.models import CustomUser

IMAGE_NAME = "testimage.png"
IMAGE_MIME_TYPE = "image/png"
GOOD_IMAGE_SIZE = 3 * 1024 * 1024
BAD_IMAGE_SIZE = 9 * 1024 * 1024
IMAGE_FORMAT = "png"
BUCKET_ADDRESS = "https://s3.eu-west-2.amazonaws.com/eventually-photos/"

class AmazonS3TestCases(TestCase):
    """TestCases for the amazons3 view"""

    def setUp(self):
        """
        Set up of test user, client, valid and invalid image files.
        Log in test user to have access to upload delete functions
        """

        user = CustomUser.objects.create(id=101,
                                         first_name="Jerry",
                                         last_name="Newbey",
                                         middle_name="Jr.",
                                         email='mail@mail.com',
                                         is_active=True)
        user.set_password('1Aa')
        user.save()

        self.client = Client()
        user = json.dumps({'email': 'mail@mail.com', 'password': '1Aa'})
        self.client.post(reverse('login_user'), user, content_type='application/json')

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


    def test_post_valid_image(self):
        """ Test for successful POST method """

        with mock.patch('utils.awss3_helper.upload') as awss3_helper:
            awss3_helper.return_value = {"image": "SOMEIMAGEKEYSOMEIMAGEKEY"}
            response = self.client.post(reverse('handle_image'),
                                        {"image": self.image_good})
            self.assertIsInstance(response, JsonResponse)


    def test_post_invalid_image(self):
        """ Test POST method with invalid image """

        response = self.client.post(reverse('handle_image'),
                                    {"image": self.image_bad})
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_content_type(self):
        """ Test POST method with invalid content type """

        response = self.client.post(reverse('handle_image'),
                                    {"image": self.image_good},
                                    content_type="INVALID-CONTENT")
        self.assertEqual(response.status_code, 400)

    def test_post_no_image(self):
        """ Test POST method with no image """

        response = self.client.post(reverse('handle_image'),
                                    {"image": ""},
                                    content_type="INVALID-CONTENT")
        self.assertEqual(response.status_code, 400)

    def test_delete_positive(self):
        """ Test DELETE method with valid data """

        with mock.patch('utils.awss3_helper.delete') as awss3_helper:
            awss3_helper.return_value = True
            response = self.client.delete(reverse("handle_image"),
                                          json.dumps({"image_key": "SOMEIMAGEKEYSOMEIMAGEKEY"}),
                                          content_type="application/json")
            self.assertEqual(response.status_code, 200)

    def test_delete_negative(self):
        """ Test DELETE method with invalid data """

        response = self.client.delete(reverse("handle_image"),
                                      json.dumps({"image_key": "SOMEIMAGEKEYSOMEIMAGEKEY"}))
        self.assertEqual(response.status_code, 400)
