const hre = require("hardhat");

async function main() {
  const useMockUsdc = (process.env.USE_MOCK_USDC || "").toLowerCase() === "true";
  let usdcAddress = process.env.USDC_TOKEN;

  if (useMockUsdc) {
    const mockUsdc = await hre.ethers.deployContract("MockUSDC");
    await mockUsdc.waitForDeployment();
    usdcAddress = await mockUsdc.getAddress();
    console.log(`MockUSDC deployed to: ${usdcAddress}`);
  } else if (!usdcAddress) {
    throw new Error("USDC_TOKEN env var is required when USE_MOCK_USDC is not true.");
  }

  const rockPaperScissors = await hre.ethers.deployContract("RockPaperScissors", [usdcAddress]);
  await rockPaperScissors.waitForDeployment();

  const deployedAddress = await rockPaperScissors.getAddress();
  console.log(
    JSON.stringify(
      {
        network: hre.network.name,
        usdcToken: usdcAddress,
        rockPaperScissors: deployedAddress,
        mockMode: useMockUsdc,
      },
      null,
      2
    )
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
