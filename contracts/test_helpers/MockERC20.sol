// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/ERC20.sol";

/// @title Mock ERC20
/// @author mymphe
/// @notice a mock ERC20 token for unit tests
contract MockERC20 is ERC20 {
    constructor() ERC20("Mock ERC20", "M20") {
        _mint(msg.sender, 1000000000 ether);
    }
}
