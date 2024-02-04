import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class RetryStrategy(object):

    @staticmethod
    def retry_mechanism(url, username=None, password=None, verify=None):

        #  Define retry strategy
        retry_strategy = Retry(
            total=4,  # Maximum number of retries
            backoff_factor=2,  # Exponential backoff factor
            status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry on
        )

        # Create an HTTP adapter with the retry strategy and mount it to session
        adapter = HTTPAdapter(max_retries=retry_strategy)

        # Create a new session object
        session = requests.Session()
        session.mount("http://", adapter)

        # Make a request using the session object
        response = session.get(url, auth=(username, password), verify=verify)

        if response.status_code == 200:
            data = response.json()
        else:
            data = {
                "message": "Failed to load movies, please try again.",
                "status_code": response.status_code,
            }
        return data
