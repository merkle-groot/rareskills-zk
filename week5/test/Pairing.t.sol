// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test} from "forge-std/Test.sol";
import {Pairing} from "../src/Pairing.sol";
import {console} from "forge-std/console.sol";

contract PairingTest is Test {
    Pairing public pairing;
    function setUp() public {
        pairing = new Pairing();
    }

    function test_pairing_1() public {
        // console.log("p1", p1x, p1y);
        // test -42*7 +17*7 + 21*4 + 7*13
        // A*B + alpha*beta + X*gamma + C1*delta
        // A = - 42
        // B = 7
        // alpha = 17
        // beta = 7
        // X = 21
        // x1 = 8, x2 = 6, x3 = 7
        // gamma = 4
        // C1 = 7
        // delta = 13
        Pairing.G1Point memory alpha = getG1Point("17");
        Pairing.G2Point memory beta = getG2Point("7");
        Pairing.G2Point memory gamma = getG2Point("4");
        Pairing.G2Point memory delta = getG2Point("13");
        pairing.setPoints(alpha, beta, gamma, delta);

        Pairing.G1Point memory A = getG1Point("-42");
        Pairing.G2Point memory B = getG2Point("7");
        uint x1 = 8;
        uint x2 = 6;
        uint x3 = 7;
        Pairing.G1Point memory C = getG1Point("7");
        assertEq(pairing.pairingCheck(A, B, C, x1, x2, x3), true);
    }

    function test_pairing_2() public {
        // console.log("p1", p1x, p1y);
        // test -42*7 +7*6 + 11*3 + 9*5
        // A*B + alpha*beta + X*gamma + C1*delta
        // A = - 40
        // B = 3
        // alpha = 7
        // beta = 6
        // X = 11
        // x1 = 5, x2 = 2, x3 = 4
        // gamma = 3
        // C1 = 9
        // delta = 5
        Pairing.G1Point memory alpha = getG1Point("7");
        Pairing.G2Point memory beta = getG2Point("6");
        Pairing.G2Point memory gamma = getG2Point("3");
        Pairing.G2Point memory delta = getG2Point("5");
        pairing.setPoints(alpha, beta, gamma, delta);

        Pairing.G1Point memory A = getG1Point("-40");
        Pairing.G2Point memory B = getG2Point("3");
        uint x1 = 5;
        uint x2 = 2;
        uint x3 = 4;
        Pairing.G1Point memory C = getG1Point("9");
        assertEq(pairing.pairingCheck(A, B, C, x1, x2, x3), true);
    }

    function getG1Point(string memory multiplier) internal returns(Pairing.G1Point memory){
        string[] memory cmds = new string[](3);
        cmds[0] = "python3";
        cmds[1] = "test/ffiHelpers/g1Multiplication.py";
        cmds[2] = multiplier;

        bytes memory result = vm.ffi(cmds);

        (uint x, uint y) = abi.decode(result, (uint, uint));

        return Pairing.G1Point(x, y);
    }

    function getG2Point(string memory multiplier) internal returns(Pairing.G2Point memory){
        string[] memory cmds = new string[](3);
        cmds[0] = "python3";
        cmds[1] = "test/ffiHelpers/g2Multiplication.py";
        cmds[2] = multiplier;

        bytes memory result = vm.ffi(cmds);
        // Parse the space-separated integers from the output
        (uint x1, uint x2, uint y1, uint y2) = abi.decode(result, (uint, uint, uint, uint));
        uint[2] memory xPoints = [x1, x2];
        uint[2] memory yPoints = [y1, y2];

        return Pairing.G2Point(xPoints, yPoints);
    }
}
