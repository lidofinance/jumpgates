# Cross-chain Token Jumpgate 🌀

Jumpgates are a class of contracts that streamline cross-chain token transfers under the Lido DAO. Although autonomous, jumpgates are meant to be part of the Easy Track Rewards Program pipeline.

## What is a jumpgate?

A jumpgate is a launching point for token bridges such as Wormhole, Terra Shuttle, etc. Each individual jumpgate carries only one type of tokens to a single cross-chain recipient through a pre-determined bridge. Jumpgate activation is performed manually by executing a permissionless transaction.

Read ADR: https://hackmd.io/snwPWGqBS-ax5Ur0A5Ix5w?view

## Development

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```
