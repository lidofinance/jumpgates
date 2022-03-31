![logo](img/logo.png?raw=true | width=200px)

# JUMPGATES

Jumpgates streamline cross-chain token transfers under the Lido DAO incentive programs. Although autonomous, jumpgates are meant to be part of the Easy Track Rewards Program pipeline.

## What is a jumpgate?

A jumpgate is a contract that serves as a launching point for token transportation via token bridges such as Wormhole, Terra Shuttle, etc. Each individual jumpgate carries only one type of tokens to a single cross-chain recipient through a pre-determined bridge. Jumpgate activation is performed manually by executing a permissionless transaction.

Read ADR: https://hackmd.io/snwPWGqBS-ax5Ur0A5Ix5w?view

## How do jumpgates work?

Jumpgates are the primary way for cross-chain token transfers under the Lido DAO. Each jumpgate is registered as an Easy Track Reward Program. The DAO then allocates the tokens bound for the cross-chain recipient to an appropriate jumpgate via an Easy Track motion. A permissionless function on the jumpgate is invoked transporting the tokens through the token bridge. And, finally, the tokens are redeemed on the target blockchain.

## Development

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```
