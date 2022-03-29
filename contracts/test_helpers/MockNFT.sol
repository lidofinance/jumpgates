//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC721/ERC721.sol";

contract MockNFT is ERC721 {
    constructor() ERC721("MOCK NFT", "MNFT") {
        _mint(msg.sender, 0);
    }
}
