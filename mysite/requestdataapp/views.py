from django.http import HttpRequest, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render


def process_get_view(request: HttpRequest) -> HttpResponse:
    context = {

    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)


MAX_FILE_SIZE = 1024 * 1024


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == 'POST' and request.FILES.get("myfile"):
        myfile = request.FILES['myfile']
        if myfile.size > MAX_FILE_SIZE:
            context['error'] = "The file size exceeds the allowed limit of 1 MB"
        else:
            fs = FileSystemStorage()
            falename = fs.save(myfile.name, myfile)
            print("saved file", falename)
            context["message"] = "The file has been successfully uploaded"

    return render(request, 'requestdataapp/file-upload.html', context=context)
