import io
import configparser
import gzip

from ftplib import FTP


class FtpClient:
    # Параметры конфига
    config = configparser.ConfigParser()
    config.read('config.ini')

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ftp = FTP(host)

    def connect(self):
        try:
            self.ftp.login(user=self.username, passwd=self.password)
            print("Connected to FTP server.")
        except Exception as e:
            print(f"Error connecting to FTP server: {e}")

    def get_files_from_last(self, type_of_edr: str) -> list:
        edr_to_parse = []
        """
        :param type_of_edr: какие типы CDR будем парсить
        :return: возвращает готовый список файлов, который нужно забрать с FTP и распарсить
        """
        try:
            self.ftp.cwd(self.config.get('FTP', 'cwd'))
            # Получаемся список файлов
            entries = list(self.ftp.nlst('-t'))
            entries.sort(reverse=True)

            for i in entries:
                if type_of_edr in i.split('-') and self.config.get('FTP', f'last_file_{type_of_edr}') != i:
                    edr_to_parse.append(i)
                elif self.config.get('FTP', f'last_file_{type_of_edr}') == i:
                    break
            return edr_to_parse
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    @staticmethod
    def gunzip_bytes_obj(bytes_obj):
        in_ = io.BytesIO()
        in_.write(bytes_obj)
        in_.seek(0)
        with gzip.GzipFile(fileobj=in_, mode='rb') as fo:
            gzipped_bytes_obj = fo.read()
        return gzipped_bytes_obj.decode(encoding='unicode-escape')

    def parse_file(self, list_of_files: list):
        r = io.BytesIO()

        try:
            for i in list_of_files:
                # Извлечение файла с ФТП в оперативку в битовом формате
                self.ftp.retrbinary('RETR ' + i, r.write)
                # Распаковка файла в оперативной памяти и разбиение его по знаку '\n'
                file = self.gunzip_bytes_obj(r.getvalue()).split('\n')
                for k in file:
                    print(k)
        except Exception as e:
            print(f"Error downloading file: {e}")

    def close(self):
        self.ftp.quit()
        print("Connection closed.")
