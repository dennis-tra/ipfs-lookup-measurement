import unittest
from model_log_file import LogFile


class TestLog(unittest.TestCase):

    def test_retrieval_logs_fixture_1(self):
        publications, retrievals = LogFile.parse("model_log_file_1.fixture")
        cid = "QmUoMx68PxewNQ3piRRRjerAEKYXrwyyDvo4czmx8wratC"
        self.assertEqual(len(retrievals), 0)
        self.assertEqual(len(publications), 1)
        self.assertEqual(len(publications[cid].add_provider_queries), 20)
        self.assertLessEqual(len(publications[cid].get_provider_queries), len(publications[cid].add_provider_queries))

    def test_retrieval_logs_fixture_3(self):
        publications, retrievals = LogFile.parse("model_log_file_3.fixture")
        cid = "QmUoMx68PxewNQ3piRRRjerAEKYXrwyyDvo4czmx8wratC"
        self.assertEqual(len(retrievals), 0)
        self.assertEqual(len(publications), 1)
        self.assertEqual(len(publications[cid].add_provider_queries), 20)
        self.assertLessEqual(len(publications[cid].get_provider_queries), len(publications[cid].add_provider_queries))
