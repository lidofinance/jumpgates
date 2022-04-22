// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/ERC20.sol";

/// @title Mock ERC20
/// @author mymphe
/// @notice a mock ERC20 token for unit tests
contract MockERC20 is ERC20 {
    uint8 private immutable decimalNumber;

    constructor(uint8 _decimals) ERC20("Mock ERC20", "M20") {
        require(_decimals <= type(uint8).max);

        _mint(msg.sender, type(uint256).max);
        decimalNumber = _decimals;
    }

    function decimals() public view override returns (uint8) {
        return decimalNumber;
    }
}
