import configparser
import ftp_class


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    ftp = ftp_class.FtpClient(host=config['FTP']['IP'],
                              username=config['FTP']['login'],
                              password=config['FTP']['password'])
    ftp.connect()
    list_of_edr = ftp.get_files_from_last(type_of_edr='sgsn')
    ftp.parse_file(list_of_edr)


if __name__ == '__main__':
    main()
