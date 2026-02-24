const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deployer:", deployer.address);

  let usdcAddress = process.env.USDC_TOKEN;
  if (!usdcAddress) {
    const MockUSDC = await hre.ethers.getContractFactory("MockUSDC");
    const mock = await MockUSDC.deploy();
    await mock.waitForDeployment();
    usdcAddress = await mock.getAddress();
    console.log("Deployed MockUSDC:", usdcAddress);
  } else {
    console.log("Using USDC token:", usdcAddress);
  }

  const RockPaperScissors = await hre.ethers.getContractFactory("RockPaperScissors");
  const rps = await RockPaperScissors.deploy(usdcAddress);
  await rps.waitForDeployment();

  console.log("Deployed RockPaperScissors:", await rps.getAddress());
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});

