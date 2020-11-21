DarkNova is a re-write of BlackNova Traders © 2000-2020 Ron Harwood & the BNT Dev team

This version is written in Python for backend, utilising Flask for serving the content.
We're aiming for the content to be as modern as possible, but also simple. Pure CSS/HTML with minimal JavaScript for client.

TODO (way too much, but still, here's a list in a rough order of priority):

 * sector warp links
 * ship modules/credits
 * manual trading in ports
 * trade routes; warp/realspace trading using the routes
 * planet bases
 * handle planets resources in update scheduler
 * ship to ship combat
 * ship to planet combat
 * sector defences
 * alliances
 * IGB
 * news
 * chatbox (may not allow if too much spam is posted)
 * rankings with online status/efficiency
 * more stuff coming, there's just so much

DONE:
 * basic integration and relationship between very simple Player, Sector and Planet classes
 * basic generation of a universe (`n` number of sectors with 0 always being 'Sol') with random unowned planets
 * basic movement of players via a query parameter
 * movement to a desired sector via a form label and button
 * allowing players to take unowned planets
 * beacon support in sector class; display beacon in the UI
 * showing ships in sector (currently unaffected by cloak as cloak is not implemented)
 * generation of basic ports which currently do nothing (distribution of certain ports needs to be tweaked); displaying ports in sector in the UI
 * turns/use turns for actions
 * handle turn cap via config
 * turn update scheduler
 * display scheduler countdown
 * animate countdown with JavaScript
 
How to test it out:
 * run the Flask server
 * navigate to `/populate{?sectors=n}`; use optional sectors parameter to determine how many sectors to create
 * try `/` and whatever you type in you will log in as
 * to move to sector other than previous/next, for now: `/play?move=<sector id>`
 * to take planets `/play?take=<planet id>`
 * `/logout` to kill the simple session
 
