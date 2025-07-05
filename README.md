# Afunge by akalysi

Afunge is similar to befunge. Instead of a pointer being directed to various places, like in Befunge, Afunge has a controller (main) and map file. The controller is the directions for the pointer to move on the map. Documentation will be written soon.

JSON Settings:
"main": The relative or absolute path of the controller afunge file.
"map": The relative or absolute path of the map afunge file.
"tolerant": The condition of ignoring and not logging any errors.
"debugTolerant": The condition of not exiting on any errors, but still logging them.