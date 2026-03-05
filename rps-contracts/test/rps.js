const { expect } = require("chai");
const { ethers } = require("hardhat");
const { time } = require("@nomicfoundation/hardhat-network-helpers");

function commitment(gameId, player, move, salt) {
  return ethers.solidityPackedKeccak256(
    ["uint256", "address", "uint8", "bytes32"],
    [gameId, player, move, salt],
  );
}

describe("RockPaperScissors", function () {
  const WAGER = 1_000_000n; // 1 USDC (6 decimals)
  const START = 10_000_000n; // 10 USDC

  async function deploy() {
    const [owner, p1, p2] = await ethers.getSigners();
    const MockUSDC = await ethers.getContractFactory("MockUSDC");
    const token = await MockUSDC.deploy();
    await token.waitForDeployment();

    const RockPaperScissors = await ethers.getContractFactory("RockPaperScissors");
    const rps = await RockPaperScissors.deploy(await token.getAddress());
    await rps.waitForDeployment();

    await token.mint(p1.address, START);
    await token.mint(p2.address, START);
    await token.connect(p1).approve(await rps.getAddress(), START);
    await token.connect(p2).approve(await rps.getAddress(), START);

    return { owner, p1, p2, token, rps };
  }

  it("settles winner with 1.5% fee", async function () {
    const { p1, p2, token, rps } = await deploy();

    await rps.connect(p1).createGame(WAGER);
    const gameId = await rps.gameCounter();
    await rps.connect(p2).joinGame(gameId);

    const salt1 = ethers.hexlify(ethers.randomBytes(32));
    const salt2 = ethers.hexlify(ethers.randomBytes(32));

    // p1 Rock, p2 Scissors
    await rps.connect(p1).commitMove(gameId, commitment(gameId, p1.address, 1, salt1));
    await rps.connect(p2).commitMove(gameId, commitment(gameId, p2.address, 3, salt2));

    await rps.connect(p1).revealMove(gameId, 1, salt1);
    await rps.connect(p2).revealMove(gameId, 3, salt2);

    const fee = (WAGER * 2n * 150n) / 10_000n;
    expect(await token.balanceOf(p1.address)).to.equal(START + WAGER - fee);
    expect(await token.balanceOf(p2.address)).to.equal(START - WAGER);
    expect(await rps.feesAccrued()).to.equal(fee);
  });

  it("settles tie by splitting after fee", async function () {
    const { p1, p2, token, rps } = await deploy();

    await rps.connect(p1).createGame(WAGER);
    const gameId = await rps.gameCounter();
    await rps.connect(p2).joinGame(gameId);

    const salt1 = ethers.hexlify(ethers.randomBytes(32));
    const salt2 = ethers.hexlify(ethers.randomBytes(32));

    // both Rock
    await rps.connect(p1).commitMove(gameId, commitment(gameId, p1.address, 1, salt1));
    await rps.connect(p2).commitMove(gameId, commitment(gameId, p2.address, 1, salt2));
    await rps.connect(p1).revealMove(gameId, 1, salt1);
    await rps.connect(p2).revealMove(gameId, 1, salt2);

    const fee = (WAGER * 2n * 150n) / 10_000n;
    const split = (WAGER * 2n - fee) / 2n;
    expect(await token.balanceOf(p1.address)).to.equal(START - WAGER + split);
    expect(await token.balanceOf(p2.address)).to.equal(START - WAGER + split);
    expect(await rps.feesAccrued()).to.equal(fee);
  });

  it("allows forceSettle if opponent fails to reveal", async function () {
    const { p1, p2, token, rps } = await deploy();

    await rps.connect(p1).createGame(WAGER);
    const gameId = await rps.gameCounter();
    await rps.connect(p2).joinGame(gameId);

    const salt1 = ethers.hexlify(ethers.randomBytes(32));
    const salt2 = ethers.hexlify(ethers.randomBytes(32));

    await rps.connect(p1).commitMove(gameId, commitment(gameId, p1.address, 2, salt1)); // Paper
    await rps.connect(p2).commitMove(gameId, commitment(gameId, p2.address, 1, salt2)); // Rock

    await rps.connect(p1).revealMove(gameId, 2, salt1);

    await time.increase(16 * 60);
    await rps.forceSettle(gameId);

    const fee = (WAGER * 2n * 150n) / 10_000n;
    expect(await token.balanceOf(p1.address)).to.equal(START + WAGER - fee);
    expect(await token.balanceOf(p2.address)).to.equal(START - WAGER);
  });

  it("allows forceSettle if opponent fails to commit", async function () {
    const { p1, p2, token, rps } = await deploy();

    await rps.connect(p1).createGame(WAGER);
    const gameId = await rps.gameCounter();
    await rps.connect(p2).joinGame(gameId);

    const salt1 = ethers.hexlify(ethers.randomBytes(32));
    await rps.connect(p1).commitMove(gameId, commitment(gameId, p1.address, 1, salt1));

    await time.increase(16 * 60);
    await rps.forceSettle(gameId);

    const fee = (WAGER * 2n * 150n) / 10_000n;
    expect(await token.balanceOf(p1.address)).to.equal(START + WAGER - fee);
    expect(await token.balanceOf(p2.address)).to.equal(START - WAGER);
  });
});

