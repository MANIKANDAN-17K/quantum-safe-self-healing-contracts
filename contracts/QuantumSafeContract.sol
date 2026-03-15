// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * Threshold-Based Self-Healing Smart Contract
 * Novel Feature: Automatic threshold-based recovery
 */

contract QuantumSafeContract {
    
    // State Variables
    address public owner;
    bool public paused;
    
    // Threshold variables
    uint256 public attackCount;
    uint256 public safeTransactionCount;
    uint256 public constant ATTACK_THRESHOLD = 3;
    uint256 public constant RECOVERY_THRESHOLD = 5;
    
    // Transaction tracking
    uint256 public totalTransactions;
    uint256 public successfulTransactions;
    uint256 public blockedTransactions;
    uint256 public autoRecoveryCount;
    
    // Transaction history
    struct Transaction {
        address sender;
        address recipient;
        uint256 amount;
        bool success;
        uint256 timestamp;
        string status;
    }
    
    Transaction[] public transactionHistory;
    
    // Events
    event TransactionExecuted(
        address indexed sender,
        address indexed recipient,
        uint256 amount,
        uint256 timestamp
    );
    
    event AttackDetected(
        address indexed attacker,
        uint256 attackCount,
        uint256 timestamp
    );
    
    event ContractPaused(
        string reason,
        uint256 attackCount,
        uint256 timestamp
    );
    
    event ContractResumed(
        string method,
        uint256 safeCount,
        uint256 timestamp
    );
    
    event AutoRecoveryTriggered(
        uint256 safeTransactionCount,
        uint256 timestamp
    );
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    modifier whenNotPaused() {
        require(
            !paused, 
            "Contract paused - self healing active"
        );
        _;
    }
    
    // Constructor
    constructor() {
        owner = msg.sender;
        paused = false;
        attackCount = 0;
        safeTransactionCount = 0;
        autoRecoveryCount = 0;
    }
    
    /**
     * Main transfer function
     * signatureValid comes from off-chain PQ verification
     */
    function transfer(
        address payable recipient,
        uint256 amount,
        bool signatureValid
    ) public whenNotPaused {
        
        totalTransactions++;
        
        // Invalid signature - attack detected
        if (!signatureValid) {
            attackCount++;
            blockedTransactions++;
            
            transactionHistory.push(Transaction({
                sender: msg.sender,
                recipient: recipient,
                amount: amount,
                success: false,
                timestamp: block.timestamp,
                status: "BLOCKED - Invalid PQ Signature"
            }));
            
            emit AttackDetected(
                msg.sender,
                attackCount,
                block.timestamp
            );
            
            // AUTO PAUSE - Novel Contribution
            if (attackCount >= ATTACK_THRESHOLD) {
                paused = true;
                safeTransactionCount = 0;
                emit ContractPaused(
                    "Auto-paused: Attack threshold reached",
                    attackCount,
                    block.timestamp
                );
            }
            return;
        }
        
        // Valid transaction
        successfulTransactions++;
        safeTransactionCount++;
        
        transactionHistory.push(Transaction({
            sender: msg.sender,
            recipient: recipient,
            amount: amount,
            success: true,
            timestamp: block.timestamp,
            status: "SUCCESS"
        }));
        
        emit TransactionExecuted(
            msg.sender,
            recipient,
            amount,
            block.timestamp
        );
    }
    
    /**
     * NOVEL FEATURE: Threshold-Based Auto Recovery
     * Heals itself after N safe transactions
     * No manual admin needed
     */
    function attemptAutoRecovery(bool signatureValid) 
        public {
        
        require(signatureValid, "Invalid signature");
        
        if (!paused) {
            return;
        }
        
        safeTransactionCount++;
        
        emit AutoRecoveryTriggered(
            safeTransactionCount,
            block.timestamp
        );
        
        // Auto resume after RECOVERY_THRESHOLD
        if (safeTransactionCount >= RECOVERY_THRESHOLD) {
            paused = false;
            attackCount = 0;
            autoRecoveryCount++;
            
            emit ContractResumed(
                "AUTO-RECOVERY: Threshold reached",
                safeTransactionCount,
                block.timestamp
            );
        }
    }
    
    /**
     * Manual recovery - admin override
     */
    function manualRecovery() public onlyOwner {
        require(paused, "Not paused");
        paused = false;
        attackCount = 0;
        safeTransactionCount = 0;
        
        emit ContractResumed(
            "MANUAL-RECOVERY: Admin override",
            0,
            block.timestamp
        );
    }
    
    /**
     * Emergency pause
     */
    function emergencyPause() public onlyOwner {
        paused = true;
        emit ContractPaused(
            "Emergency pause by admin",
            attackCount,
            block.timestamp
        );
    }
    
    // View Functions
    function getContractStatus() public view returns (
        bool isPaused,
        uint256 attacks,
        uint256 safeTxCount,
        uint256 totalTx,
        uint256 successTx,
        uint256 blockedTx,
        uint256 autoRecoveries
    ) {
        return (
            paused,
            attackCount,
            safeTransactionCount,
            totalTransactions,
            successfulTransactions,
            blockedTransactions,
            autoRecoveryCount
        );
    }
    
    function getTransactionCount() 
        public view returns (uint256) {
        return transactionHistory.length;
    }
    
    receive() external payable {}
}