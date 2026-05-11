from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .image_classifier import classify

def test(request):
    return render(request, "test.html")

def classify_test(request):
    return render(request, "interface.html", {
        "model_name": request.session.get("model_name"),
    })

def upload_image(request):
    image_url = None
    image_name = None
    outcome = None
    model_name = request.session.get("model_name")
    model_path = request.session.get("model_path")

    if request.method == "POST":
        if request.FILES.get("model"):
            uploaded_model = request.FILES["model"]
            model_upload_root = settings.MEDIA_ROOT / "models"
            os.makedirs(model_upload_root, exist_ok=True)
            model_storage = FileSystemStorage(location=model_upload_root)
            model_filename = model_storage.save(uploaded_model.name, uploaded_model)
            model_path = model_storage.path(model_filename)
            model_name = os.path.basename(model_filename)
            request.session["model_path"] = model_path
            request.session["model_name"] = model_name

        if request.FILES.get("image"):
            uploaded_file = request.FILES["image"]

            fs = FileSystemStorage()
            filename  = fs.save(uploaded_file.name, uploaded_file)

            image_path = fs.path(filename)
            image_url = fs.url(filename )
            image_name = os.path.basename(filename )

            outcome = classify(image_path, model_path)

    context = {
        "image_url": image_url,
        "image_name": image_name,
        "outcome": outcome,
        "model_name": model_name,
    }

    return render(request, "interface.html", context)
