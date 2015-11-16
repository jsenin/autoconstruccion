import unittest
from autoconstruccion import create_app


class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = create_app('DEVELOPMENT')
        self.client = self.app.test_client(False)

    def test_home_page_status_ok(self):
        assert self.client.get('/').status_code == 200

if __name__ == '__main__':
    unittest.main()
