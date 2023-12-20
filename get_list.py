import requests
from bs4 import BeautifulSoup
import json



domain = "https://link.springer.com"

for year in range(2020, 2024):
    download_list = []
    print(year)
    for page_number in range(1, 51):
        
        if page_number % 10 == 0:
            print(page_number)
        res = requests.get(
            f"https://link.springer.com/search/page/{page_number}?package=openaccess&date-facet-mode=in&facet-language=%22En%22&showAll=false&facet-end-year={year}&facet-start-year={year}&facet-discipline=%22Statistics%22&facet-content-type=%22Book%22"
        )
        if res.status_code != 200:
            print('failed', {page_number})
            continue

        soup = BeautifulSoup(res.text, 'html.parser')

        books = soup.find('ol', {'id': 'results-list'}).find_all('li')


        for book in books:
            try:
                title = book.find('h2').text.strip()
                link = f"{domain}{book.find('a', {'class': 'title'}).get('href')}" if book.find('a', {'class': 'title'}).get('href') else None

                if link:
                    response = requests.get(link)
                    if response.status_code == 200:
                        download_tags = BeautifulSoup(response.text, 'html.parser').find_all('div', {'class': 'c-pdf-download'})
                        for download_tag in download_tags:
                            pdf_link = download_tag.find('a').get('href')
                            if pdf_link.endswith('.pdf'):
                                download_list.append(
                                    {   
                                        'title': title,
                                        'pdf_link': f"{domain}{pdf_link}",
                                    }
                                )
                                break
            except Exception as e:
                print(e)

    with open(f'Statistics_Book_{year}.json', 'w', encoding= 'utf-8') as f:
        json.dump(download_list, f, indent= 4)