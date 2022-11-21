import unittest

from dateutil.parser import isoparse

from dht.model_log_file import LogFile
from dht.model_peer import Peer


class TestLog(unittest.TestCase):

    def test_fixture_provide_1(self):
        parsed = LogFile.parse("./fixtures/provide_1.logs")
        self.assertEqual(len(parsed[0]), 1)
        self.assertEqual(len(parsed[1]), 0)

        publication = parsed[0]["QmR8ffx6ZFy3Yu9KWbguYDdsgTkS3foouB4aY7AkZQqbB9"]
        self.assertEqual(publication.provide_started_at, isoparse("2022-01-13T12:40:16.462604442Z"))
        self.assertEqual(publication.find_node_started_at, isoparse("2022-01-13T12:40:16.462646736Z"))
        self.assertEqual(publication.dht_walk_ended_at, isoparse("2022-01-13T12:41:05.089824389Z"))
        self.assertEqual(publication.provide_ended_at, isoparse("2022-01-13T12:41:20.093760007Z"))
        self.assertEqual(publication.get_providers_ended_at, isoparse("2022-01-13T12:41:25.095415588Z"))

        query = publication.find_node_queries[0]
        self.assertEqual(query.started_at, isoparse("2022-01-13T12:40:16.462911643Z"))
        self.assertEqual(query.ended_at, isoparse("2022-01-13T12:40:16.786165203Z"))
        self.assertEqual(query.target_peer.id, "12D3KooWJuXdZjWiYtXLbrKdeyGcBpGGkNe7iAavafUMuZPxsinp")
        self.assertEqual(query.is_done, True)

        add_query = publication.add_provider_queries[Peer("12D3KooWEWocZsZ7RJFEu8gptfsKrYssMQohbrNjJ9h8JX1i8f3x", "")]
        self.assertEqual(add_query.started_at, isoparse("2022-01-13T12:41:05.090503288Z"))
        self.assertEqual(add_query.ended_at, isoparse("2022-01-13T12:41:05.435674841Z"))
        self.assertEqual(add_query.target_peer.id, "12D3KooWEWocZsZ7RJFEu8gptfsKrYssMQohbrNjJ9h8JX1i8f3x")
        self.assertEqual(add_query.is_done, True)

        get_query = publication.get_provider_queries[Peer("12D3KooWEWocZsZ7RJFEu8gptfsKrYssMQohbrNjJ9h8JX1i8f3x", "")]
        self.assertEqual(get_query.started_at, isoparse("2022-01-13T12:41:05.435674841Z"))
        self.assertEqual(get_query.ended_at, isoparse("2022-01-13T12:41:05.603379542Z"))
        self.assertEqual(get_query.target_peer.id, "12D3KooWEWocZsZ7RJFEu8gptfsKrYssMQohbrNjJ9h8JX1i8f3x")
        self.assertEqual(get_query.is_done, True)

    def test_fixture_provide_2(self):
        parsed = LogFile.parse("./fixtures/provide_2.logs")
        self.assertEqual(len(parsed[0]), 1)
        self.assertEqual(len(parsed[1]), 0)
        print(parsed)

    def test_fixtures_retrieve_1(self):
        parsed = LogFile.parse("./fixtures/retrieve_1.logs")
        self.assertEqual(len(parsed[0]), 0)
        self.assertEqual(len(parsed[1]), 1)
        print(parsed)

    def test_fixtures_retrieve_2(self):
        parsed = LogFile.parse("./fixtures/retrieve_2.logs")
        self.assertEqual(len(parsed[0]), 0)
        self.assertEqual(len(parsed[1]), 1)
        retrieval = parsed[1]["QmZwPsruoPazxL1QwCARW5YAowrXwABFdFn8XJn5fvJirG"]

        self.assertEqual(retrieval.retrieval_started_at, isoparse("2022-01-13T11:26:49.945149975Z"))
        self.assertEqual(retrieval.get_providers_queries_started_at, isoparse("2022-01-13T11:26:50.947272519Z"))
        self.assertEqual(retrieval.get_providers_queries[
                             Peer("12D3KooWB6KEaSdTdWQFw8u1AuxnvTwASUoomxxBAesPyW7iYEDo", "")].started_at,
                         isoparse("2022-01-13T11:26:51.089590116Z"))
        query = retrieval.get_providers_queries[Peer("12D3KooWJgf6ryYYAJkYW3nSoA7YoVgpb5u5CnXtFP3HXV1BSw7m", "")]
        self.assertEqual(query.started_at, isoparse("2022-01-13T11:26:51.735121196Z"))
        self.assertEqual(query.ended_at, isoparse("2022-01-13T11:26:51.896227511Z"))
        self.assertEqual(query.providers_count, 1)
        self.assertEqual(retrieval.dial_started_at, isoparse("2022-01-13T11:26:51.78742086Z"))
        self.assertEqual(retrieval.connected_at, isoparse("2022-01-13T11:26:52.01916078Z"))
        self.assertEqual(retrieval.stream_opened_at, isoparse("2022-01-13T11:26:52.248016655Z"))
        self.assertEqual(retrieval.received_first_HAVE_at, isoparse("2022-01-13T11:26:52.248176307Z"))
        self.assertEqual(retrieval.done_retrieving_at, isoparse("2022-01-13T11:26:52.482203774Z"))
        self.assertEqual(retrieval.finished_searching_providers_at, isoparse("2022-01-13T11:26:53.587771644Z"))

    def test_fixtures_retrieve_3(self):
        parsed = LogFile.parse("./fixtures/retrieve_3.logs")
        self.assertEqual(len(parsed[0]), 0)
        self.assertEqual(len(parsed[1]), 1)
        retrieval = parsed[1]["QmTRewf9i2KYkKMMVchcpHJatBhGocUDmTrqqRTnxjeKg2"]

        self.assertEqual(retrieval.retrieval_started_at, isoparse("2022-01-13T20:19:19.203983015Z"))
        self.assertEqual(retrieval.get_providers_queries_started_at, isoparse("2022-01-13T20:19:20.204688627Z"))
        self.assertEqual(retrieval.get_providers_queries[
                             Peer("Qmd7p3UADbSLbQsBE8oUTnGYLvz77L9Nm6uKdsDohtGZcM", "")].started_at,
                         isoparse("2022-01-13T20:19:20.205599333Z"))

        self.assertEqual(retrieval.dial_started_at, isoparse("2022-01-13T20:19:20.313263931Z"))
        self.assertEqual(retrieval.connected_at, isoparse("2022-01-13T20:19:20.45608161Z"))
        self.assertEqual(retrieval.stream_opened_at, isoparse("2022-01-13T20:19:20.598953276Z"))
        self.assertEqual(retrieval.received_first_HAVE_at, isoparse("2022-01-13T20:19:20.599043906Z"))
        self.assertEqual(retrieval.done_retrieving_at, isoparse("2022-01-13T20:19:20.749028636Z"))
        self.assertEqual(retrieval.finished_searching_providers_at, isoparse("2022-01-13T20:19:21.439215132Z"))

        query = retrieval.get_providers_queries[Peer("12D3KooWAj6LdLGh2xsBR6s289v2LJXKTu8SE8nkvEXiMBjBUdf7", "")]
        self.assertEqual(query.started_at, isoparse("2022-01-13T20:19:20.932019306Z"))
        self.assertEqual(query.ended_at, isoparse("2022-01-13T20:19:21.438640536Z"))
        self.assertEqual(query.providers_count, 0)

        self.assertTrue(Peer("12D3KooWMNGjATagX7wjS2M5LqxFFMvXWcoRs9JdvZCMaMoXZnNV", "") in retrieval.provider_peers)
        self.assertTrue(Peer("12D3KooWGcSgcQ13R9eHkgTqkbhW2uPek23qefmmMSMjbQkTEFu3", "") in retrieval.provider_peers)

    def test_fixtures_retrieve_4(self):
        parsed = LogFile.parse("./fixtures/retrieve_4.logs")
        self.assertEqual(len(parsed[0]), 0)
        self.assertEqual(len(parsed[1]), 1)

        retrieval = parsed[1]["QmZJyDj2o2jk1ZizDYp7MJpSSADGsxrJgwQtz46hqXicZn"]
        self.assertEqual(retrieval.retrieval_started_at, isoparse("2022-01-14T06:22:02.414544895Z"))
        self.assertEqual(retrieval.get_providers_queries_started_at, isoparse("2022-01-14T06:22:03.417774789Z"))
        self.assertEqual(retrieval.received_first_HAVE_at, isoparse("2022-01-14T06:22:03.754223881Z"))
        self.assertEqual(retrieval.done_retrieving_at, isoparse("2022-01-14T06:22:03.978160419Z"))



if __name__ == '__main__':
    unittest.main()
