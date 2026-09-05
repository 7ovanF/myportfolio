from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse

def landing_page(request):
    return render(request, "index.html")

def favicon(request):
    file = (settings.BASE_DIR / "favicon.ico").open("rb")
    return FileResponse(file)
