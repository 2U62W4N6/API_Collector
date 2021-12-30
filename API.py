from abc import ABC, abstractmethod

class API(ABC):
    """
    abstract class for the different apis with all mandatory methods
    """

    @abstractmethod
    def call_api():
        """
        requesting the API Endpoint
        """
        pass

    @abstractmethod
    def _authentication():
        """
        authentication for the API Access
        """
        pass

    @abstractmethod
    def _check_authentication():
        """
        check if the authentication is successful
        """
        pass

    @abstractmethod
    def _check_limit():
        """
        overviews the rate limit and waits if needed
        """
        pass
    
    @abstractmethod
    def _pagination():
        """
        handles pagination from api endpoints who distribute their data across multiple pages
        """
        pass

    def _payload():
        """
        handles the payload of the response
        """
        pass