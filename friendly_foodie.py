import re, requests, bs4, time
from pathlib import Path
import pyinputplus as pyip
from datetime import datetime

restaurants = []
calculation_factors = {'price': 1.0/3.0, 'stars': 2.0/15.0, 'affinity': 6.0/15.0, 'recency': 2.0/15.0}

class Restaurant:
    def __init__(self, name, price, stars, affinity, recency, link):
        self.name = name # name of the restaurant
        self.price = price # price on Yelp
        self.stars = stars # number of stars on Yelp
        self.affinity = affinity # personal enjoyment of the restaurant
        self.recency = recency # last time I went to the restaurant
        self.link = link # last part of the Yelp URL

def load_file():
    foodie_file_path = Path('foodie.txt')
    if foodie_file_path.is_file():
        foodie_text = open(foodie_file_path).readlines()
        for i in range(len(foodie_text)):
            # Read a line of the local foodie file
            restaurant_info = re.findall((r'[^*]*'), foodie_text[i])
            # Remove empty strings from array
            for j in range(6):
                restaurant_info.remove('')
            # Remove the \n character from the link
            restaurant_info[5] = restaurant_info[5].replace('\n', '')
            restaurants.clear()
            fill_list(restaurant_info[0], float(len(restaurant_info[1])), float(restaurant_info[2]), float(restaurant_info[3]), datetime.strptime(restaurant_info[4], '%d/%m/%Y'), restaurant_info[5])
    else:
        print('No existing "foodie.txt" file was found in the local folder.')

def fill_list(name, price, stars, affinity, recency, link):
    restaurants.clear()
    restaurants.append(Restaurant(name, price, stars, affinity, recency, link))

def calculate_restaurant():
    if restaurants:
        restaurant_sums = []
        
    else:
        print('Failed. No Foodie file has been loaded into the program.')
        time.sleep(2)

def new_file(seed_file):
    seed_file = open(Path(seed_file)) # file used to seed the program

    seed_text = seed_file.readlines()

    # clear program file
    program_file = open('foodie.txt', 'w')
    program_file.write('')
    program_file.close()
        
    program_file = open('foodie.txt', 'a')

    for x in range(len(seed_text)):
        seed_name_regex = re.compile(r'(\S)*')
        seed_name = (seed_name_regex.search(seed_text[x])).group()
        
        seed_affinity_regex = re.compile(r'\s\d([.]\d)?')
        seed_affinity_regex = re.compile(r'\d([.]\d)?')
        seed_affinity = (seed_affinity_regex.search(seed_text[x])).group()

        seed_recency_regex = re.compile(r'\d\d/\d\d/\d\d\d\d')
        seed_recency = (seed_recency_regex.search(seed_text[x])).group()

        res = requests.get("https://www.yelp.ca/biz/" + seed_name)

        try:
            res.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))

        place_soup = bs4.BeautifulSoup(res.text, 'html.parser')

        place_name = place_soup.select('body > yelp-react-root > div:nth-child(1) > div.photoHeader__09f24__nPvHp.border-color--default__09f24__NPAKY > div.photo-header-content-container__09f24__jDLBB.border-color--default__09f24__NPAKY > div.photo-header-content__09f24__q7rNO.padding-r2__09f24__ByXi4.border-color--default__09f24__NPAKY > div > div > div.headingLight__09f24__N86u1.margin-b1__09f24__vaLrm.border-color--default__09f24__NPAKY > h1')
        name = place_name[0].getText()

        place_stars = place_soup.select('body > yelp-react-root > div:nth-child(1) > div.photoHeader__09f24__nPvHp.border-color--default__09f24__NPAKY > div.photo-header-content-container__09f24__jDLBB.border-color--default__09f24__NPAKY > div.photo-header-content__09f24__q7rNO.padding-r2__09f24__ByXi4.border-color--default__09f24__NPAKY > div > div > div.arrange__09f24__LDfbs.gutter-1-5__09f24__vMtpw.vertical-align-middle__09f24__zU9sE.margin-b2__09f24__CEMjT.border-color--default__09f24__NPAKY > div:nth-child(1) > span > div')
        star_rating_regex = re.compile(r'\d(.\d)? star rating')
        stars = (star_rating_regex.search(str(place_stars[0]))).group()
        star_rating_regex = re.compile(r'\d(.\d)?')
        stars = (star_rating_regex.search(str(place_stars[0]))).group()

        place_price = place_soup.select('body > yelp-react-root > div:nth-child(1) > div.photoHeader__09f24__nPvHp.border-color--default__09f24__NPAKY > div.photo-header-content-container__09f24__jDLBB.border-color--default__09f24__NPAKY > div.photo-header-content__09f24__q7rNO.padding-r2__09f24__ByXi4.border-color--default__09f24__NPAKY > div > div > span:nth-child(4) > span')
        price = place_price[0].getText().strip()

        program_file.write(name + '*' + price + '*' + stars + '*' + seed_affinity + '*' + seed_recency + '*' + seed_name + '\n')

        fill_list(name, float(len(price)), float(stars), float(seed_affinity), datetime.strptime(seed_recency, '%d/%m/%Y'), seed_name)

    program_file.close()

while True:
    choice = 0
    print('Fellow Foodie'.center(50, '-'))
    print('1 - Calculate a Restaurant Recommendation')
    print('2 - New Foodie File from Seed')
    print('3 - Update Foodie File with Online Information')
    print('4 - Exit')
    load_file()
    choice = pyip.inputNum('Please select from the above menu options: ', min=1, max=4)
    match choice:
        case 1:
            print('New restaurant!')
        case 2:
            seed_file = ''
            # Continue asking for the seed file name if the seed file does not exist
            while True:
                seed_file = pyip.inputStr('Enter the name of the .txt seed file: ')
                if '.txt' not in seed_file:
                    seed_file += '.txt'
                if Path(seed_file).is_file():
                    break
                else:
                    print(f'A seed file with the name "{seed_file}" was not found in the local folder. Please enter the name of a valid file.')
                    time.sleep(2)
            print('Processing...')
            new_file(seed_file)
            print('Success! New Foodie file created.\n')
            time.sleep(2)
        case 3:
            print('Update!\n')
        case 4:
            print('Thank you for using Fellow Foodie!')
            break
        case _:
            print('You have made an invalid selection. Please try again.')
            time.sleep(2)

