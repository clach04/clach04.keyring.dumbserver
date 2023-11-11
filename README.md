# clach04.keyring.dumbserver

Insecure, terrible, [keyring backend](https://github.com/jaraco/keyring) - similar to jaraco.keyring Remote Agent Keyring.. just way worse
Similar intent to https://github.com/jaraco/jaraco.keyring but just for a local machine over regular http (on a tcp socket, not a domain socket).

Current backends:

  * SimpleKeyring - can store only one password in memory, both service and username are **ignored**
  * DumbServer - Accesses local http server (currently hard coded)
      * a demo http only (no https support) server `dumbserver` is included which only listens to requests from local machine and only supports one password (both service and username are **ignored**) - this is unsafe on a shared machine, and probably unsafe in general 😉


## SimpleKeyring

    python -m keyring -b clach04.keyring.SimpleKeyring get testsvc testuser

## DumbServer

NOTE **not** 100% implemented yet.

    python -m clach04.keyring.dumbserver
    python -m keyring -b clach04.keyring.DumbServer get testsvc testuser
