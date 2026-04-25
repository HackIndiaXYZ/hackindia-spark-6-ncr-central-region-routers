const express = require("express");
const { ethers } = require("ethers");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());

// 🔗 Polygon Amoy RPC
const provider = new ethers.JsonRpcProvider("https://rpc-amoy.polygon.technology/");

// 🔐 PRIVATE KEY (PUT YOUR REAL PRIVATE KEY HERE)
const PRIVATE_KEY = process.env.PRIVATE_KEY;

const wallet = new ethers.Wallet(PRIVATE_KEY, provider);

// 📍 CONTRACT ADDRESS
const contractAddress = "0x6993358415B04c290Febef2b8fcE8Aad83270f06";

// 📜 ABI
const abi = [
  "function logEvent(bytes32 dataHash, string eventType)"
];

const contract = new ethers.Contract(contractAddress, abi, wallet);

// 🟢 TEST ROUTE
app.get("/", (req, res) => {
  res.send("✅ Backend is running");
});

// 🚀 MAIN API
app.post("/log", async (req, res) => {
  try {
    const { hash, eventType } = req.body;

    const tx = await contract.logEvent(hash, eventType);
    await tx.wait();

    res.json({
      success: true,
      txHash: tx.hash
    });

  } catch (error) {
    console.error(error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// 🚀 START SERVER
app.listen(3000, () => {
  console.log("🚀 Server running at http://localhost:3000");
});