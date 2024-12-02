import os


def get_sqlite_uri():
    host = os.environ.get("DB_HOST", "/user.db")
    return f"sqlite://{host}"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"
