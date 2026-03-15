// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/// @title AIAssistedEscrow
/// @notice USDT/USDC escrow with AI-arbiter mediated release and dispute resolution.
/// @dev This contract is an MVP reference and has not been externally audited.
contract AIAssistedEscrow is ReentrancyGuard {
    address public client;
    address public contractor;
    address public aiArbiter; // Wallet controlled by backend signer service
    address public platformTreasury;

    IERC20 public paymentToken; // USDT or USDC
    uint256 public totalAmount;

    enum State {
        Created,
        Funded,
        InProgress,
        Disputed,
        Resolved,
        Completed
    }
    State public currentState;

    event EscrowFunded(uint256 amount);
    event WorkStarted();
    event WorkApprovedAndPaid(uint256 contractorAmount, uint256 platformFee);
    event DisputeRaised(address indexed raisedBy);
    event DisputeResolved(uint256 contractorAmount, uint256 clientRefund, uint256 feeAmount);

    modifier onlyClient() {
        require(msg.sender == client, "Only client");
        _;
    }
    modifier onlyArbiter() {
        require(msg.sender == aiArbiter, "Only AI Arbiter");
        _;
    }
    modifier inState(State _state) {
        require(currentState == _state, "Invalid state");
        _;
    }

    constructor(
        address _contractor,
        address _aiArbiter,
        address _platformTreasury,
        address _paymentToken,
        uint256 _totalAmount
    ) {
        require(_contractor != address(0), "Invalid contractor");
        require(_aiArbiter != address(0), "Invalid arbiter");
        require(_platformTreasury != address(0), "Invalid treasury");
        require(_paymentToken != address(0), "Invalid token");
        require(_totalAmount > 0, "Amount must be > 0");

        client = msg.sender;
        contractor = _contractor;
        aiArbiter = _aiArbiter;
        platformTreasury = _platformTreasury;
        paymentToken = IERC20(_paymentToken);
        totalAmount = _totalAmount;
        currentState = State.Created;
    }

    /// @notice Client deposits agreed token amount into escrow.
    function fundEscrow() external onlyClient inState(State.Created) {
        require(
            paymentToken.transferFrom(client, address(this), totalAmount),
            "Transfer failed"
        );
        currentState = State.Funded;
        emit EscrowFunded(totalAmount);
    }

    /// @notice Optional status transition after kickoff.
    function startWork() external onlyClient inState(State.Funded) {
        currentState = State.InProgress;
        emit WorkStarted();
    }

    /// @notice AI Arbiter signs off and pays contractor + platform fee.
    function aiApproveWork(uint256 _feePercentage)
        external
        onlyArbiter
        nonReentrant
    {
        require(
            currentState == State.Funded || currentState == State.InProgress,
            "Invalid state"
        );
        require(_feePercentage >= 5 && _feePercentage <= 30, "Fee out of range");

        uint256 feeAmount = (totalAmount * _feePercentage) / 100;
        uint256 contractorAmount = totalAmount - feeAmount;

        currentState = State.Completed;

        require(
            paymentToken.transfer(platformTreasury, feeAmount),
            "Fee transfer failed"
        );
        require(
            paymentToken.transfer(contractor, contractorAmount),
            "Contractor payment failed"
        );

        emit WorkApprovedAndPaid(contractorAmount, feeAmount);
    }

    /// @notice Either party or AI can raise dispute while funds are held.
    function flagDispute() external {
        require(
            currentState == State.Funded || currentState == State.InProgress,
            "Invalid state"
        );
        require(
            msg.sender == client ||
                msg.sender == contractor ||
                msg.sender == aiArbiter,
            "Not authorized"
        );
        currentState = State.Disputed;
        emit DisputeRaised(msg.sender);
    }

    /// @notice AI Arbiter decides final split (must sum to total escrow amount).
    function aiResolveDispute(
        uint256 contractorShare,
        uint256 clientRefund,
        uint256 feeAmount
    ) external onlyArbiter inState(State.Disputed) nonReentrant {
        require(
            contractorShare + clientRefund + feeAmount == totalAmount,
            "Math mismatch"
        );

        currentState = State.Resolved;

        if (feeAmount > 0) {
            require(paymentToken.transfer(platformTreasury, feeAmount), "Fee failed");
        }
        if (contractorShare > 0) {
            require(paymentToken.transfer(contractor, contractorShare), "Contractor pay failed");
        }
        if (clientRefund > 0) {
            require(paymentToken.transfer(client, clientRefund), "Refund failed");
        }

        emit DisputeResolved(contractorShare, clientRefund, feeAmount);
    }
}
