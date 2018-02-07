import json
from io import BytesIO
from unittest import mock

from PIL import Image
from botocore.exceptions import ClientError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase, RequestFactory
from django.urls import reverse

from authentication.models import CustomUser
from utils import awss3_helper

IMAGE_NAME = "testimage.png"
IMAGE_MIME_TYPE = "image/png"
GOOD_IMAGE_SIZE = 3 * 1024 * 1024
BAD_IMAGE_SIZE = 9 * 1024 * 1024
IMAGE_FORMAT = "png"
BUCKET_ADDRESS = "https://s3.eu-west-2.amazonaws.com/eventually-photos/"

IMAGE_KEY = "image_key"


class MockObjectsLoadRaiseClientError():
    key = IMAGE_KEY

    def load(self):
        error_response = {'Error': {'Code': '500', 'Message': 'Error Uploading'}}
        raise ClientError(error_response, 'create_stream')


class MockObjectsLoadReturnTrue():
    key = IMAGE_KEY

    def load(self):
        return True


class MockBOTO_S3LoadRaiseClientError():
    """ Class for simulate BOTO_S3 """

    @staticmethod
    def Object(*args, **kwargs):
        return MockObjectsLoadRaiseClientError()


class MockBOTO_S3TLoadReturnTrue():
    @staticmethod
    def Object(*args, **kwargs):
        return MockObjectsLoadReturnTrue()


class MockBUCKET():
    """ Class for simulate BUCKET """

    @staticmethod
    def put_object(*args, **kwargs):
        response = MockObjectsLoadReturnTrue()
        return response

    @staticmethod
    def delete_objects(**kwargs):
        return {
            'DeleteMarker': True,
            'VersionId': 'string',
            'RequestCharged': 'requester'
        }


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
        """Method that test is not success `upload` method when bad content type."""

        request = self.factory.post(reverse('handle_image'),
                                    {"image": ""},
                                    content_type='application/json')
        request.user = self.custom_user
        response = awss3_helper.upload(request)
        self.assertFalse(response)

    def test_upload_no_image_files(self):
        """Method that test is not success `upload` method when not image files."""

        request = self.factory.post(reverse('handle_image'), {'image': ""})

        request.user = self.custom_user
        response = awss3_helper.upload(request)
        self.assertFalse(response)

    def test_upload_bad_extension(self):
        """Method that test is not success `upload` method when image have bad extension."""

        request = self.factory.post(reverse('handle_image'), {'image': self.image_bad})

        request.user = self.custom_user
        response = awss3_helper.upload(request)
        self.assertFalse(response)

    @mock.patch('utils.awss3_helper.BOTO_S3', MockBOTO_S3LoadRaiseClientError)
    @mock.patch('utils.awss3_helper.BUCKET', MockBUCKET)
    def test_upload_success(self):
        """Method that test success `upload` method."""

        request = self.factory.post(reverse('handle_image'), {'image': self.image_good})

        request.user = self.custom_user

        response = awss3_helper.upload(request)
        self.assertDictEqual(response, {'image_key': 'image_key'})

    @mock.patch('utils.awss3_helper.BOTO_S3', MockBOTO_S3TLoadReturnTrue)
    @mock.patch('utils.awss3_helper.BUCKET', MockBUCKET)
    def test_upload_not_success(self):
        """Method that test is not success `upload` method."""

        request = self.factory.post(reverse('handle_image'), {'image': self.image_good})

        request.user = self.custom_user

        response = awss3_helper.upload(request)
        self.assertFalse(response)

    def test_delete_bad_content_type(self):
        """Method that test is not success `delete` method when bad content type."""

        request = self.factory.delete(reverse('handle_image'), {}, content_type='text/plain')

        request.user = self.custom_user

        response = awss3_helper.delete(request)
        self.assertFalse(response)

    def test_delete_not_image_key(self):
        """Method that test is not success `delete` method when not image key."""

        request = self.factory.delete(reverse('handle_image'),
                                      data=json.dumps({'image_key': ''}),
                                      content_type='application/json')

        request.user = self.custom_user

        response = awss3_helper.delete(request)
        self.assertFalse(response)

    @mock.patch('utils.awss3_helper.BUCKET', MockBUCKET)
    @mock.patch('utils.awss3_helper.BOTO_S3', MockBOTO_S3LoadRaiseClientError)
    def test_delete_success(self):
        """Method that test success `delete` method."""

        request = self.factory.delete(reverse('handle_image'),
                                      data=json.dumps({'image_key': 'image_key'}),
                                      content_type='application/json')

        request.user = self.custom_user

        response = awss3_helper.delete(request)
        self.assertTrue(response)

    @mock.patch('utils.awss3_helper.BUCKET', MockBUCKET)
    @mock.patch('utils.awss3_helper.BOTO_S3', MockBOTO_S3TLoadReturnTrue)
    def test_delete_not_success(self):
        """Method that test is not success `delete` method."""

        request = self.factory.delete(reverse('handle_image'),
                                      data=json.dumps({'image_key': 'image_key'}),
                                      content_type='application/json')

        request.user = self.custom_user

        response = awss3_helper.delete(request)
        self.assertFalse(response)
