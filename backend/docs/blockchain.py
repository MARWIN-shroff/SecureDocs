from web3 import Web3
from django.conf import settings

# Contract ABI - will be updated when contract is deployed
CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "documentHash", "type": "bytes32"}],
        "name": "storeDocument",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "documentHash", "type": "bytes32"}],
        "name": "verifyDocument",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

def get_web3():
    """Get Web3 instance."""
    return Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_RPC_URL))

def store_document_hash(document_hash: str) -> str:
    """Store document hash on blockchain."""
    w3 = get_web3()
    contract = w3.eth.contract(address=settings.CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    
    # For simplicity, assume we have a default account
    # In production, use proper wallet management
    account = w3.eth.accounts[0]
    
    tx_hash = contract.functions.storeDocument(bytes.fromhex(document_hash)).transact({'from': account})
    return w3.to_hex(tx_hash)

def verify_document_hash(document_hash: str) -> bool:
    """Verify document hash on blockchain."""
    w3 = get_web3()
    contract = w3.eth.contract(address=settings.CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    
    return contract.functions.verifyDocument(bytes.fromhex(document_hash)).call()
