import unittest
from unittest.mock import patch

import httpx

from src.http_client import build_client


class HttpClientTests(unittest.TestCase):
    def test_build_client_passes_expected_configuration_to_httpx(self) -> None:
        with patch("src.http_client.httpx.Client", autospec=True) as client_cls:
            expected_client = object()
            client_cls.return_value = expected_client

            client = build_client("https://api.example.com")

        self.assertIs(client, expected_client)
        client_cls.assert_called_once_with(
            base_url="https://api.example.com",
            headers={"Accept": "application/json"},
            timeout=httpx.Timeout(5.0, connect=1.0),
            follow_redirects=True,
        )
        self.assertIs(client_cls.call_args.kwargs["follow_redirects"], True)


if __name__ == "__main__":
    unittest.main()
