// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

library SafeAmounts {
    function normalizeAmount(uint256 amount, uint8 decimals)
        internal
        pure
        returns (uint256)
    {
        if (decimals > 8) {
            amount /= 10**(decimals - 8);
        }
        return amount;
    }

    function denormalizeAmount(uint256 amount, uint8 decimals)
        internal
        pure
        returns (uint256)
    {
        if (decimals > 8) {
            amount *= 10**(decimals - 8);
        }
        return amount;
    }
}
