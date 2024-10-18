pragma solidity ^0.8.0;

contract WaterConsumptionContract {
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

    mapping(uint256 => mapping(uint256 => UnitInfo)) public unitInfos;  // floor => unit => UnitInfo
    WaterUsage[] public waterUsageRecords;

    event WaterUsageRecorded(uint256 timestamp, uint256 floor, uint256 unit, uint256 waterUsage);
    event LimitExceeded(uint256 timestamp, uint256 floor, uint256 unit, uint256 currentUsage, uint256 limit);

    function recordWaterUsage(uint256 _floor, uint256 _unit, uint256 _waterUsage) public {
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
        }

        emit WaterUsageRecorded(timestamp, _floor, _unit, _waterUsage);
    }

    function setMonthlyLimit(uint256 _floor, uint256 _unit, uint256 _limit) public {
        unitInfos[_floor][_unit].monthlyLimit = _limit;
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
}