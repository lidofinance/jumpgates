//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

contract Destrudo {
    function destructSelf(address _recipient) public payable {
        selfdestruct(payable(_recipient));
    }
}
