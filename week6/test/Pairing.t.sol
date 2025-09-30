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

    function test_pairing() public {
        (uint p1x, uint p1y) = getG1Point("-2");
        // console.log("p1", p1x, p1y);
        Pairing.G1Point memory p1 = Pairing.G1Point(p1x, p1y);

        (uint[] memory p2x, uint[] memory p2y) = getG2Point("6");
        // console.log("p2.x0", p2x[0]);
        // console.log("p2.x1", p2x[1]);
        // console.log("p2.y0", p2y[0]);
        // console.log("p2.y1", p2y[1]);
        Pairing.G2Point memory p2 = Pairing.G2Point(p2x, p2y);

        (uint q1x, uint q1y) = getG1Point("4");
        // console.log("q1", q1x, q1y);
        Pairing.G1Point memory q1 = Pairing.G1Point(q1x, q1y);

        (uint[] memory q2x, uint[] memory q2y) = getG2Point("3");
        // console.log("q2", q2x, q2y);
        Pairing.G2Point memory q2 = Pairing.G2Point(q2x, q2y);

        assertEq(pairing.pairingCheck(p1, p2, q1, q2), true);
    }

    function getG1Point(string memory multiplier) internal returns(uint x, uint y){
        string[] memory cmds = new string[](3);
        cmds[0] = "python3";
        cmds[1] = "test/ffiHelpers/g1Multiplication.py";
        cmds[2] = multiplier;

        bytes memory result = vm.ffi(cmds);

        (x, y) = abi.decode(result, (uint, uint));
    }

    function getG2Point(string memory multiplier) internal returns(uint[] memory xPoints, uint[] memory yPoints){
        string[] memory cmds = new string[](3);
        cmds[0] = "python3";
        cmds[1] = "test/ffiHelpers/g2Multiplication.py";
        cmds[2] = multiplier;

        bytes memory result = vm.ffi(cmds);
        // Parse the space-separated integers from the output
        (uint x1, uint x2, uint y1, uint y2) = abi.decode(result, (uint, uint, uint, uint));
        xPoints = new uint[](2);
        xPoints[0] = x1;
        xPoints[1] = x2;

        yPoints = new uint[](2);
        yPoints[0] = y1;
        yPoints[1] = y2;
    }
}
