import psycopg2


class Postgres:
    __cursor = None
    __connection = None

    def __init__(self, host: str, database: str, username: str, password: str):
        self.host = host
        self.database = database
        self.username = username
        self.password = password

    def connect_to_db(self):
        try:
            self.__connection = psycopg2.connect(host=self.host, database=self.database,
                                                 user=self.username, password=self.password)
            self.__cursor = self.__connection.cursor()
            print("Connected to database.")
        except psycopg2.DatabaseError as e:
            print(f"Error connecting to database: {e}")

    def send_to_db(self):
        pass
