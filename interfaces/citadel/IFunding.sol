// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

interface IFunding {
    event AssetCapUpdated(uint256 assetCap);
    event CitadelPriceBoundsSet(uint256 minPrice, uint256 maxPrice);
    event CitadelPriceFlag(uint256 price, uint256 minPrice, uint256 maxPrice);
    event CitadelPriceInAssetUpdated(uint256 citadelPrice);
    event ClaimToTreasury(address indexed token, uint256 amount);
    event Deposit(
        address indexed buyer,
        uint256 assetIn,
        uint256 citadelOutValue
    );
    event DiscountLimitsSet(uint256 minDiscount, uint256 maxDiscount);
    event DiscountManagerSet(address discountManager);
    event DiscountSet(uint256 discount);
    event Paused(address account);
    event SaleRecipientUpdated(address indexed recipient);
    event Sweep(address indexed token, uint256 amount);
    event Unpaused(address account);

    function CONTRACT_GOVERNANCE_ROLE() external view returns (bytes32);

    function KEEPER_ROLE() external view returns (bytes32);

    function MAX_BPS() external view returns (uint256);

    function PAUSER_ROLE() external view returns (bytes32);

    function POLICY_OPERATIONS_ROLE() external view returns (bytes32);

    function TREASURY_OPERATIONS_ROLE() external view returns (bytes32);

    function TREASURY_VAULT_ROLE() external view returns (bytes32);

    function UNPAUSER_ROLE() external view returns (bytes32);

    function __GlobalAccessControlManaged_init(address _globalAccessControl)
        external;

    function asset() external view returns (address);

    function assetDecimalsNormalizationValue() external view returns (uint256);

    function citadel() external view returns (address);

    function citadelPriceFlag() external view returns (bool);

    function citadelPriceInAsset() external view returns (uint256);

    function citadelPriceInAssetOracle() external view returns (address);

    function claimAssetToTreasury() external;

    function clearCitadelPriceFlag() external;

    function deposit(uint256 _assetAmountIn, uint256 _minCitadelOut)
        external
        returns (uint256 citadelAmount_);

    function funding()
        external
        view
        returns (
            uint256 discount,
            uint256 minDiscount,
            uint256 maxDiscount,
            address discountManager,
            uint256 assetCumulativeFunded,
            uint256 assetCap
        );

    function gac() external view returns (address);

    function getAmountOut(uint256 _assetAmountIn)
        external
        view
        returns (uint256 citadelAmount_);

    function getDiscount() external view returns (uint256);

    function getFundingParams()
        external
        view
        returns (Funding.FundingParams memory);

    function getRemainingFundable() external view returns (uint256 limitLeft_);

    function getStakedCitadelAmountOut(uint256 _assetAmountIn)
        external
        view
        returns (uint256 xCitadelAmount_);

    function initialize(
        address _gac,
        address _citadel,
        address _asset,
        address _xCitadel,
        address _saleRecipient,
        address _citadelPriceInAssetOracle,
        uint256 _assetCap
    ) external;

    function maxCitadelPriceInAsset() external view returns (uint256);

    function minCitadelPriceInAsset() external view returns (uint256);

    function pause() external;

    function paused() external view returns (bool);

    function saleRecipient() external view returns (address);

    function setAssetCap(uint256 _assetCap) external;

    function setCitadelAssetPriceBounds(uint256 _minPrice, uint256 _maxPrice)
        external;

    function setDiscount(uint256 _discount) external;

    function setDiscountLimits(uint256 _minDiscount, uint256 _maxDiscount)
        external;

    function setDiscountManager(address _discountManager) external;

    function setSaleRecipient(address _saleRecipient) external;

    function sweep(address _token) external;

    function unpause() external;

    function updateCitadelPriceInAsset(uint256 _citadelPriceInAsset) external;

    function updateCitadelPriceInAsset() external;

    function xCitadel() external view returns (address);
}

interface Funding {
    struct FundingParams {
        uint256 discount;
        uint256 minDiscount;
        uint256 maxDiscount;
        address discountManager;
        uint256 assetCumulativeFunded;
        uint256 assetCap;
    }
}
