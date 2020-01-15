#!/usr/bin/python3
import os.path
from ftplib import FTP

import yaml


def load_settings(file: str) -> tuple:
    """Return dict ip addresses and path string from settings"""
    try:
        with open(file) as f:
            settings = yaml.safe_load(f)
    except FileNotFoundError:
        settings = {'addresses': {'127.0.0.1': 'localhost'}, 'path': '~'}
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
            if file.endswith('.jipg'):
                file_location = os.path.join(path, address, file)
                if not os.path.isfile(file_location):
                    print('Download new file ' + file)
                    ftp.retrbinary('RETR ' + file, open(file_location, 'wb').write)
                elif ftp.size(file) > os.path.getsize(file_location):
                    print('Update file ' + file)
                    ftp.retrbinary('RETR ' + file, open(file_location, 'wb').write)
        ftp.quit()


if __name__ == "__main__":
    file_settings = 'get_ftp_jipg.yml'
    ip, data_path = load_settings(file_settings)
    for ip_address in ip.keys():
        download_files(ip_address, data_path)
