import sys, os, re
import argparse
import subprocess
import requests
from bs4 import BeautifulSoup
import zipfile
from config import *
import papermill



class my_processor():

    EXIT_PASS, EXIT_FAIL = 0, 1

    def __init__(self, mode='normal', url=None):
        # Validate and process argument options
        self.parse_args(mode, url)
        # Initialize database connection
        if mode == 'normal':
            self.request_html()
            self.parse_html()
            self.wget_url()
            self.files_handler()
    
    def parse_args(self, mode, url):
        if mode == 'unittest':
            if url is None:
                print('Missing url')
                sys.app_exit('fail')
            self.url = url
        else:
            parser = argparse.ArgumentParser(description='UCI dataset processor')
            parser.add_argument('-url', '--url', help='Url of dataset', required=True)
            parser.add_argument('-path', '--path', help='Path to Save Files', required=False)

            args = parser.parse_args()

            self.url = args.url
            self.path = args.path
        
    def app_exit(self, status):
        if status.lower() == 'pass':
            print('** App Exit Status: PASS \n')
            exit(self.EXIT_PASS)
        elif status.lower() == 'skip':
            print('** App Exit Status: SKIP \n')
            exit(self.EXIT_PASS)
        else:
            print('** App Exit Status: FAIL \n')
            exit(self.EXIT_FAIL)

    def request_html(self):
        r = requests.get(self.url)
        self.html = r.content.decode('utf-8') # this converts bytes into sring
        return self.html # return statement needed for unittest

    def parse_html(self):
        # parse html return a [] of links
        soup = BeautifulSoup(self.html, 'html.parser')
        self.urls = []
        for link in soup.find_all('a'):
            if '.' in link.get('href'):
                self.urls.append(self.url + link.get('href'))
        return self.urls

    def wget_url(self):
        a = 'wget'
        p = '-P'
        for url in self.urls:
            subprocess.run([a, p, save_data_path, url])
        return 'WGET operation successful'

    def files_handler(self):
        pattern = '([^/]*$)'
        handled_files = []
        for url in self.urls:
            file_name = re.search(pattern, url)
            if 'zip' in file_name[0]:
                with zipfile.ZipFile(save_data_path + '/' + file_name[0], 'r') as zip_ref:
                    zip_ref.extractall(save_data_path)
            handled_files.append(file_name[0])
        return handled_files
    
    def execute_papermill(self):
        # first build the execute string
        
        pass


if __name__=='__main__':
    app = my_processor()