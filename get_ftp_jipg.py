#!/usr/bin/python3
import os.path
import yaml
from ftplib import FTP


def load_settings(file_name: str) -> tuple:
    """Return dict of settings"""
    try:
        with open('get_ftp_jipg.yml') as f:
            settings = yaml.safe_load(f)
    except FileNotFoundError:
        settings = {'path': '~', 'addresses': {'127.0.0.1': 'localhost'}}
    return settings['addresses'], settings['path']


def download_files(address: str, path: str):
    """Download or update a file"""
    ftp = FTP()
    print('Connecting to ' + address)
    try:
        ftp.connect(address, 2121)
    except OSError:
        print('Network is unreachable')
    else:
        ftp.login('monitor', 'usermon')
        files = ftp.nlst()
        for file in files:
            if len(file) > 4 and file[-5:] == '.jipg':
                if not os.path.isfile(os.path.join(path, address, file)):
                    print('Download new file ' + file)
                    ftp.retrbinary('RETR ' + file, open(os.path.join(path, address, file), 'wb').write)
                elif ftp.size(file) > os.path.getsize(os.path.join(path, address, file)):
                    print('Update file ' + file)
                    ftp.retrbinary('RETR ' + file, open(os.path.join(path, address, file), 'wb').write)
        ftp.quit()


if __name__ == "__main__":
    ip, path = load_settings('get_ftp_jipg.yml')
    for address in ip.keys():
        download_files(address, path)
