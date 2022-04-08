//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "../Jumpgate.sol";

contract JumpgateFactory {
    event JumpgateCreated(
        address indexed _jumpgate,
        address indexed _token,
        address indexed _bridge,
        uint16 _recipientChain,
        bytes32 _recipient,
        uint256 _arbiterFee
    );

    function createJumpgate(
        address _token,
        address _bridge,
        uint16 _recipientChain,
        bytes32 _recipient,
        uint256 _arbiterFee
    ) public {
        new Jumpgate(
            msg.sender,
            _token,
            _bridge,
            _recipientChain,
            _recipient,
            _arbiterFee
        );
    }
}
