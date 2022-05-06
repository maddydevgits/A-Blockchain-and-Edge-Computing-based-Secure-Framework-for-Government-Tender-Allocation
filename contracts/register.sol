// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {

    address[] _username;
    uint[] _password;

    mapping(address => bool) users;

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