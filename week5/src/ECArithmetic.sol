// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.0;

contract ECArithmetic {
    uint constant public MOD = 21888242871839275222246405745257275088548364400416034343698204186575808495617;
    uint constant LEN_BYTES = 32;

    struct ECPoint {
	    uint256 x;
	    uint256 y;
    }

    ECPoint G1 = ECPoint(1, 2);

    function rationalAdd(ECPoint calldata A, ECPoint calldata B, uint256 num, uint256 den) public view returns (bool verified) {
        uint multiplier = mulmod(num, inverseNum(den), MOD);
        ECPoint memory multiplierResult = getPoint(multiplier);
        ECPoint memory additionResult = addPoints(A, B);

        verified = (multiplierResult.x == additionResult.x) && (multiplierResult.y == additionResult.y);
    }

    function addPoints(ECPoint memory a, ECPoint memory b) internal view returns(ECPoint memory){
        (bool success, bytes memory data) = address(0x06).staticcall(
            abi.encodePacked(
                a.x,
                a.y,
                b.x,
                b.y
            )
        );

        require(success, "failed while ecadd");
        (uint x, uint y) = abi.decode(data, (uint, uint));

        return ECPoint(x, y);
    }

    function getPoint(uint multiplier) public view returns(ECPoint memory){
        (bool success, bytes memory data) = address(0x07).staticcall(
            abi.encodePacked(
                G1.x,
                G1.y,
                multiplier
            )
        );

        require(success, "failed while mulmod");
        (uint x, uint y) = abi.decode(data, (uint, uint));

        return ECPoint(x, y);
    }

    function multiplyPoint(ECPoint memory point, uint multiplier) internal view returns(ECPoint memory){
        (bool success, bytes memory data) = address(0x07).staticcall(
            abi.encodePacked(
                point.x,
                point.y,
                multiplier
            )
        );

        require(success, "failed while mulmod");
        (uint x, uint y) = abi.decode(data, (uint, uint));

        return ECPoint(x, y);
    }


    function inverseNum(uint num) public view returns(uint){
        bytes memory x = abi.encodePacked(
            LEN_BYTES,
            LEN_BYTES,
            LEN_BYTES,
            num,
            MOD - 2,
            MOD
        );
        (bool success, bytes memory data) = address(0x05).staticcall(x);
        require(success, "low level call failed");

        return abi.decode(data, (uint));
    }

    function multiplyMatrix(uint n, ECPoint[] calldata matrix1, uint[] calldata matrix2, ECPoint[] calldata expectedResult) public view returns (bool verified) {
        require(matrix1.length == (n * n), "invalid size for matrix1");
        require(matrix2.length == n, "invalid size for matrix2");
        require(expectedResult.length  == n, "invalid size for matrix3");
        
        ECPoint[] memory result = new ECPoint[](n);
        for(uint i=0; i<n; ++i){
            result[i] = ECPoint(0, 0);
        }


        for(uint i=0; i<n; ++i){
            for(uint j=0; j<n; ++j){
                ECPoint memory currentResult = multiplyPoint(matrix1[i * n + j], matrix2[i]);
                result[j] = addPoints(result[j], currentResult);
            }
        }

        verified = true;
        for(uint i=0; i<n; ++i){
            verified = verified && (
                (expectedResult[i].x == result[i].x) && 
                (expectedResult[i].y == result[i].y)
            );
        }
    }
}