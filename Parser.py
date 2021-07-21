from datetime import date

from bs4 import BeautifulSoup

from Car import Car


class CarfaxParser():
    def __init__(self):
        self.source = 'Carfax'

    def parse_page(self, page):
        soup = BeautifulSoup(page)
        return soup.find_all('div', {'class': 'srp-list-item'})

    def parse_item(self, item):
        """
        data i want to gather
        year
        """

        # basic details
        basic_info = item.find('h4', {'class': 'srp-list-item-basic-info-model'}
                               ).text.split(' ')
        year = basic_info[0]
        make = basic_info[1]
        model = basic_info[2]
        model_details = ' '.join(basic_info[3:])
        car = Car(make, model)
        car.year = year
        car.model_details = model_details
        car.used = True  # true for all carfax cars
        car.source = self.source

        # price
        price_text = item.find('span', {'class': 'srp-list-item-price'}).text
        price = int(price_text.split('$')[-1].replace(',', ''))
        car.price = price

        # date
        car.date = date.today().strftime('%m/%d/%Y')

        # dealer info
        dealer = item.find(
            'a', {'class': 'srp-list-item-dealership-name'}).contents[0].text.strip()
        dealer_location = item.find(
            'div', {'class': 'srp-list-item-dealership-location'}).contents[1].text.split('(')[0].strip()
        car.dealer = dealer
        car.dealer_location = dealer_location

        # mileage
        additional_details = item.find(
            'div', {'class': 'srp-list-item-special-features'})

        return additional_details.contents
