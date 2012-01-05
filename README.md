Description
===========
B3EF is the Battlefield 3 enhancement framework. It enables python developers to respond to events that are sent by
a Battlefield 3 server. Additionally it provides Battlelog integration to allow easy access to player stats.

Requirements
===========
    *Python 2.7


Included modules
===========
B3EF comes prepackaged with four modules:

 * Mapsettings:
  Create tailor-made settings for each and every map/mode combination in your rotation. You can specify your desired
  settings, allowed weapons and announcements for a map/mode combination. This module will take care of altering and
  resetting the server settings and enforcing weapon restrictions in a way that does not interrupt gameplay.

 * Votekick/Voteban

 * Min/Max Rank enforcer
  Limit the allowed minimum or maximum rank on your server

 * Killstreak announcer

Moreover the `punisher` and `playerlist` module provide a simple interface for handling punishment and the playerlist

To include these modules just uncomment their name in the `main.ini`
Config files for individual modules are located at `/configs`

How to launch B3EF
===========
`main.py -ip SERVER_IP_ADDRESS -port SERVER_QUERY_PORT -pw RCON_PASSWORD (optional)-bqu BATTLELOG_EMAIL (optional)-bqp BATTLELOG_PASSWORD`

Example:
`main.py -ip 85.14.232.194 -port 47200 -pw mypass -bqu example@example.com -bqp examplepw`