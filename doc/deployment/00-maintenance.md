Going down for Maintenance
==========================
Before the server or client can be updated, players must notified of the
impending downtime and disconnected from the game, and logins must be disabled.
This describes the process of *going down for maintenance*, and is the first
step in the deployment process.

- - -

## The Process ##
1. Going down for maintenance
2. [Updating the server](01-server.md)
3. [Updating the client](02-client.md)

- - -

## Configuration Requirements ##
The following is a list of configuration variables that must be present in the
```deployment/deploy.json``` configuration file:
* **maintenance-countdown-duration** - The duration (in minutes) of the
                                       maintenance countdown.
* **gameserver-rpc-endpoint** - The game server's RPC endpoint URL.
* **gameserver-rpc-token-secret** - The secret key that will be used to encrypt
                                    the access tokens that are generated in
                                    calls to the game server's RPC methods.
* **webserver-rpc-endpoint** - The web server's RPC endpoint URL.
* **webserver-rpc-token-secret** - The secret key that will be used to encrypt
                                   the access tokens that are generated in
                                   calls to the web server's RPC methods.

- - -

## Running the Script ##
To begin the maintenance process, simply run a command similar to the
following:
* On Windows: ```ppython deployment/maintenance.py```
* On Linux: ```./deployment/maintenance.py```
