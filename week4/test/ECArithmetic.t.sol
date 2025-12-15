// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test} from "forge-std/Test.sol";
import {ECArithmetic} from "../src/ECArithmetic.sol";
import {console} from "forge-std/console.sol";

contract ECArithmeticTest is Test {
    ECArithmetic public ecContract;

    function setUp() public {
        ecContract = new ECArithmetic();
    }

    function testRationalAdd() public view {
        // test1
        // LHS: 5G + 7G = 12G
        // RHS: 2G * inverse of 40128445265038671240785077199638337662338668067429396296780041008722315575298 = 12G

        ECArithmetic.ECPoint memory A = ecContract.getPoint(5);
        ECArithmetic.ECPoint memory B = ecContract.getPoint(7);
        uint num = 2;
        uint den = 40128445265038671240785077199638337662338668067429396296780041008722315575298;

        assertEq(mulmod(ecContract.inverseNum(den), num, ecContract.MOD()), 12);
        assertEq(ecContract.rationalAdd(A, B, num, den), true);
    }

    function testRationalAdd2() public view {
        // test2
        // LHS: 42G + 37G = 79G
        // RHS: 23G * inverse of 11636787349585437459928468877225386755937105124271815727029425010584607048303 = 79G

        ECArithmetic.ECPoint memory A = ecContract.getPoint(42);
        ECArithmetic.ECPoint memory B = ecContract.getPoint(37);
        uint num = 23;
        uint den = 11636787349585437459928468877225386755937105124271815727029425010584607048303;

        assertEq(mulmod(ecContract.inverseNum(den), num, ecContract.MOD()), 79);
        assertEq(ecContract.rationalAdd(A, B, num, den), true);
    }    

    function testMatrix2x2() public view {
        // test1
        // LHS: matrix1 = [1, 2, 3, 4] matrix 2 = [1, 2]
        // result: [7, 10] = (1*1 + 2*3)G, (2*1 + 4*2)G

        // 2x2 matrix
        uint n = 2;
        ECArithmetic.ECPoint[] memory matrix1 =  new ECArithmetic.ECPoint[](n*n);
        matrix1[0] = ecContract.getPoint(1);
        matrix1[1] = ecContract.getPoint(2);
        matrix1[2] = ecContract.getPoint(3);
        matrix1[3] = ecContract.getPoint(4);

        uint[] memory matrix2 = new uint[](n);
        matrix2[0] = 1;
        matrix2[1] = 2;

        ECArithmetic.ECPoint[] memory expectedResult =  new ECArithmetic.ECPoint[](n);
        expectedResult[0] = ecContract.getPoint(7);
        expectedResult[1] = ecContract.getPoint(10);

        assertEq(ecContract.multiplyMatrix(n, matrix1, matrix2, expectedResult), true);
    }

    function testMatrix3x3() public view {
        // test1
        // LHS: matrix1 = [1, 2, 3, 4, 5, 6, 7, 8, 9] matrix2 = [1, 2, 3]
        // result: [30, 36, 42] 

        // 3x3 matrix
        uint n = 3;
        ECArithmetic.ECPoint[] memory matrix1 =  new ECArithmetic.ECPoint[](n*n);
        matrix1[0] = ecContract.getPoint(1);
        matrix1[1] = ecContract.getPoint(2);
        matrix1[2] = ecContract.getPoint(3);
        matrix1[3] = ecContract.getPoint(4);
        matrix1[4] = ecContract.getPoint(5);
        matrix1[5] = ecContract.getPoint(6);
        matrix1[6] = ecContract.getPoint(7);
        matrix1[7] = ecContract.getPoint(8);
        matrix1[8] = ecContract.getPoint(9);

        uint[] memory matrix2 = new uint[](n);
        matrix2[0] = 1;
        matrix2[1] = 2;
        matrix2[2] = 3;

        ECArithmetic.ECPoint[] memory expectedResult =  new ECArithmetic.ECPoint[](n);
        expectedResult[0] = ecContract.getPoint(30);
        expectedResult[1] = ecContract.getPoint(36);
        expectedResult[2] = ecContract.getPoint(42);

        assertEq(ecContract.multiplyMatrix(n, matrix1, matrix2, expectedResult), true);
    }
}