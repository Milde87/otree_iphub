from otree.api import *
import requests

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'iphub'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ip_address = models.StringField()
    ip_blocked = models.BooleanField()
    ip_country = models.StringField()
    ip_test_live = models.BooleanField(initial=False)
    gender = models.IntegerField(
        label="Are you female, male or non-binary?",
        choices=[
            [0, 'female'],
            [1, 'male'],
            [2, 'non-binary'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        #initial=0
    )
    age = models.IntegerField(
        min=18,
        max=120,
        label="How old are you?",
        blank=False,
        #initial=35,
    )
# FUNCTIONS
def check_ip(ip_address):
    # Constructs the API endpoint URL with the provided IP address
    url = f"https://v2.api.iphub.info/ip/{ip_address}"
    headers = {
        # "X-Key": api_key  # Sets the API key in the header for authentication
        "X-Key": 'MjYxODc6aHU5VlZES3Z0U3NIM0U4SjRnVGJ1UFJGQks1MmJYT1E='
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

# PAGES
class MyPage(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return ['gender', 'age']

    @staticmethod
    def live_method(player, data):
        # Check if the incoming data type is 'ip_address'
        if data['type'] == 'ip_address':
            player.ip_test_live = True
            # Saves the IP address of the subscriber
            player.ip_address = data['ip_address']
            ip_data = check_ip(player.ip_address)
            player.ip_blocked = ip_data.get("block")
            player.ip_country = ip_data.get("countryName")
        elif data['type'] == 'error':
            player.ip_address = data['error_details']

class Results(Page):
    pass


class redirect_complete(Page):
    template_name = '_static/global/redirects/redirect_complete.html'

page_sequence = [MyPage, Results]
