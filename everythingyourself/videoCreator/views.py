from mimetypes import guess_type
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .video  import render_video
from .forms import UploadFaceForm

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_video(request):
    if request.method == 'POST':
        form = UploadFaceForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['face']
            filename = 'face'
            tmp_path = 'faces/{}.png'.format(filename)
            path = default_storage.save(tmp_path, ContentFile(data.read()))

            id="2x3"
            videofile = render_video(id, fps=60)

            with open(videofile, 'rb') as f:
                response = HttpResponse(f, content_type=guess_type(videofile)[0])
                response['Content-Length'] = len(response.content)
                return response

    uploadfaceform = UploadFaceForm()
    return render(request, 'videoCreator/create_video.html', {'UploadFaceForm': uploadfaceform})
