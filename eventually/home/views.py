"""  Generate index html page """

from django.http import HttpResponse
from django.template import loader


def index(request):  # pylint: disable=unused-argument
    """Send index.html page on GET request"""
    template = loader.get_template('index.html')
    return HttpResponse(template.render(), content_type='text/html')
