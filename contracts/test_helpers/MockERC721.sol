// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC721/ERC721.sol";

/// @title Mock ERC721
/// @author mymphe
/// @notice a mock ERC721 token for unit tests
contract MockERC721 is ERC721 {
    constructor() ERC721("Mock ERC721", "M721") {
        _mint(msg.sender, 0);
    }
}
