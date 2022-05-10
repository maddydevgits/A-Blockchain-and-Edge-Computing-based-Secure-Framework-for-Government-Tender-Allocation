// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {

    address[] _username;
    uint[] _password;

    address[] _bidusername;
    uint[] _bidpassword;
    string[] _bidemail;

    mapping(address => bool) users;
    mapping(address => bool) bidUsers;

    function registerBidUser(address username,uint password,string memory email) public {
        
        require(!bidUsers[username]);

        bidUsers[username]=true;
        _bidusername.push(username);
        _bidpassword.push(password);
        _bidemail.push(email);

    }

    function loginBidUser(address username,uint password) public view returns(string memory){

        uint i=0;
        require(bidUsers[username]);

        for(i=0;i<_bidusername.length;i++) {
            if(_bidusername[i]==username && _bidpassword[i]==password) {
                return _bidemail[i];
            }
        }
        return "";
    }

    function registerUser(address username,uint password) public {

        require(!users[username]);

        users[username]=true;
        _username.push(username);
        _password.push(password);
    }

    function loginUser(address username,uint password) public view returns(bool){

        uint i=0;
        require(users[username]);

        for(i=0;i<_username.length;i++) {
            if(_username[i]==username && _password[i]==password) {
                return true;
            }
        }
        return false;
    }
}