// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract Pairing {
    uint constant public MOD = 21888242871839275222246405745257275088548364400416034343698204186575808495617;
    uint constant LEN_BYTES = 32;
    
    struct G1Point {
	    uint x;
	    uint y;
    }

    struct G2Point {
        uint[] x;
        uint[] y;
    }

    G1Point G1 = G1Point(1, 2);

    function pairingCheck(G1Point calldata a, G2Point calldata b, G1Point calldata c, G2Point calldata d) external view returns (bool verified) {
        bytes memory inputPairing = abi.encodePacked(a.x, a.y, b.x[1], b.x[0], b.y[1], b.y[0], c.x, c.y, d.x[1], d.x[0], d.y[1], d.y[0]);
        (bool success, bytes memory data) = address(0x08).staticcall(inputPairing);

        require(success, "failed to get pairing verification");

        verified = abi.decode(data, (bool));
    }

    // function increment() public {
    //     number++;
    // }
}
