"""
File Handler
============
Provides methods for upload and download processes of the object to Amazon S3 service
"""

import json
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from utils.utils import LOGGER
from utils.validators import image_validator, file_validator
from customprofile.models import CustomProfile
from eventually import settings
from team.models import Team


BOTO_S3 = boto3.resource('s3',
                         aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)
BUCKET_IMG = BOTO_S3.Bucket(settings.AWS_STORAGE_BUCKET_NAME_IMG)
BUCKET_TASKS = BOTO_S3.Bucket(settings.AWS_STORAGE_BUCKET_NAME_TASKS)


def _get_all_img_keys():
    """
    Collects keys of all images stored in database
    :return: list of keys of all images from database stored in amazons3
    """

    images_list = []
    teams_querysets = Team.get_all()
    for team in teams_querysets:
        if team.image:
            images_list.append(team.image)

    customprofile_querysets = CustomProfile.get_all()
    for profile in customprofile_querysets:
        if profile.photo:
            images_list.append(profile.photo)

    return images_list


def upload(request):
    """
    Handles upload to Amazon S3 bucket eventually-photos.
    URL for requests: s3.eu-west-2.amazonaws.com/eventually-photos/
    Accepts the following image extensions: *.gif, *.png, *.jpg, *.jpeg, *.bmp
    :param request: request from the web page
    :type request: multipart/form-data
    :Example:
    |   POST /s3.eu-west-2.amazonaws.com/eventually-photos/ HTTP/1.1
    |   Host: localhost:8000
    |   Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
    |   ------WebKitFormBoundary7MA4YWxkTrZu0gW
    |   Content-Disposition: form-data; name="image"; filename="IMG_20171129.jpg"
    |   Content-Type: image/jpeg
    |   ------WebKitFormBoundary7MA4YWxkTrZu0gW--
    :return: True if image has been uploaded successfully
             False if image hasn't been uploaded
    """

    if request.content_type != 'multipart/form-data':
        return False

    image_for_upload = request.FILES.get('image')
    if not image_for_upload:
        return False

    image_extension = image_validator(image_for_upload)
    if not image_extension:
        return False
    else:
        mime_type = 'image/' + image_extension

    image_acl = "public-read"
    image_key = str(uuid.uuid4()).replace('-', '').upper()
    try:
        BOTO_S3.Object(settings.AWS_STORAGE_BUCKET_NAME_IMG, image_key).load()
    except ClientError:
        response = BUCKET_IMG.put_object(ACL=image_acl,
                                         Body=image_for_upload.read(),
                                         ContentType=mime_type,
                                         Key=image_key)
        return {"image_key": response.key}
    else:
        return False


def delete(request):
    """
    Handles delete image from bucket request
    :param request: request from the website
    :type request: application/json
    :return: True if object has been deleted, otherwise - False
    """

    if request.content_type != 'application/json':
        return False

    image_to_delete = json.loads(request.body)
    if not image_to_delete.get("image_key"):
        return False

    return delete_by_image_key(image_to_delete.get("image_key"))

def delete_by_image_key(image_key):
    """
    Handles delete image from bucket request

    :param image_key: image_key in aws3
    :type image_key: str

    :return: True if object has been deleted, otherwise - False
    """

    delete_obj = {"Key": image_key}
    BUCKET_IMG.delete_objects(Delete={"Objects":[delete_obj]})

    try:
        BOTO_S3.Object(settings.AWS_STORAGE_BUCKET_NAME_IMG,
                       image_key).load()
    except ClientError as err:
        LOGGER.error(f'Image key {image_key} does not exist. {err}')
        return True
    return False


def get_all_images_a3():
    """
    Collects keys of all images stored on amazons3 bucket.
    :return: list of strings with keys of images stored on amazons3
    """

    bucket_objects = BUCKET_IMG.meta.client.list_objects(Bucket=BUCKET_IMG.name)
    keys_list = []
    for image in bucket_objects['Contents']:
        keys_list.append(image['Key'])
    return keys_list


def get_keys_to_delete():
    """
    Compares lists of image keys from amazons3 and database, returns list of keys which are
    not in database.
    :return: list of strings with keys of images stored on amazons3, but not in database
    """

    a3_images = get_all_images_a3()
    pg_images = _get_all_img_keys()
    for image in pg_images:
        a3_images.remove(image)
    return a3_images


def delete_images_awss3():
    """
    deletes images by keys from amazons3
    :return: list with keys of deleted images from amazons3
    """

    keys_to_delete = get_keys_to_delete()[0:2]
    objects_to_del = []
    for key in keys_to_delete:
        delete_obj = {"Key": key}
        objects_to_del.append(delete_obj)
    if objects_to_del:
        dict_keys_del = {'Objects': objects_to_del}
        BUCKET_IMG.delete_objects(Delete=dict_keys_del)
        return keys_to_delete


class AWSPracticalAssignment:
    """
    Handles practical tasks upload and delete from AWS S3 service.
    """
    @staticmethod
    def upload(request):
        """
        Uploads file to AWS S3 service.
        :param request: request from the website
        :type request: application/json
        :return: dict or False
        """
        if request.content_type != 'multipart/form-data':
            return False

        file_for_upload = request.FILES.get('file')

        if not file_for_upload:
            return False

        if not file_validator(file_for_upload):
            return False

        curriculum = str(request.POST.get('curriculum_id'))
        topic = str(request.POST.get('topic_id'))
        item = str(request.POST.get('item_id'))
        name_date = (str(request.user.email) + str(datetime.now())).replace(' ', '_')

        file_key = '/'.join([curriculum, topic, item, name_date])
        file_acl = "public-read"

        try:
            BOTO_S3.Object(settings.AWS_STORAGE_BUCKET_NAME_TASKS, file_key).load()
        except ClientError:
            response = BUCKET_TASKS.put_object(ACL=file_acl,
                                               Body=file_for_upload.read(),
                                               Key=file_key)
            return {"file_key": response.key}
        else:
            return False

    @staticmethod
    def delete(request):
        """
        Handles delete file from bucket request
        :param request: request from the website
        :type request: application/json
        :return: status 200 if object has been deleted, otherwise - status 400
        """

        if request.content_type != 'application/json':
            return False

        file_to_delete = json.loads(request.body)
        key = file_to_delete.get("file_key")
        if not key:
            return False

        delete_obj = {"Key": key}
        BUCKET_TASKS.delete_objects(Delete={"Objects": [delete_obj]})

        try:
            BOTO_S3.Object(settings.AWS_STORAGE_BUCKET_NAME_TASKS,
                           file_to_delete.get("file_key")).load()
        except ClientError:
            return True
        return False
