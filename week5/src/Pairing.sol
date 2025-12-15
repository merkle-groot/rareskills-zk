// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";


contract Pairing is Ownable {
    uint constant public MOD = 21888242871839275222246405745257275088548364400416034343698204186575808495617;
    uint constant LEN_BYTES = 32;
    
    struct G1Point {
	    uint x;
	    uint y;
    }

    struct G2Point {
        uint[2] x;
        uint[2] y;
    }

    G1Point G1 = G1Point(1, 2);
    G1Point alpha;
    G2Point beta = G2Point([uint(0), 0], [uint(0), 0]);
    G2Point gamma = G2Point([uint(0), 0], [uint(0), 0]);
    G2Point delta = G2Point([uint(0), 0], [uint(0), 0]);

    constructor() Ownable(msg.sender){}

    function setPoints(G1Point memory _alpha, G2Point memory _beta, G2Point memory _gamma, G2Point memory _delta) external onlyOwner{
        alpha = _alpha;
        beta = _beta;
        gamma = _gamma;
        delta = _delta;
    }

    function pairingCheck(G1Point calldata A, G2Point calldata B, G1Point calldata C, uint x1, uint x2, uint x3) external returns(bool) {
        G1Point memory X = calcXPoint(x1, x2, x3);

        return verifyPairing(A, B, alpha, beta, X, gamma, C, delta);
    }

    function calcXPoint(uint x1, uint x2, uint x3) internal returns(G1Point memory){
        G1Point memory X1 = g1Mul(G1, x1);
        G1Point memory X2 = g1Mul(G1, x2);
        G1Point memory X3 = g1Mul(G1, x3);

        G1Point memory X12 = g1Add(X1, X2);
        return g1Add(X3, X12);
    }

    function g1Add(G1Point memory a, G1Point memory b) internal view returns(G1Point memory){
        (bool success, bytes memory data) = address(0x06).staticcall(abi.encodePacked(a.x, a.y, b.x, b.y));
        require(success, "failed to do G1 add");
        (uint x, uint y) = abi.decode(data, (uint, uint));

        return G1Point(x, y);
    }

    function g1Mul(G1Point memory a, uint multiplier) internal view returns(G1Point memory){
        (bool sucess, bytes memory data) = address(0x07).staticcall(abi.encodePacked(a.x, a.y, multiplier));
        require(sucess, "failed to do G1 mul");
        (uint x, uint y) = abi.decode(data, (uint, uint));

        return G1Point(x, y);
    }

    function verifyPairing(
        G1Point memory a, 
        G2Point memory b, 
        G1Point memory c, 
        G2Point memory d, 
        G1Point memory e, 
        G2Point memory f, 
        G1Point memory g, 
        G2Point memory h
    ) internal view returns (bool) {

        bytes memory inputPairing;

        {
            inputPairing = abi.encodePacked(
                a.x, a.y, b.x[1], b.x[0], b.y[1], b.y[0],
                c.x, c.y, d.x[1], d.x[0], d.y[1], d.y[0]
            );
        }

        {
            bytes memory rest = abi.encodePacked(
                e.x, e.y, f.x[1], f.x[0], f.y[1], f.y[0],
                g.x, g.y, h.x[1], h.x[0], h.y[1], h.y[0]
            );
            inputPairing = bytes.concat(inputPairing, rest);
        }

        (bool success, bytes memory data) = address(0x08).staticcall(inputPairing);

        require(success, "failed to get pairing verification");
        bool verified = abi.decode(data, (bool));
        return verified;
    }
}
