import unittest
import sys, os.path, re

sys.path.insert(0, '/home/randall/Dev/uci_dataset_processor/processor')
bin_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(bin_path)
#sys.path.insert(0, lib_path)

#import wget_functions
import processor

class TestProcessor(unittest.TestCase):
    
    def setUp(self):
        mode = 'unittest'
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00554/'
        self.app = processor.my_processor(mode, url)

    def test_request_html(self):
        self.assertEqual(self.app.request_html()[:14], '<!DOCTYPE HTML')

    def test_html_parse(self):
        self.assertIsInstance(self.app.parse_html()[0], str)

    def test_wget_files(self):
        pass

    #def tearDown(self) -> None:
    #    i = super().tearDown()
    #   return super().tearDown()


#class TestWget(unittest.TestCase):
#    def test_wget_url(self):
#        """
#        Test that it can download a given downloadable url link
#        """
#        wget_functions.wget_url()

if __name__ == '__main__':
    unittest.main()