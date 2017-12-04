"""
Views module
============
"""

import json
import uuid
import boto3
from eventually import settings
from botocore.exceptions import ClientError
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
from utils.validators import image_validator

BOTO_S3 = boto3.resource('s3',
                         aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)
BUCKET = BOTO_S3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

class ImageManagement(View):
    """ View for handling upload and delete objects in the AmazonS3 bucket """

    def post(self, request):
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

        :return: Status 200 and JsonResponse with random image name
                 Status 400 if bad request
                 Status 409 if image already exists
        """

        if request.content_type != 'multipart/form-data':
            return HttpResponse(status=400)

        image_for_upload = request.FILES.get('image')
        if not image_for_upload:
            return HttpResponse(status=400)

        image_extension = image_validator(image_for_upload)
        if not image_validator(image_for_upload):
            return HttpResponse(status=400)
        else: mime_type = 'image/' + image_extension

        image_acl = "public-read"
        image_key = str(uuid.uuid4()).replace('-', '').upper()

        try:
            BOTO_S3.Object(settings.AWS_STORAGE_BUCKET_NAME, image_key).load()
        except ClientError:
            response = BUCKET.put_object(ACL=image_acl,
                                         Body=image_for_upload.read(),
                                         ContentType=mime_type,
                                         Key=image_key)
            return JsonResponse({"image_key": response.key}, status=200)
        else:
            return HttpResponse(status=409)


    def delete(self, request):
        """
        Handles delete image from bucket request

        :param request: request from the website
        :type request: application/json

        :return: status 200 if object has been deleted, otherwise - status 400
        """

        if request.content_type != 'application/json':
            return HttpResponse(status=400)

        image_to_delete = json.loads(request.body)
        if not image_to_delete.get("image_key"):
            return HttpResponse(status=400)

        delete_obj = {"Key": image_to_delete.get("image_key")}
        BUCKET.delete_objects(Delete={"Objects":[delete_obj]})

        try:
            BOTO_S3.Object(settings.AWS_STORAGE_BUCKET_NAME,
                           image_to_delete.get("image_key")).load()
        except ClientError:
            return HttpResponse(status=200)

        return HttpResponse(status=400)
