Going down for Maintenance
==========================
Before the server or client can be updated, players must notified of the
impending downtime, disconnected from the game, and logins must be disabled.
This describes the process of *going down for maintenance*, and is the first
step in the deployment process.

- - -

## The Process ##
1. Going down for maintenance
2. [Updating the server](01-server.md)
3. [Updating the client](02-client.md)

- - -

## Module Requirements ##
The following is a list of Python modules that are required to run the
```maintenance.py``` script:
* **PyCrypto** - A package containing various cryptographic modules.
* **JSONRPClib** - An implementation of the JSON-RPC specification

## Configuration Requirements ##
The following is a list of configuration variables that must be present in the
```deployment/deploy.json``` configuration file:
* **maintenance-countdown-duration** - The duration (in minutes) of the
                                       maintenance countdown.
* **maintenance-lock-time** - The minute during the countdown at which the
                              account server will begin to reject login
                              attempts by accounts of the ```user``` access
                              level.
* **maintenance-lock-message** - The message to display upon login rejection
                                 by the account server. If this is ```null```
                                 then the default message will be used.
* **game-rpc-endpoint** - The game server's RPC endpoint.
* **game-rpc-token-secret** - The secret key that will be used to encrypt the
                              access tokens that are generated in calls to the
                              game server's RPC methods.
* **web-rpc-endpoint** - The web server's RPC endpoint.
* **web-rpc-token-secret** - The secret key that will be used to encrypt the
                             access tokens that are generated in calls to the
                             web server's RPC methods.

- - -

## Running the Script ##
To begin the maintenance process, simply run a command similar to the
following:
* On Windows: ```python deployment/maintenance.py```
* On Linux: ```./deployment/maintenance.py```
