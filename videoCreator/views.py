from mimetypes import guess_type
import os
import base64
import django_heroku


from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http.request import HttpRequest
from django.shortcuts import redirect

from .video  import render_video
from .forms import UploadFaceForm, CropFaceForm
from .models import VideoTemplate, FaceInsert

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def video_create(request, id, fps=60):
    """
    Calls function to render video and returns path to it.
    :param id: ID of face insert instance
    :param fps: frames per second of
    :return: video
    """
    videofile = render_video(id, fps=60)
    video_path = os.path.join(BASE_DIR, videofile)

    with open(video_path, 'rb') as f:
        response = HttpResponse(f, content_type='video/mp4')
        response['Content-Length'] = len(response.content)
        response['Content-Disposition'] = 'attachment; filename=export-face.mp4'
        return response


def image_upload(request):
    if request.method == 'POST':
        form = UploadFaceForm(request.POST, request.FILES)
        if form.is_valid():
            template = VideoTemplate.objects.get(id="1")

            insert = FaceInsert(template=template)
            insert.save()
            id = insert.id

            data = request.FILES['face']
            filename = 'original-img_{}'.format(id)
            tmp_path = 'faces/{}.png'.format(filename)
            path = default_storage.save(tmp_path, ContentFile(data.read()))

            django_heroku.settings(locals())
            is_production = os.environ['PRODUCTION']
            host = HttpRequest.get_host(request)
            if is_production:
                redirect_url = 'https://{}/create/crop/{}'.format(host, id)
            else:
                redirect_url = 'http://{}/create/crop/{}'.format(host, id)
            return redirect(redirect_url)

    uploadfaceform = UploadFaceForm()
    return render(request, 'videoCreator/image_upload.html', {'UploadFaceForm': uploadfaceform})


def image_crop(request, id):
    django_heroku.settings(locals())
    is_production = os.environ['PRODUCTION']
    if request.method == 'POST':
        form = CropFaceForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data['imagefield']
            formatinfo, imgstring = data.split(';base64,')
            ext = formatinfo.split('/')[-1]

            image = ContentFile(base64.b64decode(imgstring), name='temp.' + ext)
            filename = 'cropped-img_{}'.format(id)
            tmp_path = 'faces/{}.png'.format(filename)
            path = default_storage.save(tmp_path, image)

            host = HttpRequest.get_host(request)
            if is_production:
                redirect_url = 'https://{}/create/create/{}'.format(host, id)
            else:
                redirect_url = 'http://{}/create/create/{}'.format(host, id)
            return redirect(redirect_url)

    filename = 'original-img_{}'.format(id)
    host = HttpRequest.get_host(request)
    if is_production:
        path = 'https://{}/media/faces/{}.png'.format(host, filename)
    else:
        path = 'http://{}/media/faces/{}.png'.format(host, filename)
    # path = os.path.join(BASE_DIR, tmp_path)

    return render(request, 'videoCreator/image_crop.html', {'imgsrc': path, 'id': id})

