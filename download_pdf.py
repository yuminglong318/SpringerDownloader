import requests
import json
import os

def download_pdf(title, url, dir):
    filename = os.path.join(dir, title)

    response = requests.get(url, stream=True)

    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

if __name__ == '__main__':


    # Article Downloading
    print('Downloading Articles')
    for dir in os.listdir('./article_list'):
        print(f"{dir}")
        subdir = os.path.join('./article_list', dir)
        for file in os.listdir(subdir):
            filepath = os.path.join(subdir, file)
            year = file.split('.')[0][-4:]
            dest_dir = os.path.join('./Articles', dir, year)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            with open(filepath, "r", encoding= "utf-8") as f:
                pdfs = json.load(f)
            
            print(year)
            for pdf in pdfs:
                
                progress = pdfs.index(pdf)
                total = len(pdfs)

                bar_width = 100
                filled_length = int(bar_width * progress / total)
                bar = '█' * filled_length + '-' * (bar_width - filled_length)

                download_pdf(pdf.get('title'), pdf.get('pdf_link'), dest_dir)
                print(f"\r Downloading {progress}/{total}: [{bar}]", end= '', flush= True)

            print("\n")
