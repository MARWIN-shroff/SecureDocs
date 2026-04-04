const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying SecureDocs contract...");

  const SecureDocs = await ethers.getContractFactory("SecureDocs");
  const secureDocs = await SecureDocs.deploy();

  await secureDocs.deployed();

  console.log("SecureDocs deployed to:", secureDocs.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
