# IPHub Integration for oTree 5

This document explains how to integrate the IPHub API into oTree 5. 
The tool provides functionality to check IP addresses for fraud, spam, 
or location-based restrictions.

## Installation
- Install ```requests``` in your Python environment to handle API requests.

## Setup
- Sign up for an API key from [IPHub](https://iphub.info/)
- Save your API key for use in the ```_static/checkIP.py``` script.
- Copy the provided ```ipHub.js``` and ```checkIP.py``` scripts in your ```_static``` folder
- Update the ````checkIP.py```` script with your API key:
```python
# checkIP.py
API_KEY = 'YourIPHubApiKey123'
```

## Usage
### Add Imports
In your app's ````__init__.py````, include the necessary imports:

```python
# __init__.py
from otree.api import *
from _static.checkIP import check_ip
```

### Define Player Fields
Add fields to your Player class to store IP-related data:

```python
class Player(BasePlayer):
    ip_address = models.StringField()
    ip_blocked = models.BooleanField()
    ip_country = models.StringField()
```    
    
### Create Live Method for Validation
Add a live method to validate IP addresses and process the returned data:

```python
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
```

### Redirect Based on Results
Add a page to redirect users based on the IP data:

> **Note:** Redirect pages are located in ````_static/global/redirects````. 
> Ensure you adjust the paths to align with your survey platform or hosting environment

```python
class redirect_iphub(Page):
    template_name = '_static/global/redirects/redirect_iphub.html'

    @staticmethod
    def is_displayed(player: Player):
        # Redirect if the IP is blocked or if the country is not in the allowed list
        return player.field_maybe_none('ip_blocked') in [1, None] or player.field_maybe_none('ip_country') not in ['United States', 'Germany']
```

## Help
If you have any questions, please feel free to contact me via my [homepage](https://www.studies-services.de/en).
