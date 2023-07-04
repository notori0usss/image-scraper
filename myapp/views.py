from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import urllib.parse
import zipfile
import io

def home(request):
    if request.method == 'POST':
        url = request.POST.get("url")
        req = requests.get(url)
        response = req.text
        soup = BeautifulSoup(response, "html.parser")
        img = soup.find_all("img")
        images = []
        for i in img:
            src = i['src']
            if not urllib.parse.urlparse(src).scheme:
                # If the scheme is missing, assume it's a relative URL and add the default scheme
                src = urllib.parse.urljoin(url, src)
            images.append(src)

        batch_size = 10  # Number of files per ZIP
        num_batches = len(images) // batch_size + 1

        zip_files = []
        for i in range(num_batches):
            start_index = i * batch_size
            end_index = (i + 1) * batch_size
            batch_images = images[start_index:end_index]

            zip_file_path = f'images_batch{i + 1}.zip'
            zip_data = io.BytesIO()

            with zipfile.ZipFile(zip_data, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for image in batch_images:
                    image_data = requests.get(image).content
                    zipf.writestr(image.split('/')[-1], image_data)

            zip_data.seek(0)
            zip_files.append({'name': zip_file_path, 'data': zip_data.getvalue()})

        return render(request, 'myapp/index.html', {'zip_files': zip_files})

    return render(request, 'myapp/index.html')
