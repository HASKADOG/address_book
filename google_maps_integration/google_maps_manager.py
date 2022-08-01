import requests


class GoogleMapsManagerError(Exception):
    pass


class GoogleMapsManager:
    """
    A small lib to integrate with GMAPS.
    """

    def __init__(self, api_key: str):
        """
        Initialises GoogleMapsManager

        Params:
        api_key: str - the api key from gmaps platform/credentials
        """
        self.API_KEY = api_key

    def geocode(self, address: str) -> dict:
        """
        Uses GMAPS's geocode method to gather extended info about the address provided

        Params:
        address: str - any address you want

        Returns:
        gmaps_request: dict - contains extended info from gmaps api
        """
        params = {
            "address": address,
            "key": self.API_KEY,
        }

        gmaps_request = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json", params=params
        ).json()

        if len(gmaps_request["results"]) < 1 or gmaps_request["status"] != "OK":
            raise GoogleMapsManagerError

        return gmaps_request
