export const ERC20_ABI = [
  'function decimals() view returns (uint8)',
  'function balanceOf(address) view returns (uint256)',
  'function allowance(address owner, address spender) view returns (uint256)',
  'function approve(address spender, uint256 amount) returns (bool)',
]

export const RPS_ABI = [
  'function usdcToken() view returns (address)',
  'function feeBps() view returns (uint16)',
  'function createGame(uint256 wager) returns (uint256)',
  'function joinGame(uint256 gameId)',
  'function commitMove(uint256 gameId, bytes32 commitment)',
  'function revealMove(uint256 gameId, uint8 move, bytes32 salt)',
  'function forceSettle(uint256 gameId)',
  'function computeCommitment(uint256 gameId, address player, uint8 move, bytes32 salt) pure returns (bytes32)',
  'function games(uint256) view returns (address player1,address player2,bytes32 p1Commitment,bytes32 p2Commitment,uint8 p1Reveal,uint8 p2Reveal,uint256 wager,uint8 state,uint64 commitDeadline,uint64 revealDeadline)',
  'event GameCreated(uint256 indexed gameId, address indexed player1, uint256 wager)',
  'event GameJoined(uint256 indexed gameId, address indexed player2)',
  'event MoveCommitted(uint256 indexed gameId, address indexed player, bytes32 commitment)',
  'event MoveRevealed(uint256 indexed gameId, address indexed player, uint8 move)',
  'event GameSettled(uint256 indexed gameId, address winner, bool tie, uint256 payoutPlayer1, uint256 payoutPlayer2, uint256 fee)',
]

