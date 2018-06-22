"""
Views module
============
"""

import boto3
from eventually import settings
from django.views.generic.base import View
from django.http import JsonResponse
from utils.responsehelper import (RESPONSE_400_INVALID_DATA,
                                  RESPONSE_200_DELETED)
from utils import awss3_helper

BOTO_S3 = boto3.resource('s3',
                         aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)
BUCKET_TASKS = BOTO_S3.Bucket(settings.AWS_STORAGE_BUCKET_NAME_TASKS)
BUCKET_IMG = BOTO_S3.Bucket(settings.AWS_STORAGE_BUCKET_NAME_IMG)


class ImageManagement(View):
    """ View for handling upload and delete objects in the AmazonS3 bucket """

    def post(self, request):
        """
        Handles POST request to Amazon S3 bucket - eventually-photos.
        Accepts the following image extensions: *.gif, *.png, *.jpg, *.jpeg, *.bmp

        URL for GET requests: s3.eu-west-2.amazonaws.com/eventually-photos/<IMAGE KEY>
        Image key is a 32-symbol string. E.G.: "088858E477604992B3F5F6BBD478F616"

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

        :return: Status 200 and JsonResponse with random image name
                 Status 400 if bad request or image with such name already exists
        """
        image_key = awss3_helper.upload(request)
        if not image_key:
            return RESPONSE_400_INVALID_DATA
        return JsonResponse(image_key, status=200)

    def delete(self, request):
        """
        Handles DELETE request to Amazon S3 bucket - eventually-photos.

        :param request: request from the website
        :type request: application/json

        :return: status 200 if object has been deleted, otherwise - status 400
        """

        deleted = awss3_helper.delete(request)
        if not deleted:
            return RESPONSE_400_INVALID_DATA
        return RESPONSE_200_DELETED


class PracticalAssignmentManagement(View):
    """
    Handles practical assignments upload and delete from AWS S3.
    """

    def post(self, request):
        """
        Handles post request for PracticalAssignmentManagement.
        """
        file_key = awss3_helper.AWSPracticalAssignment.upload(request)
        if not file_key:
            return RESPONSE_400_INVALID_DATA
        return JsonResponse(file_key, status=200)

    def delete(self, request):
        """
        Handles delete request for PracticalAssignmentManagement.
        """
        deleted = awss3_helper.AWSPracticalAssignment.delete(request)
        if not deleted:
            return RESPONSE_400_INVALID_DATA
        return RESPONSE_200_DELETED
