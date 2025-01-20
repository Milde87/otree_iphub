// Function to determine the IP address and send it to the server
function getAndSendIP() {
    fetch("https://api.ipify.org?format=json")
        .then(response => response.json())
        .then(data => {
            const ip = data.ip;
            // Sending the IP address to the server via livesend
            liveSend({
                type: 'ip_address',
                ip_address: ip
            });
        })
        .catch(error => {
            // Notify the backend about the error silently
            liveSend({
                type: 'error',
                error_details: error.message
            });
        });}

// Calling up the function after loading the page
document.addEventListener("DOMContentLoaded", getAndSendIP);