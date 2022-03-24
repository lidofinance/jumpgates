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

    // initiates the transfer;
    function bridgeTokens() public {
        uint256 amount = token.balanceOf(address(this));
        token.approve(address(bridge), amount);

        _callBridgeTransfer(amount);
    }

    // calls the transfer on the bridge;
    // isolates the bridge-specific logic of the transfer;
    // when using a different bridge, change the body of this function
    // and leave the rest of the contract unchanged
    function _callBridgeTransfer(uint256 amount) private {
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

    // recover any ETH on this contract
    function recoverETH(address _recipient) public onlyOwner {
        (bool success, ) = _recipient.call{value: address(this).balance}("");
        require(success);
    }
}
