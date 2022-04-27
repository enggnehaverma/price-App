import unittest
from server import app
import requests

URL = "http://127.0.0.1:5000"

dataToCompare={
    'prod_name' : 'chair',
    'prod_id' : 1,
    'price_per_unit' : 8,
    'created_date' : '2022-04-26 22:09:06.460863'
}

class TestMain(unittest.TestCase):
    # Check if response is 200

    def test_1_productlist(self):
        tester = app.test_client(self)
        response = tester.get("/productlist")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_2_pricing(self):
        tester = app.test_client(self)
        response = tester.get("/pricing")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_3_exchangerate(self):
        tester = app.test_client(self)
        response = tester.get("/exchangerate")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_4_error(self):
        tester = app.test_client(self)
        response = tester.get("/error")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_4_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_4_exc_rate(self):
        tester = app.test_client(self)
        response = tester.get("/excrate")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_5_get_request(self):
        tester = app.test_client(self)
        r = tester.get('http://127.0.0.1:5000/productlist')
        #self.assertAlmostEqual(r.json(),dataToCompare)
        self.assertEqual(r.status_code, 200)
        #self.assertEqual(len(r.json()), 4)

if __name__ == "__main__" :
    unittest.main()

