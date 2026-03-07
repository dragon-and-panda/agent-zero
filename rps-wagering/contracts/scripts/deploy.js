const hre = require("hardhat");

async function main() {
  const usdcAddress = process.env.USDC_TOKEN;
  if (!usdcAddress) {
    throw new Error("USDC_TOKEN env var is required.");
  }

  const rockPaperScissors = await hre.ethers.deployContract("RockPaperScissors", [usdcAddress]);
  await rockPaperScissors.waitForDeployment();

  const deployedAddress = await rockPaperScissors.getAddress();
  console.log(`RockPaperScissors deployed to: ${deployedAddress}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
