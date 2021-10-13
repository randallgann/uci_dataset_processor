import sys, os.path, re
import argparse
import subprocess
import requests

class my_processor():

    EXIT_PASS, EXIT_FAIL = 0, 1

    def __init__(self, mode='normal', url=None):
        # Validate and process argument options
        self.parse_args(mode, url)
        # Initialize database connection
        self.request_html()
    
    def parse_args(self, mode, url):
        if mode == 'unittest':
            if url is None:
                print('Missing url')
                sys.app_exit('fail')
            self.url = url
        else:
            parser = argparse.ArgumentParser(description='UCI dataset processor')
            parser.add_argument('-url', '--url', help='Url of dataset', required=True)

            args = parser.parse_args()

            self.url = args.url
        
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
        return self.html

    def parse_html(self):
        pass

    def wget_url(self, url):
        a = 'wget'
        subprocess.run([a, url])

if __name__=='__main__':
    app = my_processor()