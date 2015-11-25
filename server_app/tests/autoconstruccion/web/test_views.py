import unittest
from autoconstruccion import create_app


class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = create_app('DEVELOPMENT')
        self.client = self.app.test_client(False)



if __name__ == '__main__':
    unittest.main()
