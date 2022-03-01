//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/access/Ownable.sol";
import "./Relay.sol";

contract RelayFactory {
    // deploys a new Relay contract
    function deployRelay(
        address _token,
        address _bridge,
        uint16 _recipientChain,
        bytes32 _recipient,
        uint256 _arbiterFee
    ) public {
        new Relay(_token, _bridge, _recipientChain, _recipient, _arbiterFee);
    }
}
