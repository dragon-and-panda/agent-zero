// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract RockPaperScissors is Ownable, ReentrancyGuard {
    using SafeERC20 for IERC20;

    enum Move {
        None,
        Rock,
        Paper,
        Scissors
    }

    enum GameState {
        Open,
        Committed,
        Revealed,
        Settled
    }

    struct Game {
        address player1;
        address player2;
        bytes32 p1Commitment;
        bytes32 p2Commitment;
        Move p1Reveal;
        Move p2Reveal;
        uint256 wager;
        GameState state;
        uint64 commitDeadline;
        uint64 revealDeadline;
    }

    IERC20 public immutable usdcToken;

    /// @dev Fee in basis points. 150 = 1.5%
    uint16 public feeBps = 150;
    uint256 public feesAccrued;

    uint32 public commitPeriodSeconds = 15 minutes;
    uint32 public revealPeriodSeconds = 15 minutes;

    mapping(uint256 => Game) public games;
    uint256 public gameCounter;

    event GameCreated(uint256 indexed gameId, address indexed player1, uint256 wager);
    event GameJoined(uint256 indexed gameId, address indexed player2);
    event MoveCommitted(uint256 indexed gameId, address indexed player, bytes32 commitment);
    event MoveRevealed(uint256 indexed gameId, address indexed player, Move move);
    event GameSettled(
        uint256 indexed gameId,
        address winner,
        bool tie,
        uint256 payoutPlayer1,
        uint256 payoutPlayer2,
        uint256 fee
    );

    error InvalidState();
    error NotAPlayer();
    error CommitmentAlreadySet();
    error RevealAlreadySet();
    error InvalidMove();
    error DeadlineNotReached();
    error InvalidCommitment();

    constructor(address _usdcToken) Ownable(msg.sender) {
        require(_usdcToken != address(0), "USDC=0");
        usdcToken = IERC20(_usdcToken);
    }

    function setFeeBps(uint16 newFeeBps) external onlyOwner {
        require(newFeeBps <= 500, "fee too high"); // hard cap at 5%
        feeBps = newFeeBps;
    }

    function setPeriods(uint32 newCommitPeriodSeconds, uint32 newRevealPeriodSeconds) external onlyOwner {
        require(newCommitPeriodSeconds >= 60, "commit too short");
        require(newRevealPeriodSeconds >= 60, "reveal too short");
        commitPeriodSeconds = newCommitPeriodSeconds;
        revealPeriodSeconds = newRevealPeriodSeconds;
    }

    function withdrawFees(address to, uint256 amount) external onlyOwner nonReentrant {
        require(to != address(0), "to=0");
        require(amount <= feesAccrued, "amount>fees");
        feesAccrued -= amount;
        usdcToken.safeTransfer(to, amount);
    }

    function createGame(uint256 wager) external nonReentrant returns (uint256 gameId) {
        require(wager > 0, "wager=0");

        gameId = ++gameCounter;
        games[gameId] = Game({
            player1: msg.sender,
            player2: address(0),
            p1Commitment: bytes32(0),
            p2Commitment: bytes32(0),
            p1Reveal: Move.None,
            p2Reveal: Move.None,
            wager: wager,
            state: GameState.Open,
            commitDeadline: 0,
            revealDeadline: 0
        });

        usdcToken.safeTransferFrom(msg.sender, address(this), wager);
        emit GameCreated(gameId, msg.sender, wager);
    }

    function joinGame(uint256 gameId) external nonReentrant {
        Game storage g = games[gameId];
        if (g.state != GameState.Open) revert InvalidState();
        require(g.player1 != address(0), "no game");
        require(g.player2 == address(0), "joined");
        require(msg.sender != g.player1, "self join");

        g.player2 = msg.sender;
        g.state = GameState.Committed;
        g.commitDeadline = uint64(block.timestamp + commitPeriodSeconds);

        usdcToken.safeTransferFrom(msg.sender, address(this), g.wager);
        emit GameJoined(gameId, msg.sender);
    }

    function computeCommitment(uint256 gameId, address player, Move move, bytes32 salt) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(gameId, player, uint8(move), salt));
    }

    function commitMove(uint256 gameId, bytes32 commitment) external {
        Game storage g = games[gameId];
        if (g.state != GameState.Committed) revert InvalidState();
        if (block.timestamp > g.commitDeadline) revert DeadlineNotReached();

        if (msg.sender != g.player1 && msg.sender != g.player2) revert NotAPlayer();

        if (msg.sender == g.player1) {
            if (g.p1Commitment != bytes32(0)) revert CommitmentAlreadySet();
            g.p1Commitment = commitment;
        } else {
            if (g.p2Commitment != bytes32(0)) revert CommitmentAlreadySet();
            g.p2Commitment = commitment;
        }

        emit MoveCommitted(gameId, msg.sender, commitment);

        if (g.p1Commitment != bytes32(0) && g.p2Commitment != bytes32(0)) {
            g.state = GameState.Revealed;
            g.revealDeadline = uint64(block.timestamp + revealPeriodSeconds);
        }
    }

    function revealMove(uint256 gameId, Move move, bytes32 salt) external nonReentrant {
        Game storage g = games[gameId];
        if (g.state != GameState.Revealed) revert InvalidState();
        if (block.timestamp > g.revealDeadline) revert DeadlineNotReached();
        if (move != Move.Rock && move != Move.Paper && move != Move.Scissors) revert InvalidMove();
        if (msg.sender != g.player1 && msg.sender != g.player2) revert NotAPlayer();

        bytes32 expected = computeCommitment(gameId, msg.sender, move, salt);
        if (msg.sender == g.player1) {
            if (g.p1Reveal != Move.None) revert RevealAlreadySet();
            if (expected != g.p1Commitment) revert InvalidCommitment();
            g.p1Reveal = move;
        } else {
            if (g.p2Reveal != Move.None) revert RevealAlreadySet();
            if (expected != g.p2Commitment) revert InvalidCommitment();
            g.p2Reveal = move;
        }

        emit MoveRevealed(gameId, msg.sender, move);

        if (g.p1Reveal != Move.None && g.p2Reveal != Move.None) {
            _settle(gameId, true);
        }
    }

    /// @dev Force settle after commit/reveal deadlines to prevent griefing.
    function forceSettle(uint256 gameId) external nonReentrant {
        Game storage g = games[gameId];
        if (g.state == GameState.Committed) {
            if (block.timestamp <= g.commitDeadline) revert DeadlineNotReached();
            _settle(gameId, false);
            return;
        }
        if (g.state == GameState.Revealed) {
            if (block.timestamp <= g.revealDeadline) revert DeadlineNotReached();
            _settle(gameId, false);
            return;
        }
        revert InvalidState();
    }

    function _settle(uint256 gameId, bool bothRevealed) internal {
        Game storage g = games[gameId];
        if (g.state == GameState.Settled) revert InvalidState();

        uint256 pot = g.wager * 2;

        uint256 payout1;
        uint256 payout2;
        uint256 fee;
        address winner = address(0);
        bool tie = false;

        if (g.state == GameState.Committed) {
            // forfeit if only one player committed, refund if none committed
            bool p1Committed = g.p1Commitment != bytes32(0);
            bool p2Committed = g.p2Commitment != bytes32(0);
            if (!p1Committed && !p2Committed) {
                payout1 = g.wager;
                payout2 = g.wager;
            } else {
                fee = (pot * feeBps) / 10_000;
                feesAccrued += fee;
                uint256 remaining = pot - fee;
                if (p1Committed && !p2Committed) {
                    payout1 = remaining;
                    winner = g.player1;
                } else if (p2Committed && !p1Committed) {
                    payout2 = remaining;
                    winner = g.player2;
                } else {
                    // both committed but didn't reveal before force settle: refund (no fee)
                    payout1 = g.wager;
                    payout2 = g.wager;
                }
            }
        } else if (g.state == GameState.Revealed) {
            // normal settlement if both revealed, otherwise forfeit/refund
            bool p1Revealed = g.p1Reveal != Move.None;
            bool p2Revealed = g.p2Reveal != Move.None;

            if (bothRevealed) {
                (winner, tie) = _determineWinner(g);
                fee = (pot * feeBps) / 10_000;
                feesAccrued += fee;
                uint256 remaining = pot - fee;
                if (tie) {
                    payout1 = remaining / 2;
                    payout2 = remaining - payout1;
                } else if (winner == g.player1) {
                    payout1 = remaining;
                } else {
                    payout2 = remaining;
                }
            } else if (p1Revealed && !p2Revealed) {
                fee = (pot * feeBps) / 10_000;
                feesAccrued += fee;
                payout1 = pot - fee;
                winner = g.player1;
            } else if (p2Revealed && !p1Revealed) {
                fee = (pot * feeBps) / 10_000;
                feesAccrued += fee;
                payout2 = pot - fee;
                winner = g.player2;
            } else {
                payout1 = g.wager;
                payout2 = g.wager;
            }
        } else {
            revert InvalidState();
        }

        g.state = GameState.Settled;

        if (payout1 > 0) usdcToken.safeTransfer(g.player1, payout1);
        if (payout2 > 0) usdcToken.safeTransfer(g.player2, payout2);

        emit GameSettled(gameId, winner, tie, payout1, payout2, fee);
    }

    function _determineWinner(Game storage g) internal view returns (address winner, bool tie) {
        Move a = g.p1Reveal;
        Move b = g.p2Reveal;
        if (a == b) return (address(0), true);

        // Rock beats Scissors, Scissors beats Paper, Paper beats Rock
        bool p1Wins = (a == Move.Rock && b == Move.Scissors) ||
            (a == Move.Scissors && b == Move.Paper) ||
            (a == Move.Paper && b == Move.Rock);
        return (p1Wins ? g.player1 : g.player2, false);
    }
}

