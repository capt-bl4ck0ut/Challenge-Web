import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django import forms
from PIL import Image, ImageMath
from django.conf import settings
from datetime import datetime

class UploadForm(forms.Form):
    files = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist('files')
            fs = FileSystemStorage()
            for file in uploaded_files:
                fs.save(file.name, file)
            return render(request, 'upload.html', {'success': True})
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form, 'success': False})

def process_images(request):
    image_paths = [f for f in os.listdir('uploads') if f != 'results']
    
    if request.method == 'POST':
        selected_images = request.POST.getlist('selected_images')
        expression = request.POST.get('expression', '')
        images = [Image.open(os.path.join('uploads', img)) for img in selected_images]

        if len(images) < 2:
            return render(request, 'select_images.html', {'error': "Select at least two images."})
        
        try:
            context = {os.path.splitext(img.filename)[0][8:]: img.convert('L') for img in images}
            result = ImageMath.eval(expression, **context)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')
            output_path = f'result_{timestamp}.png'
            result.save(os.path.join(settings.MEDIA_ROOT, 'results', output_path))
            return render(request, 'select_images.html', {'image_paths': image_paths, 'success': True, 'output_image': output_path})
        except Exception as e:
            return render(request, 'select_images.html', {'error': 'We apologize for the inconvenience. Please report this error message to the administrator.\n\nError: ' + str(e), 'image_paths': selected_images})
    
    return render(request, 'select_images.html', {'image_paths': image_paths, 'error': None})
    
def serve_file(request, file_path):
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(full_path):
        with open(full_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='image/png')
    return HttpResponse("File not found.", status=404)

def gallery(request):
    images = os.listdir('uploads/results')
    return render(request, 'gallery.html', {'images': images})