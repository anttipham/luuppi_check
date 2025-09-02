# Luuppi Check

The Luuppi websites are always overwhelmed by the number of people refreshing the site when an event ticket starts. Thus, I developed a script that can communicate directly with the API of the website.
This way the user does not need to wait for the front end and all of the ticket availability checks and can buy the tickets almost instantly.

The script was developed by reading the HTTP requests of the browser.

The script is given the event ID, selling time of the event, and browser cookies as the input.
The script then adds the event ticket to the cart when the tickets become available. The user can then pay for the tickets in 30 minutes to secure them.
