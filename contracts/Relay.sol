//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/utils/SafeERC20.sol";
import "../interfaces/IBridge.sol";

contract Relay is Ownable {
    // tokens that are being transferred
    IERC20 public immutable token;

    // Wormhole Token Bridge
    IBridge public immutable bridge;

    // recipient address on the other side
    bytes32 public immutable recipient;

    // Wormhole id of the target chain,
    uint16 public immutable recipientChain;

    // arbiter fee
    uint256 public immutable arbiterFee;

    // nonce of the transfer
    // incremented on each transfer
    uint32 public nonce;

    constructor(
        address _token,
        address _bridge,
        uint16 _recipientChain,
        bytes32 _recipient,
        uint256 _arbiterFee
    ) {
        token = IERC20(_token);
        bridge = IBridge(_bridge);
        recipientChain = _recipientChain;
        recipient = _recipient;
        arbiterFee = _arbiterFee;
    }

    // transfers all of the `token` tokens in its possession
    // to the `recipient` on the `recipientChain` chain
    // via the Wormhole Token Bridge;
    function bridgeTokens() public {
        uint256 amount = token.balanceOf(address(this));
        token.approve(address(bridge), amount);

        bridge.transferTokens(
            address(token),
            amount,
            recipientChain,
            recipient,
            arbiterFee,
            nonce++
        );
    }

    // recover any ERC20 tokens sent to this contract
    function recoverERC20(
        address _token,
        address _recipient,
        uint256 amount
    ) public onlyOwner {
        SafeERC20.safeTransfer(IERC20(_token), _recipient, amount);
    }
}
