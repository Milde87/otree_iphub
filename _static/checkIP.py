import requests

API_KEY = 'YourIPHubApiKey123'

def check_ip(ip_address):
    # Constructs the API endpoint URL with the provided IP address
    url = f"https://v2.api.iphub.info/ip/{ip_address}"
    headers = {
        # "X-Key": api_key  # Sets the API key in the header for authentication
        "X-Key": API_KEY
    }
    try:
        # Sends a GET request to the API
        response = requests.get(url, headers=headers)
        # Raises an exception if the response status code indicates an error
        response.raise_for_status()
        # Parses the response JSON into a dictionary
        data = response.json()
        return data  # Returns the API response data for further processing
    except requests.exceptions.HTTPError as http_err:
        # Handles specific HTTP errors (e.g., 404, 500) and prints the error message
        print(f"HTTP error: {http_err}")
    except requests.exceptions.RequestException as err:
        # Catches other request-related errors (e.g., network issues) and prints the error message
        print(f"General error: {err}")
    return None