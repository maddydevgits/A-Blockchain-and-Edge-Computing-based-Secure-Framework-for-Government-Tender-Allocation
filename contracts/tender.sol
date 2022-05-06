// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract tender {
    
    address[] _tenderOwner;
    uint[] _tenderId;
    string[] _tenderData;
    bool[] _tenderState;
    address[] _tenderBidder;

    uint[] _bidTenderId;
    uint[] _bidAmount;
    string[] _bidEmail;
    address[] _bidders;
    
    mapping(uint => bool) public tId;
    mapping(address =>bool) public bidders;

    function createTender(address tenderOwner,uint tenderId,string memory tenderData) public {

        require(!tId[tenderId]);

        tId[tenderId]=true;
        _tenderOwner.push(tenderOwner);
        _tenderId.push(tenderId);
        _tenderData.push(tenderData);
        _tenderState.push(false);
    }

    function getTender(uint tenderId) public view returns (address,uint,string memory) {
        
        require(tId[tenderId]);
        uint i=0;

        if(_tenderId.length>0) {
            for(i=0;i<_tenderId.length;i++) {
                if(_tenderId[i]==tenderId) {
                    return (_tenderOwner[i],_tenderId[i],_tenderData[i]);
                }
            }
        }
        return (msg.sender,0,'NA');
    }

    function viewTenders() public view returns(address[] memory,uint[] memory, string[] memory,bool[] memory,address[] memory) {

        return(_tenderOwner,_tenderId,_tenderData,_tenderState,_tenderBidder);
    }

    function bidTender(uint bidTenderId,uint bidAmount,string memory bidEmail) public {

        _bidAmount.push(bidAmount);
        _bidders.push(msg.sender);
        _bidTenderId.push(bidTenderId);
        _bidEmail.push(bidEmail);

    }

    function viewBids() public view returns(uint[] memory,string[] memory,address[] memory,uint[] memory) {

        return (_bidTenderId,_bidEmail,_bidders,_bidAmount);
    }

    function allocateTender(uint tenderId,address bidOwner) public {

        uint i;
        for(i=0;i<_tenderId.length;i++) {
            if(_tenderId[i]==tenderId) {
                _tenderState[i]==true;
                _tenderBidder[i]=bidOwner;
            }
        }
    }
}
