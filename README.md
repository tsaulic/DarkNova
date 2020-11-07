DarkNova is a re-write of BlackNova Traders © 2000-2020 Ron Harwood & the BNT Dev team

This version is written in Python, utilising Flask for both the backend and serving the content.
We're aiming for the content to be as modern as possible, but also simple. Pure CSS/HTML with minimal JavaScript.

TODO:
 * pretty much everything at this point :D
 
DONE:
 * basic integration and relationship between very simple Player and Sector classes
 * basic generation of a universe (`n` number of sectors with 0 always being 'Sol')
 * basic movement of players via a query parameter
 
How to test it out:
 * run the Flask server
 * navigate to `/populate{?sectors=n}` with optional number of sectors parameter
 * try `/?player=Test` and to move `/?player=Test&move=n`
 