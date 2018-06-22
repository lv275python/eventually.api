import json

from io import BytesIO, StringIO
from unittest import mock

from PIL import Image
from botocore.exceptions import ClientError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase, RequestFactory
from django.urls import reverse

from authentication.models import CustomUser
from utils import awss3_helper

from customprofile.models import CustomProfile
from team.models import Team
import datetime

IMAGE_NAME = "testimage.png"
IMAGE_MIME_TYPE = "image/png"
GOOD_IMAGE_SIZE = 3 * 1024 * 1024
BAD_IMAGE_SIZE = 9 * 1024 * 1024
IMAGE_FORMAT = "png"
BUCKET_ADDRESS = "https://s3.eu-west-2.amazonaws.com/eventually-photos/"

IMAGE_KEY = "image_key"

TEST_TIME = datetime.datetime(2017, 10, 15, 8, 15, 12)


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


class MockClient():
    def list_objects(*args, **kwargs):
        return {'Contents': [
            {'Key': 'team_1'},
            {'Key': 'team_2'},
            {'Key': 'img1'},
            {'Key': 'img2'},
            {'Key': 'cus_prof_1'},
            {'Key': 'cus_prof_2'}
        ]}

class MockMeta():
    client = MockClient()

class MockBUCKET():
    """ Class for simulate BUCKET """

    @staticmethod
    def put_object(*args, **kwargs):
        response = MockObjectsLoadReturnTrue()
        return response

    @staticmethod
    def delete_objects(*args, **kwargs):
        return {
            'DeleteMarker': True,
            'VersionId': 'string',
            'RequestCharged': 'requester'
        }

    meta = MockMeta()
    name = "MockBUCKET"

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

        self.cus_prof_1 = CustomProfile.objects.create(photo = 'cus_prof_1')
        self.cus_prof_2 = CustomProfile.objects.create(photo = 'cus_prof_2')
        self.team_1 = Team.objects.create(image = 'team_1')
        self.team_2 = Team.objects.create(image = 'team_2')



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
    @mock.patch('utils.awss3_helper.BUCKET_IMG', MockBUCKET)
    def test_upload_success(self):
        """Method that test success `upload` method."""

        request = self.factory.post(reverse('handle_image'), {'image': self.image_good})

        request.user = self.custom_user

        response = awss3_helper.upload(request)
        self.assertDictEqual(response, {'image_key': 'image_key'})

    @mock.patch('utils.awss3_helper.BOTO_S3', MockBOTO_S3TLoadReturnTrue)
    @mock.patch('utils.awss3_helper.BUCKET_IMG', MockBUCKET)
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

    @mock.patch('utils.awss3_helper.BUCKET_IMG', MockBUCKET)
    @mock.patch('utils.awss3_helper.BOTO_S3', MockBOTO_S3LoadRaiseClientError)
    def test_delete_success(self):
        """Method that test success `delete` method."""

        request = self.factory.delete(reverse('handle_image'),
                                      data=json.dumps({'image_key': 'image_key'}),
                                      content_type='application/json')

        request.user = self.custom_user

        response = awss3_helper.delete(request)
        self.assertTrue(response)

    @mock.patch('utils.awss3_helper.BUCKET_IMG', MockBUCKET)
    @mock.patch('utils.awss3_helper.BOTO_S3', MockBOTO_S3TLoadReturnTrue)
    def test_delete_not_success(self):
        """Method that test is not success `delete` method."""

        request = self.factory.delete(reverse('handle_image'),
                                      data=json.dumps({'image_key': 'image_key'}),
                                      content_type='application/json')

        request.user = self.custom_user

        response = awss3_helper.delete(request)
        self.assertFalse(response)

    def test_get_all_img_keys(self):
        images_list = awss3_helper._get_all_img_keys()
        expected_list = [
            'team_1',
            'team_2',
            'cus_prof_1',
            'cus_prof_2'
        ]
        self.assertListEqual(images_list, expected_list)

    @mock.patch('utils.awss3_helper.BUCKET_IMG', MockBUCKET)
    def test_get_all_images_a3(self):
        keys_list = awss3_helper.get_all_images_a3()
        result = ['team_1', 'team_2', 'img1', 'img2', 'cus_prof_1', 'cus_prof_2']
        self.assertListEqual(keys_list, result)

    @mock.patch('utils.awss3_helper.BUCKET_IMG', MockBUCKET)
    def test_get_keys_to_delete(self):
        result = ['img1', 'img2']
        a3_images = awss3_helper.get_keys_to_delete()
        self.assertListEqual(a3_images, result)

    @mock.patch('utils.awss3_helper.BUCKET_IMG', MockBUCKET)
    def test_delete_images_awss3(self):
        keys_to_delete = awss3_helper.delete_images_awss3()
        result = ['img1', 'img2']
        self.assertListEqual(keys_to_delete, result)


