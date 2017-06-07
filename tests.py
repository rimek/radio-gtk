import unittest

import http
import requests

from rimradio import streams


class StreamAvailabilityTest(unittest.TestCase):
    def test_streams(self):
        for name, stream in streams.items():
            # with self.assertRaisesRegexp(http.client.BadStatusLine, 'ICY 200 OK'):

            print('Testing stream %s: %s' % (name, stream))

            try:
                response = requests.get(stream)
                self.assertEqual(response.status_code, 200)
            except requests.exceptions.ConnectionError as e:
                # TODO find a better way to check the stream
                self.assertTrue(isinstance(e.args[0].args[1], http.client.BadStatusLine))


if __name__ == '__main__':
    unittest.main()
