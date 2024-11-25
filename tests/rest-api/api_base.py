
import unittest
import os

class TestApiBase(unittest.TestCase):
    __test__ = False

    def setUp(self):
        self.base_url = os.getenv("HUSH_APIGW_URL")
        if not self.base_url:
            self.fail("Environment variable 'HUSH_APIGW_URL' is not set.")
        self.base_url = self.base_url + '/v1'

        self.aws_reqion = os.getenv("HUSH_AWS_REGION")
        if not self.aws_reqion:
            self.fail("Environment variable 'HUSH_AWS_REGION' is not set.")