import unittest
from model_log_line import LogLine
from dateutil.parser import isoparse

from model_peer import Peer


class TestLog(unittest.TestCase):

    def test_log_is_start_providing(self):
        parsed = LogLine(
            "2022-01-12T15:28:41.164857388Z: Start providing cid QmPf1NktjTcT4bHDZUAFWNhkUtRAkiYRbCQCoMbDFUTER2",
            None).is_start_providing()
        self.assertEqual(parsed.cid, "QmPf1NktjTcT4bHDZUAFWNhkUtRAkiYRbCQCoMbDFUTER2")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:28:41.164857388Z"))

        cid = LogLine("invalid", None).is_start_providing()
        self.assertEqual(cid, None)

    def test_log_is_start_getting_closest_peers(self):
        parsed = LogLine(
            "2022-01-12T15:33:39.721929903Z: Start getting closest peers to cid QmRqMeMtmVYj2cWb1HmRgunEMZDkja2s82rYRW51vwV3J5",
            None).is_start_getting_closest_peers()
        self.assertEqual(parsed.cid, "QmRqMeMtmVYj2cWb1HmRgunEMZDkja2s82rYRW51vwV3J5")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:33:39.721929903Z"))

        cid = LogLine("invalid", None).is_start_providing()
        self.assertEqual(cid, None)

    def test_log_is_getting_closest_peers(self):
        parsed = LogLine(
            "2022-01-12T15:33:39.722688082Z: Getting closest peers for cid QmRqMeMtmVYj2cWb1HmRgunEMZDkja2s82rYRW51vwV3J5 from QmW5NjfCRGT8kaoHrpJ5eWg59rCheQjk5QvJjKmJxMpbCP(go-ipfs/0.8.0/)",
            None).is_getting_closest_peers()
        self.assertEqual(parsed.cid, "QmRqMeMtmVYj2cWb1HmRgunEMZDkja2s82rYRW51vwV3J5")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:33:39.722688082Z"))
        self.assertEqual(parsed.remote_peer.id, "QmW5NjfCRGT8kaoHrpJ5eWg59rCheQjk5QvJjKmJxMpbCP")
        self.assertEqual(parsed.remote_peer.agent_version, "go-ipfs/0.8.0/")

        cid = LogLine("invalid", None).is_getting_closest_peers()
        self.assertEqual(cid, None)

    def test_log_is_got_provider(self):
        parsed = LogLine(
            "2022-01-12T14:51:39.546677792Z: Got provider 12D3KooWHpyf9LmvsWgvJF2eBQdrWdt1dphtyK1RRPwWyvLCXhJd for content QmXZ5vjyFPH95PfUPZWx8tFXPW9zDPuLJt2pmneBHqPStb",
            None).is_got_provider()
        self.assertEqual(parsed.cid, "QmXZ5vjyFPH95PfUPZWx8tFXPW9zDPuLJt2pmneBHqPStb")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T14:51:39.546677792Z"))
        self.assertEqual(parsed.remote_peer.id, "12D3KooWHpyf9LmvsWgvJF2eBQdrWdt1dphtyK1RRPwWyvLCXhJd")
        self.assertEqual(parsed.remote_peer.agent_version, "n.a.")

        cid = LogLine("invalid", None).is_getting_closest_peers()
        self.assertEqual(cid, None)

    def test_log_is_got_closest_peers(self):
        parsed = LogLine(
            "2022-01-12T15:33:39.785615224Z: Got 20 closest peers to cid QmRqMeMtmVYj2cWb1HmRgunEMZDkja2s82rYRW51vwV3J5 from 12D3KooWCpu8Nk4wmoXSsVeVSVzVHmrwBnEoC9jpcVpeWP7n67Bt(go-ipfs/0.11.0-dev/ef0428a):  12D3KooWStFdcZRjLvLWdiEoHsSiYhbsbLek9yMG69BZhedKcZTr 12D3KooWA8a8hwhmiK27hBekToNPBVVfMqVD6W5TWTXA93TiUzVo 12D3KooWSznNjrr86rzib97WCKa6nTcaFv8NaqpcuZBQMc8mnbMz QmPySsdmbczdZYBpbi2oq2WMJ8ErbfxtkG8Mo192UHkfGP 12D3KooWAgZMjJkj8bqsmjRMCecqfoUMGvm5JuWnoGhf7Zv9d8g8 12D3KooWKrEdbRaktJLruuwwqLKzggrbatV1xjrUFvxUK2Bsm32r 12D3KooWC8D7AJRuYx1DoXE5ibnLZQRts4tcvXBMwAPUNiS4iuj5 12D3KooWE9GzUXDqhgxSy4xrpaD7o1u4m33ydaGUzTiFJWD7iw7W 12D3KooWK7mtceLAgqpjGE5xzn8na8VYMx916eCKPbU2FeUC4VQm 12D3KooWLeSjMKfe6yH6jwWxGxfwgLrx92XwJn5cxisECBjKaMhk 12D3KooWBbJtZicZU2BVr65jggHqmiLF4NdQmFKVme1drHnNEirS 12D3KooWDXT5Hxk8r5r4Af8BmqXn7B2v2FJqiMh2fWGKaZgCWYDm 12D3KooWGJnTNUxivQsAB4LEhr13Q6iezPfSuBC5dz7YRDVfrxNv 12D3KooWCBipj6qakV9uajDV8h7jEhCS1FyjxPpL1ZPvYB8JyqLU 12D3KooWM4RjMeGXKxGURbTyY8G3SpiUG4FjXKM9LWRW5CwajrFT 12D3KooWFpirSG8TGgjps1dnLjjBQ1G8a6bT8NUgPruwn2C38ccD 12D3KooWC9GUx1ZduRfbmxcdtMDMDZZtBdRHCp7eFM3xLyH3Egs7 12D3KooWEDMw7oRqQkdCJbyeqS5mUmWGwTp8JJ2tjCzTkHboF6wK 12D3KooWRTepFC1CLHGB9CLzKWnEo3aDddaN1xL7YpiNvVjjuVmj 12D3KooWN3QPsKngxBf87qG5JyJmKz5rGcMJ52ptPme66SBZiVYH",
            None).is_got_closest_peers()
        self.assertEqual(parsed.cid, "QmRqMeMtmVYj2cWb1HmRgunEMZDkja2s82rYRW51vwV3J5")
        self.assertEqual(parsed.remote_peer.id, "12D3KooWCpu8Nk4wmoXSsVeVSVzVHmrwBnEoC9jpcVpeWP7n67Bt")
        self.assertEqual(parsed.remote_peer.agent_version, "go-ipfs/0.11.0-dev/ef0428a")
        expected_peers = [
            Peer("12D3KooWStFdcZRjLvLWdiEoHsSiYhbsbLek9yMG69BZhedKcZTr", "n.a."),
            Peer("12D3KooWA8a8hwhmiK27hBekToNPBVVfMqVD6W5TWTXA93TiUzVo", "n.a."),
            Peer("12D3KooWSznNjrr86rzib97WCKa6nTcaFv8NaqpcuZBQMc8mnbMz", "n.a."),
            Peer("QmPySsdmbczdZYBpbi2oq2WMJ8ErbfxtkG8Mo192UHkfGP", "n.a."),
            Peer("12D3KooWAgZMjJkj8bqsmjRMCecqfoUMGvm5JuWnoGhf7Zv9d8g8", "n.a."),
            Peer("12D3KooWKrEdbRaktJLruuwwqLKzggrbatV1xjrUFvxUK2Bsm32r", "n.a."),
            Peer("12D3KooWC8D7AJRuYx1DoXE5ibnLZQRts4tcvXBMwAPUNiS4iuj5", "n.a."),
            Peer("12D3KooWE9GzUXDqhgxSy4xrpaD7o1u4m33ydaGUzTiFJWD7iw7W", "n.a."),
            Peer("12D3KooWK7mtceLAgqpjGE5xzn8na8VYMx916eCKPbU2FeUC4VQm", "n.a."),
            Peer("12D3KooWLeSjMKfe6yH6jwWxGxfwgLrx92XwJn5cxisECBjKaMhk", "n.a."),
            Peer("12D3KooWBbJtZicZU2BVr65jggHqmiLF4NdQmFKVme1drHnNEirS", "n.a."),
            Peer("12D3KooWDXT5Hxk8r5r4Af8BmqXn7B2v2FJqiMh2fWGKaZgCWYDm", "n.a."),
            Peer("12D3KooWGJnTNUxivQsAB4LEhr13Q6iezPfSuBC5dz7YRDVfrxNv", "n.a."),
            Peer("12D3KooWCBipj6qakV9uajDV8h7jEhCS1FyjxPpL1ZPvYB8JyqLU", "n.a."),
            Peer("12D3KooWM4RjMeGXKxGURbTyY8G3SpiUG4FjXKM9LWRW5CwajrFT", "n.a."),
            Peer("12D3KooWFpirSG8TGgjps1dnLjjBQ1G8a6bT8NUgPruwn2C38ccD", "n.a."),
            Peer("12D3KooWC9GUx1ZduRfbmxcdtMDMDZZtBdRHCp7eFM3xLyH3Egs7", "n.a."),
            Peer("12D3KooWEDMw7oRqQkdCJbyeqS5mUmWGwTp8JJ2tjCzTkHboF6wK", "n.a."),
            Peer("12D3KooWRTepFC1CLHGB9CLzKWnEo3aDddaN1xL7YpiNvVjjuVmj", "n.a."),
            Peer("12D3KooWN3QPsKngxBf87qG5JyJmKz5rGcMJ52ptPme66SBZiVYH", "n.a."),
        ]
        self.assertEqual(parsed.closest_peers, expected_peers)

        cid = LogLine("invalid", None).is_getting_closest_peers()
        self.assertEqual(cid, None)

    def test_log_is_error_getting_closest_peers(self):
        parsed = LogLine(
            "2022-01-13T12:40:35.091228329Z: Error getting closest peers for cid QmR8ffx6ZFy3Yu9KWbguYDdsgTkS3foouB4aY7AkZQqbB9 from Qmen1J2jkD4UDsrPqjM2LtVTavtjAu696kXJiFPVtjJo8m(storm): failed to dial Qmen1J2jkD4UDsrPqjM2LtVTavtjAu696kXJiFPVtjJo8m:,  * [/ip4/127.0.0.1/tcp/42507] dial tcp4 127.0.0.1:42507: connect: connection refused,  * [/ip4/179.84.135.89/tcp/42507] failed to negotiate security protocol: context deadline exceeded",
            None).is_error_getting_closest_peers()
        self.assertEqual(parsed.cid, "QmR8ffx6ZFy3Yu9KWbguYDdsgTkS3foouB4aY7AkZQqbB9")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-13T12:40:35.091228329Z"))
        self.assertEqual(parsed.remote_peer.id, "Qmen1J2jkD4UDsrPqjM2LtVTavtjAu696kXJiFPVtjJo8m")
        self.assertEqual(parsed.remote_peer.agent_version, "storm")
        self.assertEqual(parsed.error_str,
                         "failed to dial Qmen1J2jkD4UDsrPqjM2LtVTavtjAu696kXJiFPVtjJo8m:,  * [/ip4/127.0.0.1/tcp/42507] dial tcp4 127.0.0.1:42507: connect: connection refused,  * [/ip4/179.84.135.89/tcp/42507] failed to negotiate security protocol: context deadline exceeded")

    def test_log_is_add_provider_started(self):
        parsed = LogLine(
            "2022-01-13T12:41:05.090200065Z: Start putting provider record for cid QmR8ffx6ZFy3Yu9KWbguYDdsgTkS3foouB4aY7AkZQqbB9 to 12D3KooWRNYZFhrkozXCZQwmGSehHjqYzoN7ZdGLw5B34Wjg4Eht(n.a.)",
            None).is_add_provider_started()
        self.assertEqual(parsed.cid, "QmR8ffx6ZFy3Yu9KWbguYDdsgTkS3foouB4aY7AkZQqbB9")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-13T12:41:05.090200065Z"))
        self.assertEqual(parsed.remote_peer.id, "12D3KooWRNYZFhrkozXCZQwmGSehHjqYzoN7ZdGLw5B34Wjg4Eht")
        self.assertEqual(parsed.remote_peer.agent_version, "n.a.")

    def test_log_is_pvd_dht_walk_end(self):
        parsed = LogLine(
            "2022-01-12T15:25:10.546838625Z: In total, got 20 closest peers to cid QmaU4UUvL77BpkWXG3Tfq41Vccb6BWL5kGYpjCGtyZD1UA to publish record: QmQVvETseWiCr9rwkFc11cmsWkLYqRnbXyHLo3PwoHNECi(go-ipfs/0.8.0/48f94e2) 12D3KooWAtB3AtsrmSFP3ZH5sXLqosMqKgomcXxwwYCQyVzpVdWQ(go-ipfs/0.7.0/) Qme1VirUR9jJrAtTkyWRQy95r3rHq67iGrXcMLp4c7uVB2(go-ipfs/0.8.0/48f94e2) 12D3KooWAPeySLwwtbbRH11Ug768h1TTDhngTAwNeVJERJ2KVCr7(go-ipfs/0.9.0/) 12D3KooWPGDKrgrpaHSk8kjXTCDDUuLsBuJmVu3E3CAsXJs4w7To(n.a.) 12D3KooWGbPV7mdg4JxSFUL7fD3xBHZWzCJWAkx7W9QMsjTEGhrn(go-ipfs/0.10.0/64b532fbb) 12D3KooWPqzJdEH16xAW2AaEJgVZtb5Vfhy8N5k3syUUtDZ8ZypA(go-ipfs/0.10.0/) 12D3KooWHYECSHmxNPxTGFXpV9ekEgUU9JTvPfs2y125nbKWZFH8(go-ipfs/0.9.1/) 12D3KooWSRn7UucM7xoHQEXgTkpLpv3ShrJRTCvz6EkxNSu4rMbH(go-ipfs/0.9.0/) 12D3KooWJyxLGVneFaadwzqvzFcKZYVMm1UCbf4nqVmMXweCct9s(n.a.) 12D3KooWFge1jrRCdvA7dbZBXbdqJz9s5knQPkKikXzK4Amxt4Mo(go-ipfs/0.7.0/) 12D3KooWP7Aw2KGoj85i5FsxYHK1gyCqXzuzwDScymSoS9wGsyyY(n.a.) 12D3KooWKZgV2NyfMZgScvLB3zQTCjKZX7faSyNmA71wkd94iFuv(n.a.) 12D3KooWE2jF6zhhP1Ubbxxoj8geoxWLvj8JP9iK3FsVQJZJbuJP(go-ipfs/0.7.0/) 12D3KooWNpqJhAkLDsbtiachKAkX2LV8MWYacZoJs6j9Utc7c3V8(go-ipfs/0.9.0/) 12D3KooWErRM449DVh9ZpSVwxfGU98NH2YR9H9e4tNqPxwmKm6V5(go-ipfs/0.9.1/dc2715a) QmYMwjoy5pTZzBy9kV4taogUq9pBhc2bQqnMwAG59mBwmX(storm) QmXa1tRfbeAoB2b8iba94D1BASZdV2F7szuBXoVMvy1ZZx(go-ipfs/0.8.0/48f94e2) 12D3KooWP8uN95URtKD1s4mKuJuEqBzsR8hvVM19obgmFBGzEpiy(go-ipfs/0.7.0/) Qmd3gbBj7FZNLrYsExaS85m4eUMdU8MCrSvYuAr5cWaxrc(go-ipfs/0.11.0/) ",
            None).is_pvd_dht_walk_end()
        self.assertEqual(parsed.cid, "QmaU4UUvL77BpkWXG3Tfq41Vccb6BWL5kGYpjCGtyZD1UA")
        self.assertEqual(parsed.remote_peer, None)

        cid = LogLine("invalid", None).is_pvd_dht_walk_end()
        self.assertEqual(cid, None)

    def test_log_is_add_provider_success(self):
        parsed = LogLine(
            "2022-01-12T15:17:09.428086541Z: Succeed in putting provider record for cid QmRY9ZMn1Fm3p3a4k8WJipnAKjYQ3GhjceTjKu9opUW3m2 to QmXECULqVaM2RuVpSWpELe9yCfsuVZHfnvMBKuHpPDExJq(go-ipfs/0.8.0/48f94e2)",
            None).is_add_provider_success()
        self.assertEqual(parsed.cid, "QmRY9ZMn1Fm3p3a4k8WJipnAKjYQ3GhjceTjKu9opUW3m2")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:17:09.428086541Z"))
        self.assertEqual(parsed.remote_peer.id, "QmXECULqVaM2RuVpSWpELe9yCfsuVZHfnvMBKuHpPDExJq")
        self.assertEqual(parsed.remote_peer.agent_version, "go-ipfs/0.8.0/48f94e2")

        cid = LogLine("invalid", None).is_add_provider_success()
        self.assertEqual(cid, None)

    def test_log_is_add_provider_error(self):
        parsed = LogLine(
            "2022-01-12T15:17:13.06511104Z: Error putting provider record for cid QmRY9ZMn1Fm3p3a4k8WJipnAKjYQ3GhjceTjKu9opUW3m2 to QmRS4sZjaeQn29vfthxxXifSWQc4ciTNEce6griGzBHKdh(n.a.) [failed to dial QmRS4sZjaeQn29vfthxxXifSWQc4ciTNEce6griGzBHKdh:,  * [/ip4/51.15.254.203/tcp/4001] dial tcp4 51.15.254.203:4001: connect: connection refused,  * [/ip4/172.18.0.3/tcp/4001] dial tcp4 172.18.0.3:4001: i/o timeout]",
            None).is_add_provider_error()
        self.assertEqual(parsed.cid, "QmRY9ZMn1Fm3p3a4k8WJipnAKjYQ3GhjceTjKu9opUW3m2")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:17:13.06511104Z"))
        self.assertEqual(parsed.remote_peer.id, "QmRS4sZjaeQn29vfthxxXifSWQc4ciTNEce6griGzBHKdh")
        self.assertEqual(parsed.remote_peer.agent_version, "n.a.")
        self.assertEqual(parsed.error_str,
                         "failed to dial QmRS4sZjaeQn29vfthxxXifSWQc4ciTNEce6griGzBHKdh:,  * [/ip4/51.15.254.203/tcp/4001] dial tcp4 51.15.254.203:4001: connect: connection refused,  * [/ip4/172.18.0.3/tcp/4001] dial tcp4 172.18.0.3:4001: i/o timeout")

        cid = LogLine("invalid", None).is_add_provider_error()
        self.assertEqual(cid, None)

    def test_log_is_get_provider_success(self):
        parsed = LogLine(
            "2022-01-12T15:17:09.519917147Z: Got 1 provider records back from Qmdb3rfcvTGQw7bqznVpF1MHV1kc5vSAwWtQqrNXKauFzT(storm) after a successful put:  12D3KooWPLWBDJDB1gKacwUt4CjCb5ny9BbuZ1d4ynjSk3eJbZij",
            None).is_get_provider_success()
        self.assertEqual(parsed.cid, "")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:17:09.519917147Z"))
        self.assertEqual(parsed.remote_peer.id, "Qmdb3rfcvTGQw7bqznVpF1MHV1kc5vSAwWtQqrNXKauFzT")
        self.assertEqual(parsed.remote_peer.agent_version, "storm")

        cid = LogLine("invalid", None).is_pvd_found()
        self.assertEqual(cid, None)

    def test_log_is_get_provider_error(self):
        parsed = LogLine(
            "2022-01-12T15:07:07.168470708Z: Error getting provider record for cid Qmcb7G2hCJYDPQYreFumfPSS267sJDEZavk4YRfXQYjbbV from 12D3KooWJfxZxgQKnAGj1SP53MPh7SKVdAtU7xmP3hc6HUGHEL1b(go-ipfs/0.9.0/) after a successful put timed out reading response",
            None).is_get_provider_error()
        self.assertEqual(parsed.cid, "Qmcb7G2hCJYDPQYreFumfPSS267sJDEZavk4YRfXQYjbbV")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:07:07.168470708Z"))
        self.assertEqual(parsed.remote_peer.id, "12D3KooWJfxZxgQKnAGj1SP53MPh7SKVdAtU7xmP3hc6HUGHEL1b")
        self.assertEqual(parsed.remote_peer.agent_version, "go-ipfs/0.9.0/")

        cid = LogLine("invalid", None).is_pvd_found()
        self.assertEqual(cid, None)

    def test_log_is_finish_providing(self):
        parsed = LogLine(
            "2022-01-12T15:07:07.168577575Z: Finish providing cid Qmcb7G2hCJYDPQYreFumfPSS267sJDEZavk4YRfXQYjbbV",
            None).is_finish_providing()
        self.assertEqual(parsed.cid, "Qmcb7G2hCJYDPQYreFumfPSS267sJDEZavk4YRfXQYjbbV")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:07:07.168577575Z"))

        cid = LogLine("invalid", None).is_finish_providing()
        self.assertEqual(cid, None)

    def test_log_is_start_retrieving(self):
        parsed = LogLine(
            "2022-01-12T15:05:29.241941904Z: Start retrieving content for QmemmESLgGsBaLr4X2tCxt6DLN2iwcv8j2JfAe9jotRLa4",
            None).is_start_retrieving()
        self.assertEqual(parsed.cid, "QmemmESLgGsBaLr4X2tCxt6DLN2iwcv8j2JfAe9jotRLa4")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:05:29.241941904Z"))

        cid = LogLine("invalid", None).is_start_retrieving()
        self.assertEqual(cid, None)

    def test_log_is_start_searching_pvd(self):
        parsed = LogLine(
            "2022-01-12T15:05:30.243296853Z: Start searching providers for cid QmemmESLgGsBaLr4X2tCxt6DLN2iwcv8j2JfAe9jotRLa4",
            None).is_start_searching_pvd()
        self.assertEqual(parsed.cid, "QmemmESLgGsBaLr4X2tCxt6DLN2iwcv8j2JfAe9jotRLa4")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:05:30.243296853Z"))

        parsed = LogLine(
            "2022-01-12T16:41:44.719287677Z: Start searching providers for cid QmX9JCYLE3vBdVHy1JazY2aWbPyHpj1NVkMYqGVAzg5b1F",
            None).is_start_searching_pvd()
        self.assertEqual(parsed.cid, "QmX9JCYLE3vBdVHy1JazY2aWbPyHpj1NVkMYqGVAzg5b1F")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T16:41:44.719287677Z"))

        cid = LogLine("invalid", None).is_start_retrieving()
        self.assertEqual(cid, None)

    def test_log_is_start_getting_providers(self):
        parsed = LogLine(
            "2022-01-12T15:05:30.244117362Z: Getting providers for cid QmemmESLgGsBaLr4X2tCxt6DLN2iwcv8j2JfAe9jotRLa4 from Qmbut9Ywz9YEDrz8ySBSgWyJk41Uvm2QJPhwDJzJyGFsD6(go-ipfs/0.11.0/67220ed)",
            None).is_start_getting_providers()
        self.assertEqual(parsed.cid, "QmemmESLgGsBaLr4X2tCxt6DLN2iwcv8j2JfAe9jotRLa4")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:05:30.244117362Z"))
        self.assertEqual(parsed.remote_peer.id, "Qmbut9Ywz9YEDrz8ySBSgWyJk41Uvm2QJPhwDJzJyGFsD6")
        self.assertEqual(parsed.remote_peer.agent_version, "go-ipfs/0.11.0/67220ed")

        cid = LogLine("invalid", None).is_start_retrieving()
        self.assertEqual(cid, None)

    def test_log_is_found_provider_entries(self):
        parsed = LogLine(
            "2022-01-12T15:01:02.349908195Z: Found 0 provider entries for cid QmSeMLr3rs8xZKTk9QaxFrD9aZEVSCwuaAoE8ywots7upW from QmUPch8qryfh8PXxHqaFBCHT8TUWKb69Gssi7kZvFNKzXL(go.vocdoni.io/dvote): context canceled",
            None).is_found_provider_entries()
        self.assertEqual(parsed.cid, "QmSeMLr3rs8xZKTk9QaxFrD9aZEVSCwuaAoE8ywots7upW")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:01:02.349908195Z"))
        self.assertEqual(parsed.remote_peer.id, "QmUPch8qryfh8PXxHqaFBCHT8TUWKb69Gssi7kZvFNKzXL")
        self.assertEqual(parsed.remote_peer.agent_version, "go.vocdoni.io/dvote")
        self.assertEqual(parsed.error_str, "context canceled")

        parsed = LogLine(
            "2022-01-12T15:01:02.202394014Z: Found 1 provider entries for cid QmSeMLr3rs8xZKTk9QaxFrD9aZEVSCwuaAoE8ywots7upW from 12D3KooWEbvwVeLVe91sCGaJgf9xkAwwqVQU4G5UmCUFzBo8AiSt(go-ipfs/0.7.0/): ",
            None).is_found_provider_entries()
        self.assertEqual(parsed.cid, "QmSeMLr3rs8xZKTk9QaxFrD9aZEVSCwuaAoE8ywots7upW")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:01:02.202394014Z"))
        self.assertEqual(parsed.remote_peer.id, "12D3KooWEbvwVeLVe91sCGaJgf9xkAwwqVQU4G5UmCUFzBo8AiSt")
        self.assertEqual(parsed.remote_peer.agent_version, "go-ipfs/0.7.0/")
        self.assertEqual(parsed.error_str, None)

        cid = LogLine("invalid", None).is_start_retrieving()
        self.assertEqual(cid, None)

    def test_log_is_pvd_found(self):
        parsed = LogLine(
            "2022-01-12T15:01:02.202506719Z: Found provider 12D3KooWHpyf9LmvsWgvJF2eBQdrWdt1dphtyK1RRPwWyvLCXhJd for cid QmSeMLr3rs8xZKTk9QaxFrD9aZEVSCwuaAoE8ywots7upW from 12D3KooWEbvwVeLVe91sCGaJgf9xkAwwqVQU4G5UmCUFzBo8AiSt(go-ipfs/0.7.0/)",
            None).is_pvd_found()
        self.assertEqual(parsed.cid, "QmSeMLr3rs8xZKTk9QaxFrD9aZEVSCwuaAoE8ywots7upW")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:01:02.202506719Z"))
        self.assertEqual(parsed.remote_peer.id, "12D3KooWEbvwVeLVe91sCGaJgf9xkAwwqVQU4G5UmCUFzBo8AiSt")
        self.assertEqual(parsed.remote_peer.agent_version, "go-ipfs/0.7.0/")
        self.assertEqual(parsed.other_peer.id, "12D3KooWHpyf9LmvsWgvJF2eBQdrWdt1dphtyK1RRPwWyvLCXhJd")
        self.assertEqual(parsed.other_peer.agent_version, "n.a.")

        cid = LogLine("invalid", None).is_pvd_found()
        self.assertEqual(cid, None)

    def test_log_is_bitswap_connect(self):
        parsed = LogLine(
            "2022-01-13T08:36:05.27519329Z: Bitswap connect to peer 12D3KooWSeNdFUhdsCYNq4q7qxWsV6UdADdirGqm6AjsSigqiADs",
            None).is_bitswap_connect()
        self.assertEqual(parsed.cid, "")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-13T08:36:05.27519329Z"))
        self.assertEqual(parsed.remote_peer.id, "12D3KooWSeNdFUhdsCYNq4q7qxWsV6UdADdirGqm6AjsSigqiADs")
        self.assertEqual(parsed.remote_peer.agent_version, "n.a.")

        cid = LogLine("invalid", None).is_bitswap_connect()
        self.assertEqual(cid, None)

    def test_log_is_bitswap_connected(self):
        parsed = LogLine(
            "2022-01-13T11:23:43.813196785Z: Bitswap connected to peer 12D3KooWSVybhAdutmsWmwig3UvMR9JNHc6x5s2cVNpy2cNSuhjC",
            None).is_bitswap_connected()
        self.assertEqual(parsed.cid, "")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-13T11:23:43.813196785Z"))
        self.assertEqual(parsed.remote_peer.id, "12D3KooWSVybhAdutmsWmwig3UvMR9JNHc6x5s2cVNpy2cNSuhjC")
        self.assertEqual(parsed.remote_peer.agent_version, "n.a.")

        cid = LogLine("invalid", None).is_bitswap_connected()
        self.assertEqual(cid, None)

    def test_log_is_done_retrieving(self):
        parsed = LogLine(
            "2022-01-12T15:00:59.792831991Z: Done retrieving content for QmSeMLr3rs8xZKTk9QaxFrD9aZEVSCwuaAoE8ywots7upW error: ",
            None).is_done_retrieving()
        self.assertEqual(parsed.cid, "QmSeMLr3rs8xZKTk9QaxFrD9aZEVSCwuaAoE8ywots7upW")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:00:59.792831991Z"))
        self.assertEqual(parsed.error_str, None)
        parsed = LogLine(
            "2022-01-12T15:00:59.792831991Z: Done retrieving content for QmSeMLr3rs8xZKTk9QaxFrD9aZEVSCwuaAoE8ywots7upW error: context cancelled",
            None).is_done_retrieving()

        self.assertEqual(parsed.cid, "QmSeMLr3rs8xZKTk9QaxFrD9aZEVSCwuaAoE8ywots7upW")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:00:59.792831991Z"))
        self.assertEqual(parsed.error_str, "context cancelled")

        cid = LogLine("invalid", None).is_done_retrieving()
        self.assertEqual(cid, None)

    def test_log_is_connected_to_pvd(self):
        parsed = LogLine(
            "2022-01-12T14:51:39.40622137Z: Connected to provider 12D3KooWHpyf9LmvsWgvJF2eBQdrWdt1dphtyK1RRPwWyvLCXhJd(go-ipfs/0.10.0/9e34b227c-dirty) for cid QmQLXLLQrLeMm1ikmuDPWSjzLEJ1vc2BCeDzFUWuurGKPS from 12D3KooWR13QSmidvr9FUCo7PVP5NMx2QM6ET9ae8vV11KHtiewJ(go-ipfs/0.9.0/)",
            None).is_connected_to_pvd()
        self.assertEqual(parsed.cid, "QmQLXLLQrLeMm1ikmuDPWSjzLEJ1vc2BCeDzFUWuurGKPS")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T14:51:39.40622137Z"))
        self.assertEqual(parsed.remote_peer.id, "12D3KooWHpyf9LmvsWgvJF2eBQdrWdt1dphtyK1RRPwWyvLCXhJd")
        self.assertEqual(parsed.remote_peer.agent_version, "go-ipfs/0.10.0/9e34b227c-dirty")
        self.assertEqual(parsed.other_peer.id, "12D3KooWR13QSmidvr9FUCo7PVP5NMx2QM6ET9ae8vV11KHtiewJ")
        self.assertEqual(parsed.other_peer.agent_version, "go-ipfs/0.9.0/")

        cid = LogLine("invalid", None).is_connected_to_pvd()
        self.assertEqual(cid, None)

    def test_log_is_finish_searching_pvd(self):
        parsed = LogLine(
            "2022-01-12T15:27:21.552103081Z: Finished searching providers for cid QmRCTrxhtBJ3exC5oH952X72YZkdF4SzitqvK5M3c7oBBU ctx error: context canceled",
            None).is_finish_searching_pvd()
        self.assertEqual(parsed.cid, "QmRCTrxhtBJ3exC5oH952X72YZkdF4SzitqvK5M3c7oBBU")
        self.assertEqual(parsed.timestamp, isoparse("2022-01-12T15:27:21.552103081Z"))
        self.assertEqual(parsed.error_str, "context canceled")

        cid = LogLine("invalid", None).is_connected_to_pvd()
        self.assertEqual(cid, None)
