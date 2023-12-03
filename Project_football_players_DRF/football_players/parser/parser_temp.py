import csv
import re
import pandas
import requests
from bs4 import BeautifulSoup
from datetime import datetime
#import data_client

base_url = 'https://www.transfermarkt.com'
extra_url = '/uefa-champions-league/torschuetzenliste/pokalwettbewerb/CL/ajax/yw1/saison_id/gesamt/plus/0/galerie/0'
rating = []
flag = True
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0'}


def write_csv(ratings):
    for i in range(0, len(ratings)):
        pandas.DataFrame(ratings).to_csv('best_scorers_of_champions_league.csv', index=False)

while flag:
    response = requests.get(base_url+extra_url, headers=headers)
    html = response.text

    html_rating = BeautifulSoup(html, 'html.parser')
    next_page = html_rating.find('a', title='Go to next page')

    if next_page != None:
        extra_url = next_page.attrs['href']
    else:
        flag = False

    players = html_rating.find('table', class_='items').find_all('td', class_=['hauptlink', 'zentriert', 'zentriert hauptlink'])
    for player in players:
        player_description = player.text.replace('\n', '')
        rating.append(player_description)

ratings = [rating[i:i+7] for i in range(0, len(rating), 7)]
print(ratings)
print(len(ratings))
write_csv(ratings)

#####################################################################################
#####################################################################################
# def get_html(url):
#     r = requests.get(url)   # response
#     return r.text           # возвращает HTML-код страницы (url)
#
# def get_all_links(html):
#     soup = BeautifulSoup(html, 'lxml')  # lxml — это библиотека Python для работы с XML и HTML документами.
#     tds = soup.find('div', class_='sc-37735160-0 eedPba cmc-table--sort-by__rank cmc-table').find_all('a', class_='cmc-table__column-name--symbol cmc-link')  #???????
#     links = []
#     for td in tds:
#         a = td['href']                # string
#         link = 'https://coinmarketcap.com' + a      # /currencies/bitcoin/
#         links.append(link)
#     return links
#
# def get_page_data(html):
#     soup = BeautifulSoup(html, 'lxml')
#     try:
#         name = soup.find('span', class_='coin-name-pc').text.strip()
#     except:
#         name = ''
#
#     try:
#         price = soup.find('span', class_='sc-f70bb44c-0 jxpCgO base-text').text.strip()
#     except:
#         price = ''
#
#     try:
#        market_cap = soup.find('p', class_='sc-4984dd93-0 sc-83eb68a9-1 kyUSRS').text.strip()
#     except:
#         market_cap = ''
#
#     try:
#         volume = soup.find('p', class_='sc-4984dd93-0 sc-83eb68a9-1 dvnslc').text.strip()
#     except:
#         volume = ''
#
#     try:
#         volume_market_cap = soup.find('dd', class_='sc-f70bb44c-0 bCgkcs base-text').text.strip()  # удаляет только пробельные символы в начале и конце строки
#     except:
#         volume_market_cap = ''
#
#     try:
#         circulating_supply = soup.find('dd', class_='sc-f70bb44c-0 bCgkcs base-text').text.strip()
#     except:
#         circulating_supply = ''
#
#     data = {'name': name, 'price': price, 'market_cap': market_cap, 'volume': volume,
#             'volume_market_cap': volume_market_cap, 'circulating_supply': circulating_supply}
#     return data
#
# def write_csv(data):
#     with open('coinmarketcap.csv', 'a') as f:
#         writer = csv.writer(f)
#         writer.writerow((data['name'], data['price'], data['market_cap'], data['volume'], data['market_cap'],
#                          data['volume_market_cap'], data['circulating_supply']))
#         print(data['name'], 'parsed')
#
# def make_all(url):
#     html = get_html(url)
#     data = get_page_data(html)
#     write_csv(data)
#
# def main():
#     start = datetime.now()
#     url = 'https://coinmarketcap.com/all/views/all/'
#     all_links = get_all_links(get_html(url))
#
#     # for index, url in enumerate(all_links):
#     #     html = get_html(url)
#     #     data = get_page_data(html)
#     #     write_csv(data)
#     #     print(index)
#
#     with Pool(40) as p:
#         p.map(make_all, all_links)
#     end = datetime.now()
#     total = end - start
#     print(str(total))
#
# if __name__ == '__main__':
#     main()

#####################################################################################
#####################################################################################

# def parser_coin():
#     response = requests.get('https://coinmarketcap.com/')
#     soup = BeautifulSoup(response.text, 'html.parser')
#     data = soup.find_all('div', {'class': 'sc-a0353bbc-0 gDrtaY'})
#     coin_data = []
#     for elem in data:
#         el = elem.text.replace('$', '')
#         coin_data.append(el.replace(',', ''))
#     for i in range(len(coin_data)):
#         coin_data[i] = float(coin_data[i])
#     return coin_data
#
# if __name__ == '__main__':
#     print('Bitcoin value is ', parser_coin())

#########################################################################################
#########################################################################################

# class Parser:
#     links_to_parse = [
#         'https://coinmarketcap.com/'
#     ]
#
#     #data_client_imp = data_client.PostgresClient  # применение полиморфизма
#
#     @staticmethod
#     def get_player_by_link(link):
#         response = requests.get(link)
#         player_data = response.text  # откорректировать
#         player_items = []  # откорректировать
#         to_parse = BeautifulSoup(player_data, 'html.parser')  # откорректировать
#         for elem in to_parse.find_all(class_=re.compile("aef7b723")):  # откорректировать
#             price, description = elem.text.split('р.')  # откорректировать
#             player_items.append(
#                 (elem['href'],  # откорректировать
#                  int(price.replace(' ', '')),  # откорректировать
#                  description  # откорректировать
#                  ))
#
#         return player_items  # откорректировать
#
#     # def save_to_postgres(self, player_items):  # откорректировать
#     #     connection = self.data_client_imp.get_connection()   # применение полиморфизма
#     #     self.data_client_imp.create_player_table(connection)  # откорректировать
#     #     for item in player_items:  # откорректировать
#     #         self.data_client_imp.insert(connection, item[0], item[1], item[2])  # откорректировать
#
#     def run(self):
#         player_items = []  # откорректировать
#         for link in Parser.links_to_parse:
#             player_items.extend(self.get_player_by_link(link))  # откорректировать
#             #self.save_to_postgres(player_items)  # откорректировать
#
# Parser().run()
