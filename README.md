# clach04.keyring.dumbserver

Insecure, terrible, keyring backend - similar to jaraco.keyring Remote Agent Keyring.. just way worse
Similar intent to https://github.com/jaraco/jaraco.keyring but just for a local machine over regular http (on a tcp socket, not a domain socket).

Current backends:

  * SimpleKeyring
  * DumbServer


## SimpleKeyring

    python -m keyring -b clach04.keyring.SimpleKeyring get testsvc testuser

## DumbServer

NOTE **not** 100% implemented yet.

    python -m clach04.keyring.dumbserver
    python -m keyring -b clach04.keyring.DumbServer get testsvc testuser
