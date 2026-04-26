import httpx


def build_client(base_url: str) -> httpx.Client:
    return httpx.Client(
        base_url=base_url,
        headers={"Accept": "application/json"},
        timeout=httpx.Timeout(5.0, connect=1.0),
        follow_redirects=True,
    )
