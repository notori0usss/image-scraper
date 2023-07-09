import io
import urllib.parse
import zipfile

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

from myapp.models import File

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}


def home(request):
    if request.method == 'POST':
        url = request.POST.get("url")
        req = requests.get(url, headers=headers)
        response = req.text
        soup = BeautifulSoup(response, "html.parser")

        img = soup.find_all("img")[:30]
        images = []
        for i, img_tag in enumerate(img, start=1):
            src = img_tag['src']
            if not urllib.parse.urlparse(src).scheme:
                src = urllib.parse.urljoin(url, src)
            images.append((src, i))

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for image_url, index in images:
                image_req = requests.get(image_url)
                image_data = image_req.content
                image_filename = image_url.split('/')[-1]
                if images.count((image_url, index)) > 1:
                    # Add the index to the filename to make it unique
                    image_filename = f"{image_filename.split('.')[0]}_{index}.{image_filename.split('.')[-1]}"
                zip_file.writestr(image_filename, image_data)

        # Save the zip file to the database
        if images.__len__() <= 0:
            context = {
                'error': True
            }
            return render(request, 'myapp/index.html', context)
        else:
            file_instance = File()
            file_instance.docfile.save('images.zip', zip_buffer)
            file_instance.save()
            context = {
                'zip_file': file_instance,
            }
            return render(request, 'myapp/index.html', context)

    return render(request, 'myapp/index.html')
