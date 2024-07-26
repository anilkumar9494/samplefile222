import os
from django.http import HttpResponse
from django.conf import settings

def android_file(request):
    image_path = os.path.join(settings.BASE_DIR, 'metatrader4.apk.1')
    with open(image_path, 'rb') as f:
        image = f.read()
    return HttpResponse(image, content_type="/png")