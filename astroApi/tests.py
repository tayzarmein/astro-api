import unittest
import requests
import json


class AstroApi_test(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000"

    def testGetTbrgStar(self):
        response = requests.post(self.base_url + "/astroapi/", json={
            'type': 'GET_TBRG_STAR',
            'date': '2020-05-23T23:12:23.123Z',
            'lat': 12.23,
            'long': 121.23,
            'selectedStar': 'Sirius',
        })
        self.assertEqual(response.headers["Content-type"], 'application/json')

        jsonResponse = json.loads(response.content)
        self.assertIsInstance(jsonResponse, dict)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(jsonResponse["az"], float)


if __name__ == "__main__":
    unittest.main()
