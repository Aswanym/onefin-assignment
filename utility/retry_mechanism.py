import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class RetryStrategy(object):
    """
        A class providing a retry mechanism for making HTTP requests with exponential backoff.

        Usage:
        ------
        To use the retry mechanism, create an instance of this class and call the
        `retry_mechanism` method with the desired parameters.

        Example:
        --------
        ```python
        retry_strategy = RetryStrategy()
        response_data = retry_strategy.retry_mechanism(
            url='https://example.com/api/data',
            username='your_username',
            password='your_password',
            verify='path/to/certificate.pem'
        )
        ```

        Attributes:
        -----------
        None

        Methods:
        --------
        retry_mechanism(url, username=None, password=None, verify=None):
            Performs an HTTP GET request to the specified URL with retry logic based on
            predefined retry strategy parameters.

        """

    @staticmethod
    def retry_mechanism(url, username=None, password=None, verify=None):

        """
                Performs an HTTP GET request to the specified URL with retry logic based on
                predefined retry strategy parameters.

                Parameters:
                -----------
                url (str): The URL to make the HTTP request to.
                username (str, optional): The username for authentication.
                password (str, optional): The password for authentication.
                verify (str, optional): Path to the CA certificate file for SSL verification.

                Returns:
                --------
                dict: A dictionary containing the response data. If the request is successful (HTTP status code 200),
                the response data is parsed from JSON. Otherwise, a dictionary with an error message and status code is returned.

                """

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
