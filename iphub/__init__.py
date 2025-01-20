from otree.api import *
from _static.checkIP import check_ip

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

# FUNCTIONS


# PAGES
class MyPage(Page):
    @staticmethod
    def live_method(player, data):
        # Check if the received data type is 'ip_address'
        if data['type'] == 'ip_address':
            # Save the participant's IP address
            player.ip_address = data['ip_address']
            # Use the check_ip function to validate the IP and retrieve details
            ip_data = check_ip(player.ip_address)
            # Save whether the IP is blocked
            player.ip_blocked = ip_data.get("block")
            # Save the country associated with the IP address
            player.ip_country = ip_data.get("countryName")
        elif data['type'] == 'error':
            # Handle cases where retrieving the IP address fails
            player.ip_address = 'Error'


class redirect_iphub(Page):
    template_name = '_static/global/redirects/redirect_iphub.html'

    @staticmethod
    def is_displayed(player: Player):
        # Redirect if the IP is blocked or if the country is not in the allowed list
        return player.field_maybe_none('ip_blocked') in [1, None] or player.field_maybe_none('ip_country') not in ['United States', 'Germany']



class Results(Page):
    pass


class redirect_complete(Page):
    template_name = '_static/global/redirects/redirect_complete.html'


page_sequence = [MyPage, redirect_iphub, Results, redirect_complete]
