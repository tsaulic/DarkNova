DarkNova is a re-write of BlackNova Traders © 2000-2020 Ron Harwood & the BNT Dev team

This version is written in Python for backend, utilising Flask for serving the content.
I'm aiming for the UI to be as modern as possible, but also simple. Pure CSS/HTML with minimal JavaScript for client.

**TODO** (way too much, but still, here's a list in a rough order of priority):

 * ship modules/credits
 * special port shop
 * manual trading in ports
 * real-space movement which is dependent on engine level and universe size
 * trade routes; warp/real-space trading using the routes
 * planet bases and resources
 * handle planets resources in update scheduler
 * ship to ship combat
 * ship to planet combat
 * sector defences
 * alliances
 * IGB
 * news
 * rankings with online status/efficiency
 * more stuff coming, there's just so much
 * chat-box (if I can integrate some anti-spam service)

**DONE**:

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
 * sector warp links
 * add random warp links
 
How to test it out:
 * run the Flask server
 * navigate to `/populate{?sectors=n}`; use optional sectors parameter to determine how many sectors to create (default is 1000)
 * try `/` and whatever player name and ship you use it will created that player for you
 * `/logout` to kill the simple session or if you want to create a new account for now
 
