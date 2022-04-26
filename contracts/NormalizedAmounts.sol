// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.13;

/// @title Normalized Amounts
/// @author mymphe
/// @notice normalize and denormalize amounts for safer transfers via Wormhole
/// @dev Wormhole Token Bridge normalizes transfer amount to 8 decimals
library NormalizedAmounts {
    function normalize(uint256 amount, uint8 decimals)
        internal
        pure
        returns (uint256)
    {
        if (decimals > 8) {
            amount /= 10**(decimals - 8);
        }
        return amount;
    }

    function denormalize(uint256 amount, uint8 decimals)
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
