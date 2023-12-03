# pip install psycopg2
import psycopg2  # это адаптер базы данных PostgreSQL для Python
from sqlite3 import Error
from abc import ABC, abstractmethod


class DataClient(ABC):
    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def create_player_table(self, conn):
        pass

    @abstractmethod
    def get_items(self, conn, goals_from=0, goals_to=10000):
        pass

    @abstractmethod
    def insert(self, conn, football_player_name, nationality, age, count_of_club, matches, goals):
        pass

    def run_test(self):
        conn = self.get_connection()
        self.create_player_table(conn)
        # items = self.get_items(conn, goals_from=10, goals_to=30)
        # for item in items:  # откорректировать
        #     print(item)  # откорректировать
        conn.close()


class PostgresClient(DataClient):
    DB_NAME = 'football_players'
    USER = 'postgres'
    PASSWORD = 'postgres'
    HOST = 'localhost'
    PORT = '5432'

    def get_connection(self):   # подключение к БД
        try:
            connection = psycopg2.connect(
                database=self.DB_NAME,
                user=self.USER,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT,
            )
            return connection
        except Error:
            print(Error)

    def create_player_table(self, conn):
        cursor_object = conn.cursor()
        cursor_object.execute(
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
        conn.commit()

    def get_items(self, conn, goals_from=0, goals_to=200):
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM players_player WHERE goals >= {goals_from} and goals <= {goals_to}')
        return cursor.fetchall()  # fetchall() возвращает результаты запроса в виде списка кортежей, в котором каждый
    # кортеж содержит одну строку данных из результатов запроса

    def insert(self, conn, football_player_name, nationality, age, count_of_club, matches, goals):
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO players_player (football_player_name, nationality, age, count_of_club, matches, goals)"
                       f" VALUES ('{football_player_name}', '{nationality}', '{age}', '{count_of_club}', '{matches}', '{goals}')")
        conn.commit()


data_client = PostgresClient()

