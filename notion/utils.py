from urllib.parse import urlparse

def query_finder(url: str) -> dict[str, str]:
    u = urlparse(url)
    return {p[0]: p[1] for p in [q.split("=") for q in u.query.split("&")]}