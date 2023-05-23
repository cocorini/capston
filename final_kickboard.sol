// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.18;

contract kickboard {

    address public owner; //소유자주소 설정
    string public coin; //토큰 이름
    string public symbol; //토큰 단위
    uint8 public decimals; //토큰 소수점 아래 단위
    //uint256 public totalSupply; //총 토큰 발행량

    mapping(address => int256) public trust_value; //신뢰점수
    mapping(address => bool) public black_list; //black list
    mapping(address => uint256) public cnt_list; //user별 사용횟수
    mapping(address => uint256) public balance; //코인 잔액
    mapping(address => bool) public isUser; //user가 존재하는 놈이라면 true로 저장.

    //modifier onlyOwner() { if(msg.sender == owner) _; }

    //생성자
    //코인 이름, 총 발행량, 코인의 단위, 소수점 아래 단위, 처음 컨트랙트 배포한 소유자도 저장함.
    constructor(string memory _coin, uint256 _supply, string memory _symbol) {
        balance[msg.sender] = _supply;
        coin = _coin;
        symbol = _symbol;
        owner = msg.sender;
    }

    //등록
    function register() public {
        isUser[msg.sender]=true;
        balance[msg.sender]=0;
        cnt_list[msg.sender]=0;
        black_list[msg.sender]=false;
        trust_value[msg.sender]=5000;
    }

    //사용횟수증가
    function addCnt() public {
        require(isUser[msg.sender]);
        cnt_list[msg.sender]+=1;
    }

    //인센티브 지급
    function incentive() payable public {
        require(isUser[msg.sender]);
        if(cnt_list[msg.sender]>=15&&cnt_list[msg.sender]%15==0&&trust_value[msg.sender]>=8000){
            balance[owner]-=1;
            balance[msg.sender]+=1;
        }
    }

    //블랙리스트->사용횟수 상관없이 3000점 보다 낮으면 벤.
    function blacklist() public {
        require(isUser[msg.sender]);
        if(trust_value[msg.sender]<=3000){
            black_list[msg.sender]=true;
        }
    }

    //신뢰점수 갱신
    function trustValue(int256 x1, int256 x2) public{
        require(isUser[msg.sender]);
        trust_value[msg.sender]+=x1*56+x2*44;
    }

    //블랙리스트에 있는지 확인
    function getBlackmember() public view returns (bool) {
        require(isUser[msg.sender]);
        return black_list[msg.sender];
    }

    //신뢰점수 반환
    function getTrustVal() public view returns (int256) {
        require(isUser[msg.sender]);
        return trust_value[msg.sender];
    }

    //지갑 잔액 반환
    function getBalance() public view returns (uint256) {
        require(isUser[msg.sender]);
        return balance[msg.sender];
    }
}