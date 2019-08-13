#!/usr/bin/python3
from ftplib import FTP
from os.path import isfile, join, getsize


def addresses_list(file_name):
    """Возвращает список IP-адресов"""
    with open(file_name) as ip_list:
        for string in ip_list:
            string_list = string.strip().split()
            addresses.append(string_list[0])

def download_file(address):
    """Скачивание или обновление файла"""
    print('Connecting to ' + address + '.')
    try:
        ftp.connect(address, 2121)
    except OSError:
        print('Network is unreachable.')
    else:
        ftp.login('monitor', 'usermon')
        files = ftp.nlst()
        for file in files:
            if len(file) > 4 and file[-5:] == '.jipg':
                if not isfile(join(address, file)):
                    print('Download new file ' + file + '.')
                    ftp.retrbinary('RETR ' + file, open(join(address, file), 'wb').write)
                elif ftp.size(file) > getsize(join(address, file)):
                    print('Update file ' + file + '.')
                    ftp.retrbinary('RETR ' + file, open(join(address, file), 'wb').write)
        ftp.quit()


addresses = []
addresses_list('get_ftp_jipg.ini')
ftp = FTP()
for ip_address in addresses:
    download_file(ip_address)
