DarkNova is a re-write of BlackNova Traders © 2000-2020 Ron Harwood & the BNT Dev team

This version is written in Python, utilising Flask for both the backend and serving the content.
We're aiming for the content to be as modern as possible, but also simple. Pure CSS/HTML with minimal JavaScript.

TODO:
 * way too much

DONE:
 * basic integration and relationship between very simple Player, Sector and Planet classes
 * basic generation of a universe (`n` number of sectors with 0 always being 'Sol') with random unowned planets
 * basic movement of players via a query parameter
 * allowing players to take unowned planets
 
How to test it out:
 * run the Flask server
 * navigate to `/populate{?sectors=n}`; use optional sectors parameter to determine how many sectors to create
 * try `/` and whatever you type in you will log in as
 * to move to sector other than previous/next, for now: `/play?move=<sector id>`
 * to take planets `/play?take=<planet id>`
 * `/logout` to kill the simple session
 