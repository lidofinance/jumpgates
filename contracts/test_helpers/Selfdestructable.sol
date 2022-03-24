//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

contract Selfdestructable {
    function destroy(address _recipient) public payable {
        selfdestruct(payable(_recipient));
    }
}
