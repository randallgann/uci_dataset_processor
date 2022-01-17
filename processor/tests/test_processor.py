import unittest
import sys, os.path, re

sys.path.insert(0, '/home/randall/Dev/uci_dataset_processor/processor')
bin_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(bin_path)
#sys.path.insert(0, lib_path)

#import wget_functions
import processor

class TestProcessor(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        mode = 'unittest'
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00554/'
        self.app = processor.my_processor(mode, url)

    def test_request_and_parse_html(self):
        response = self.app.request_html()
        self.assertEqual(response[:14], '<!DOCTYPE HTML')
        self.assertIsInstance(self.app.parse_html()[0], str)
        
    def test_wget_files_and_handler(self):
        self.assertEqual(self.app.wget_url(), 'WGET operation successful')
        self.assertIsInstance(self.app.files_handler(), list)

    # Next i need to build the papermill execute string
#    import papermill as pm

#    pm.execute_notebook(
#        'path/to/input.ipynb',
#        'path/to/output.ipynb',
#        parameters=dict(alpha=0.6, ratio=0.1)
#)
    # def test_file_handler(self):
        

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