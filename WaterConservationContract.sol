pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract WaterConservationToken is ERC20, Ownable {
    constructor(uint256 initialSupply) ERC20("WaterSaver", "WTR") {
        _mint(msg.sender, initialSupply);
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
}

contract WaterConservationContract is Ownable {
    WaterConservationToken public token;

    struct WaterUsage {
        uint256 timestamp;
        uint256 floor;
        uint256 unit;
        uint256 waterUsage;  // in liters
    }

    struct UnitInfo {
        uint256 monthlyLimit;
        uint256 currentMonthUsage;
        uint256 lastResetTimestamp;
    }

    struct IssueReport {
        uint256 timestamp;
        uint256 floor;
        uint256 unit;
        string description;
        bool resolved;
    }

    mapping(uint256 => mapping(uint256 => UnitInfo)) public unitInfos;  // floor => unit => UnitInfo
    WaterUsage[] public waterUsageRecords;
    IssueReport[] public issueReports;

    event WaterUsageRecorded(uint256 timestamp, uint256 floor, uint256 unit, uint256 waterUsage);
    event LimitExceeded(uint256 timestamp, uint256 floor, uint256 unit, uint256 currentUsage, uint256 limit);
    event IssueReported(uint256 timestamp, uint256 floor, uint256 unit, string description);
    event IssueResolved(uint256 issueId);

    constructor(address _tokenAddress) {
        token = WaterConservationToken(_tokenAddress);
    }

    function recordWaterUsage(uint256 _floor, uint256 _unit, uint256 _waterUsage) public onlyOwner {
        uint256 timestamp = block.timestamp;
        waterUsageRecords.push(WaterUsage(timestamp, _floor, _unit, _waterUsage));

        UnitInfo storage unitInfo = unitInfos[_floor][_unit];
        
        // Reset monthly usage if it's a new month
        if (timestamp - unitInfo.lastResetTimestamp >= 30 days) {
            unitInfo.currentMonthUsage = 0;
            unitInfo.lastResetTimestamp = timestamp;
        }

        unitInfo.currentMonthUsage += _waterUsage;

        // Check if the usage exceeds the limit
        if (unitInfo.currentMonthUsage > unitInfo.monthlyLimit) {
            emit LimitExceeded(timestamp, _floor, _unit, unitInfo.currentMonthUsage, unitInfo.monthlyLimit);
        } else {
            // Reward token for staying under the limit
            token.mint(msg.sender, 1 * 10**18);  // Mint 1 token
        }

        emit WaterUsageRecorded(timestamp, _floor, _unit, _waterUsage);
    }

    function setMonthlyLimit(uint256 _floor, uint256 _unit, uint256 _limit) public onlyOwner {
        unitInfos[_floor][_unit].monthlyLimit = _limit;
    }

    function reportIssue(uint256 _floor, uint256 _unit, string memory _description) public {
        issueReports.push(IssueReport(block.timestamp, _floor, _unit, _description, false));
        emit IssueReported(block.timestamp, _floor, _unit, _description);
        
        // Reward token for reporting an issue
        token.mint(msg.sender, 5 * 10**18);  // Mint 5 tokens
    }

    function resolveIssue(uint256 _issueId) public onlyOwner {
        require(_issueId < issueReports.length, "Invalid issue ID");
        issueReports[_issueId].resolved = true;
        emit IssueResolved(_issueId);
    }

    function getWaterUsageRecord(uint256 _index) public view returns (uint256, uint256, uint256, uint256) {
        WaterUsage memory usage = waterUsageRecords[_index];
        return (usage.timestamp, usage.floor, usage.unit, usage.waterUsage);
    }

    function getCurrentMonthUsage(uint256 _floor, uint256 _unit) public view returns (uint256) {
        return unitInfos[_floor][_unit].currentMonthUsage;
    }

    function getMonthlyLimit(uint256 _floor, uint256 _unit) public view returns (uint256) {
        return unitInfos[_floor][_unit].monthlyLimit;
    }

    function getIssueReport(uint256 _issueId) public view returns (uint256, uint256, uint256, string memory, bool) {
        IssueReport memory report = issueReports[_issueId];
        return (report.timestamp, report.floor, report.unit, report.description, report.resolved);
    }
}