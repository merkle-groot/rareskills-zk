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
        pairing.G1Point = G1Point();
    }

    function test_getG1Point() public returns(pairing.G1Point){
        string[] memory cmds = new string[](3);
        cmds[0] = "python3";
        cmds[1] = "test/ffiHelpers/g1Multiplication.py";
        cmds[2] = "2";

        bytes memory result = vm.ffi(cmds);

        (uint x, uint y) = abi.decode(result, (uint, uint));

        return G1Point(x, y);
    }

    function test_getG2Point() public returns(pairing.G2Point){
        string[] memory cmds = new string[](3);
        cmds[0] = "python3";
        cmds[1] = "test/ffiHelpers/g2Multiplication.py";
        cmds[2] = "2";

        bytes memory result = vm.ffi(cmds);
        // Parse the space-separated integers from the output
        (uint x1, uint x2, uint y1, uint y2) = abi.decode(result, (uint, uint, uint, uint));
        uint[] xPoints = new uint[](2);
        xPoints.push(x1);
        xPoints.push(x2);

        uint[] yPoints = new uint[](2);
        yPoints.push(y1);
        yPoints.push(y2);

        return G2Point(xPoints, yPoints);
    }
}
