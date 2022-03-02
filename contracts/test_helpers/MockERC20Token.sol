//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/ERC20.sol";

contract MockERC20Token is ERC20 {
    constructor(uint256 initialSupply) ERC20("MOCK ERC20", "MCK") {
        _mint(msg.sender, initialSupply);
    }
}
