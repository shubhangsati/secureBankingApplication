from app import app
import unittest


class FlaskTestCase(unittest.TestCase):

    def test_server(self):
        tester = app.test_client(self)
        response = tester.get("/test", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'It works!' in response.data)


if __name__ == "__main__":
    unittest.main()
