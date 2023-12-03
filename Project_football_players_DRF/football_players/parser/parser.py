import requests
from bs4 import BeautifulSoup
from datetime import datetime
import psycopg2
import pandas

class Parser:
    db_name = 'football_players'
    user = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = '5432'
    base_url = 'https://www.transfermarkt.com'
    extra_url = '/uefa-champions-league/torschuetzenliste/pokalwettbewerb/CL/ajax/yw1/saison_id/gesamt/plus/0/galerie/0'

    @staticmethod
    def get_player_by_link(base_url, extra_url):
        rating = []
        flag = True
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0'}
        while flag:
            response = requests.get(base_url+extra_url, headers=headers)
            html = response.text

            html_rating = BeautifulSoup(html, 'html.parser')
            next_page = html_rating.find('a', title='Go to the next page')

            if next_page != None:
                extra_url = next_page.attrs['href']
            else:
                flag = False

            players = html_rating.find('table', class_='items').find_all('td', class_=['hauptlink', 'zentriert', 'zentriert hauptlink'])
            for player in players:
                player_description = player.text.replace('\n', '')
                rating.append(player_description)

        ratings = [tuple(rating[i:i+7]) for i in range(0, len(rating), 7)]
        return ratings

    def create_connection(self):  # подключение к БД
        connection = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )
        return connection

    def create_player_table(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("""
            TRUNCATE TABLE players_player
            """
            )
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS players_player
                    (
                        id serial PRIMARY KEY,
                        football_player_name text,
                        nationality text,
                        age integer,
                        count_of_club text,
                        matches integer,
                        goals integer
                    )
    
                """
            )
            connection.commit()
            print("Table created successfully")

########################################################################################
    def insert(self, connection, ratings):
        cursor = connection.cursor()
        symbol = "'"
        for rating in ratings:
            if symbol not in rating[1]:
                cursor.execute(f"INSERT INTO players_player (id, football_player_name, age, count_of_club, matches, goals)"
                               f" VALUES ({int(rating[0])}, '{rating[1]}',  {int(rating[3])},"
                               f" '{rating[4]}', {int(rating[5])}, {int(rating[6])})")
            elif symbol in rating[1]:
                rate = rating[1].replace("'", "^")
                cursor.execute(f"INSERT INTO players_player (id, football_player_name, age, count_of_club, matches, goals)"
                               f" VALUES ({int(rating[0])}, '{rate}',  {int(rating[3])},"
                               f" '{rating[4]}', {int(rating[5])}, {int(rating[6])})")
        connection.commit()


    def save_to_postgres(self, ratings):
        connection = self.create_connection()
        self.create_player_table(connection)
        self.insert(connection, ratings)


    def write_csv(self, ratings):
        for i in range(0, len(ratings)):
            pandas.DataFrame(ratings).to_csv('best_scorers_of_champions_league.csv', index=False)

    def run(self):
        begin_time = datetime.now()
        player_items = self.get_player_by_link(Parser.base_url, Parser.extra_url)
        print(player_items)
        connection = self.create_connection()
        self.create_player_table(connection)
        self.insert(connection, player_items)
        self.save_to_postgres(player_items)
        self.write_csv(player_items)
        end_time = datetime.now()
        execute_time = end_time - begin_time
        print(f"Время получения данных {execute_time}")

Parser().run()


