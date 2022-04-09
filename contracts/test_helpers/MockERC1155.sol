// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC1155/ERC1155.sol";

/// @title Mock ERC1155
/// @author mymphe
/// @notice a mock ERC1155 token for unit tests
contract MockERC1155 is ERC1155 {
    constructor() ERC1155("uri") {
        _mint(msg.sender, 0, 1, "");
    }
}