class AwsPracticalAssignmentTestCase(TestCase):

    def setUp(self):
        user = CustomUser.objects.create(id=101,
                                         first_name="Jerry",
                                         last_name="Newbey",
                                         middle_name="Jr.",
                                         email='mail@mail.com',
                                         is_active=True)
        user.set_password('1Aa')
        user.save()

        self.factory = RequestFactory()
        self.request = self.factory.post('path',
                                         data=json.dumps({'file_key': 'key'}),
                                         content_type='application/json'
                                         )
        self.request.user = user
        self.request.FILES['curriculum_id'] = 1
        self.request.FILES['topic_id'] = 2
        self.request.FILES['item_id'] = 3

    def test_upload_positive(self):
        class response:
            key = 'key'

        self.request.FILES['file'] = StringIO()
        self.request.content_type = 'multipart/form-data'

        with mock.patch('utils.awss3_helper.BUCKET_TASKS') as mock_bucket:
            with mock.patch('utils.awss3_helper.file_validator') as mock_validator:
                mock_validator.return_value = True
                mock_bucket.put_object.return_value = response
                result = awss3_helper.AwsPracticalAssignment.upload(self.request)

                self.assertEqual(result['file_key'], 'key')

    def test_upload_object_exists(self):
        self.request.FILES['file'] = StringIO()
        self.request.content_type = 'multipart/form-data'

        with mock.patch('utils.awss3_helper.BOTO_S3') as mock_boto:
            with mock.patch('utils.awss3_helper.file_validator') as mock_validator:
                mock_validator.return_value = True
                mock_boto.Object.load.return_value = True
                result = awss3_helper.AwsPracticalAssignment.upload(self.request)

                self.assertFalse(result)

    def test_upload_negative_content_type(self):
        self.request.content_type = 'wrong/type'
        result = awss3_helper.AwsPracticalAssignment.upload(self.request)

        self.assertFalse(result)

    def test_upload_negative_file_for_upload(self):
        self.request.content_type = 'multipart/form-data'

        result = awss3_helper.AwsPracticalAssignment.upload(self.request)
        self.assertFalse(result)

    def test_upload_negative_validation(self):
        with mock.patch('utils.awss3_helper.file_validator') as mock_validator:
            self.request.content_type = 'multipart/form-data'
            self.request.FILES['file'] = StringIO()
            mock_validator.return_value = False

            result = awss3_helper.AwsPracticalAssignment.upload(self.request)
            self.assertFalse(result)

    def test_delete_positive(self):
        with mock.patch('utils.awss3_helper.BOTO_S3') as mock_boto:
            error_response = {'Error': {'Code': '500', 'Message': 'Error Get'}}
            mock_boto.Object.side_effect = ClientError(error_response, 'get_object')
            result = awss3_helper.AwsPracticalAssignment.delete(self.request)

            self.assertTrue(result)

    def test_delete_negative(self):
        with mock.patch('utils.awss3_helper.BOTO_S3') as mock_boto:
            mock_boto.Object.load.return_value = True
            result = awss3_helper.AwsPracticalAssignment.delete(self.request)

            self.assertFalse(result)

    def test_delete_not_content_type(self):
        request = self.factory.delete('path')
        request.content_type = 'wrong/type'
        result = awss3_helper.AwsPracticalAssignment.delete(request)

        self.assertFalse(result)

    def test_delete_not_key(self):
        request = self.factory.delete('path', data=json.dumps({'no_key':''}))
        request.content_type = 'application/json'
        result = awss3_helper.AwsPracticalAssignment.delete(request)

        self.assertFalse(result)
