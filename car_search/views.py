from django.shortcuts import render
from bs4 import BeautifulSoup
import requests


def index(request):
    return render(request, 'car_search/index.html')

def search(request):
    if request.method == 'POST':
        model = request.POST.get('model')
        year = request.POST.get('year')
        zipcode = request.POST.get('zipcode')
        distance = request.POST.get('distance')

        # Construct the URL with the year parameter
        website = f'https://www.cars.com/shopping/results/?stock_type=cpo&makes%5B%5D={model}&models%5B%5D=&list_price_max=&maximum_distance={distance}20&zip={zipcode}'
        if year:
            website += f'&year={year}'

        response = requests.get(website)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('div', {'class': 'vehicle-card'})

        cars = []
        for result in results:
            car = {}
            car['name'] = result.find('h2').get_text() if result.find('h2') else 'n/a'
            car['mileage'] = result.find('div', {'class': 'mileage'}).get_text() if result.find('div',
                                                                                                  {'class': 'mileage'}) else 'n/a'
            car['dealer_name'] = result.find('div', {'class': 'dealer-name'}).get_text().strip() if result.find('div',
                                                                                                                   {'class': 'dealer-name'}) else 'n/a'
            car['rating'] = result.find('span', {'class': 'sds-rating__count'}).get_text() if result.find('span',
                                                                                                           {'class': 'sds-rating__count'}) else 'n/a'
            car['review_count'] = result.find('span', {'class': 'sds-rating__link'}).get_text() if result.find(
                'span', {'class': 'sds-rating__link'}) else 'n/a'
            car['price'] = result.find('span', {'class': 'primary-price'}).get_text() if result.find('span',
                                                                                                       {'class': 'primary-price'}) else 'n/a'
            car['image'] = result.find('img')['data-src'] if result.find('img') and 'data-src' in result.find(
                'img').attrs else 'n/a'
            if car['image'] == 'n/a':
                car['image'] = result.find('img')['src'] if result.find('img') and 'src' in result.find(
                    'img').attrs else 'n/a'
            cars.append(car)

            print(car['name'])

        return render(request, 'car_search/results.html', {'cars': cars})

    return render(request, 'car_search/error.html', {'message': 'Invalid request method.'})
