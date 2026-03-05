const hre = require("hardhat");

async function main() {
  const tokenAddress = process.argv[2];
  const to = process.argv[3];
  const amount = process.argv[4]; // in smallest units (6 decimals)

  if (!tokenAddress || !to || !amount) {
    throw new Error("Usage: node scripts/mint-mock-usdc.js <tokenAddress> <to> <amount>");
  }

  const token = await hre.ethers.getContractAt("MockUSDC", tokenAddress);
  const tx = await token.mint(to, amount);
  await tx.wait();
  console.log(`Minted ${amount} to ${to}`);
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});

