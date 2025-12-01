"""
VEra-Resonance — Web3 Service for BASE Sepolia
© 2025 Karlheinz Beismann — VEra-Resonance Project
Licensed under the Apache License, Version 2.0

Handles all blockchain interactions with BASE Sepolia smart contracts:
- Identity NFT minting and queries
- Resonance Score updates
- Interaction recording
- Token ID lookups
"""

import os
import asyncio
from typing import Dict, Any, Optional, Tuple, List
from web3 import Web3
from web3.exceptions import ContractLogicError
from eth_account import Account
from logger import setup_logger

logger = setup_logger(__name__)


class Web3Service:
    """Service for interacting with BASE Sepolia blockchain"""
    
    def __init__(self):
        """Initialize Web3 connection and contract instances"""
        # Load environment variables (will be loaded by server.py before import)
        self.rpc_url = os.getenv("BASE_SEPOLIA_RPC_URL", "https://sepolia.base.org")
        # Try BACKEND_PRIVATE_KEY first (has funds!), then fallback to others
        self.private_key = os.getenv("BACKEND_PRIVATE_KEY") or os.getenv("PRIVATE_KEY") or os.getenv("ADMIN_PRIVATE_KEY")
        
        # Contract addresses
        self.identity_nft_address = os.getenv("IDENTITY_NFT_ADDRESS")
        self.resonance_score_address = os.getenv("RESONANCE_SCORE_ADDRESS")
        self.resonance_registry_address = os.getenv("RESONANCE_REGISTRY_ADDRESS")
        
        # Initialize Web3 (read-only mode if no PRIVATE_KEY)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        if not self.private_key:
            logger.warning("⚠️ PRIVATE_KEY not found - Web3Service in READ-ONLY mode")
            logger.warning("⚠️ Blockchain queries work, but minting/transactions disabled")
            self.account = None
        else:
            self.account = Account.from_key(self.private_key)
            logger.info(f"🌐 Connected to BASE Sepolia: {self.rpc_url}")
            logger.info(f"💳 Backend Wallet: {self.account.address}")
        
        # Load contract ABIs and initialize contracts
        self._load_contracts()
        
    def _load_contracts(self):
        """Load smart contract instances"""
        # Identity NFT ABI (minimal - only functions we use)
        identity_abi = [
            {
                "inputs": [{"internalType": "address", "name": "to", "type": "address"}],
                "name": "mintIdentity",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "uint256", "name": "index", "type": "uint256"}],
                "name": "tokenOfOwnerByIndex",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
                    {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
                    {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "Transfer",
                "type": "event"
            }
        ]
        
        # Resonance Score ABI
        score_abi = [
            {
                "inputs": [{"internalType": "address", "name": "user", "type": "address"}, {"internalType": "uint256", "name": "newAmount", "type": "uint256"}],
                "name": "adminAdjust",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
                "name": "getResonance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        # Resonance Registry ABI
        registry_abi = [
            {
                "inputs": [
                    {"internalType": "address", "name": "follower", "type": "address"},
                    {"internalType": "address", "name": "creator", "type": "address"},
                    {"internalType": "bytes32", "name": "linkId", "type": "bytes32"},
                    {"internalType": "uint8", "name": "actionType", "type": "uint8"},
                    {"internalType": "uint256", "name": "weightFollower", "type": "uint256"},
                    {"internalType": "uint256", "name": "weightCreator", "type": "uint256"}
                ],
                "name": "recordInteraction",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "address", "name": "user", "type": "address"}, {"internalType": "uint256", "name": "offset", "type": "uint256"}, {"internalType": "uint256", "name": "limit", "type": "uint256"}],
                "name": "getUserInteractions",
                "outputs": [
                    {
                        "components": [
                            {"internalType": "address", "name": "initiator", "type": "address"},
                            {"internalType": "address", "name": "responder", "type": "address"},
                            {"internalType": "uint8", "name": "interactionType", "type": "uint8"},
                            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                            {"internalType": "string", "name": "metadata", "type": "string"}
                        ],
                        "internalType": "struct InteractionData[]",
                        "name": "",
                        "type": "tuple[]"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "internalType": "address", "name": "follower", "type": "address"},
                    {"indexed": True, "internalType": "address", "name": "creator", "type": "address"},
                    {"indexed": True, "internalType": "bytes32", "name": "linkId", "type": "bytes32"},
                    {"indexed": False, "internalType": "uint8", "name": "actionType", "type": "uint8"},
                    {"indexed": False, "internalType": "uint256", "name": "weightFollower", "type": "uint256"},
                    {"indexed": False, "internalType": "uint256", "name": "weightCreator", "type": "uint256"},
                    {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
                ],
                "name": "InteractionRecorded",
                "type": "event"
            }
        ]
        
        # Initialize contract instances
        if self.identity_nft_address:
            self.identity_nft = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.identity_nft_address),
                abi=identity_abi
            )
            logger.info(f"✅ Identity NFT Contract: {self.identity_nft_address}")
        else:
            logger.warning("⚠️ IDENTITY_NFT_ADDRESS not set")
            self.identity_nft = None
            
        if self.resonance_score_address:
            self.resonance_score = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.resonance_score_address),
                abi=score_abi
            )
            logger.info(f"✅ Resonance Score Contract: {self.resonance_score_address}")
        else:
            logger.warning("⚠️ RESONANCE_SCORE_ADDRESS not set")
            self.resonance_score = None
            
        if self.resonance_registry_address:
            self.resonance_registry = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.resonance_registry_address),
                abi=registry_abi
            )
            logger.info(f"✅ Resonance Registry Contract: {self.resonance_registry_address}")
        else:
            logger.warning("⚠️ RESONANCE_REGISTRY_ADDRESS not set")
            self.resonance_registry = None
    
    async def has_identity_nft(self, address: str) -> bool:
        """Check if address has an Identity NFT"""
        try:
            if not self.identity_nft:
                logger.warning("Identity NFT contract not initialized")
                return False
                
            checksum_address = Web3.to_checksum_address(address)
            balance = self.identity_nft.functions.balanceOf(checksum_address).call()
            return balance > 0
        except Exception as e:
            logger.error(f"Error checking NFT balance for {address}: {e}")
            return False
    
    async def get_identity_token_id(self, address: str) -> Optional[int]:
        """Get Identity NFT token ID for address"""
        try:
            if not self.identity_nft:
                return None
                
            checksum_address = Web3.to_checksum_address(address)
            balance = self.identity_nft.functions.balanceOf(checksum_address).call()
            
            if balance == 0:
                return None
            
            # Get first token (index 0)
            token_id = self.identity_nft.functions.tokenOfOwnerByIndex(checksum_address, 0).call()
            return int(token_id)
            
        except Exception as e:
            logger.error(f"Error getting token ID for {address}: {e}")
            # Fallback: Try to get from Transfer events
            return await self._get_token_id_from_events(address)
    
    async def _get_token_id_from_events(self, address: str) -> Optional[int]:
        """Fallback: Get token ID from Transfer events"""
        try:
            if not self.identity_nft:
                return None
                
            checksum_address = Web3.to_checksum_address(address)
            
            # Get current block
            current_block = self.w3.eth.block_number
            from_block = max(0, current_block - 10000)  # Search last 10k blocks
            
            # Get Transfer events where 'to' is our address
            logs = self.w3.eth.get_logs({
                'fromBlock': from_block,
                'toBlock': 'latest',
                'address': self.identity_nft.address,
                'topics': [
                    self.w3.keccak(text='Transfer(address,address,uint256)').hex(),
                    None,  # from (any)
                    '0x' + checksum_address[2:].lower().zfill(64)  # to (our address)
                ]
            })
            
            if logs:
                # Get tokenId from last Transfer event
                token_id = int(logs[-1]['topics'][3].hex(), 16)
                logger.info(f"✅ Found token ID {token_id} from events for {address}")
                return token_id
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting token ID from events for {address}: {e}")
            return None
    
    async def mint_identity_nft(self, address: str) -> Tuple[bool, Dict[str, Any]]:
        """Mint Identity NFT for address"""
        try:
            if not self.identity_nft:
                return False, {"error": "Identity NFT contract not initialized"}
            
            checksum_address = Web3.to_checksum_address(address)
            
            # Check if already has NFT
            if await self.has_identity_nft(address):
                logger.info(f"⚠️ Address {address} already has Identity NFT")
                token_id = await self.get_identity_token_id(address)
                return True, {
                    "message": "Already has Identity NFT",
                    "token_id": token_id,
                    "address": address
                }
            
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            mint_tx = self.identity_nft.functions.mintIdentity(checksum_address).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 200000,
                'maxFeePerGas': self.w3.eth.gas_price * 2,
                'maxPriorityFeePerGas': self.w3.eth.gas_price,
                'chainId': 84532  # BASE Sepolia
            })
            
            # Sign and send transaction
            signed_tx = self.w3.eth.account.sign_transaction(mint_tx, self.private_key)
            # Handle both .rawTransaction (older) and .raw_transaction (newer) Web3.py versions
            raw_tx = getattr(signed_tx, 'rawTransaction', getattr(signed_tx, 'raw_transaction', None))
            if raw_tx is None:
                raise ValueError("Could not get raw transaction from signed transaction")
            tx_hash = self.w3.eth.send_raw_transaction(raw_tx)
            tx_hash_hex = tx_hash.hex()
            
            logger.info(f"🎨 NFT mint transaction sent: {tx_hash_hex}")
            logger.info(f"   → For: {address}")
            logger.info(f"   → Status: pending confirmation...")
            
            return True, {
                "tx_hash": tx_hash_hex,
                "status": "pending",
                "address": address,
                "basescan_url": f"https://sepolia.basescan.org/tx/{tx_hash_hex}"
            }
            
        except ContractLogicError as e:
            logger.error(f"Contract error minting NFT for {address}: {e}")
            return False, {"error": f"Contract error: {str(e)}"}
        except Exception as e:
            logger.error(f"Error minting NFT for {address}: {e}")
            return False, {"error": str(e)}
    
    async def get_blockchain_score(self, address: str) -> int:
        """Get Resonance Score from blockchain"""
        try:
            if not self.resonance_score:
                logger.warning("Resonance Score contract not initialized")
                return 0
            
            checksum_address = Web3.to_checksum_address(address)
            score = self.resonance_score.functions.getResonance(checksum_address).call()
            return int(score)
            
        except Exception as e:
            logger.error(f"Error getting blockchain score for {address}: {e}")
            return 0
    
    async def update_blockchain_score(self, address: str, score: int) -> Tuple[bool, Dict[str, Any]]:
        """Update Resonance Score on blockchain"""
        try:
            if not self.resonance_score:
                return False, {"error": "Resonance Score contract not initialized"}
            
            checksum_address = Web3.to_checksum_address(address)
            
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            update_tx = self.resonance_score.functions.adminAdjust(
                checksum_address, 
                score
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 100000,
                'maxFeePerGas': self.w3.eth.gas_price * 2,
                'maxPriorityFeePerGas': self.w3.eth.gas_price,
                'chainId': 84532
            })
            
            # Sign and send
            signed_tx = self.w3.eth.account.sign_transaction(update_tx, self.private_key)
            raw_tx = getattr(signed_tx, 'rawTransaction', getattr(signed_tx, 'raw_transaction', None))
            if raw_tx is None:
                raise ValueError("Could not get raw transaction from signed transaction")
            tx_hash = self.w3.eth.send_raw_transaction(raw_tx)
            tx_hash_hex = tx_hash.hex()
            
            logger.info(f"📊 Score update transaction sent: {tx_hash_hex}")
            logger.info(f"   → Address: {address}")
            logger.info(f"   → Score: {score}")
            
            return True, {
                "tx_hash": tx_hash_hex,
                "status": "pending",
                "score": score,
                "basescan_url": f"https://sepolia.basescan.org/tx/{tx_hash_hex}"
            }
            
        except Exception as e:
            logger.error(f"Error updating score for {address}: {e}")
            return False, {"error": str(e)}
    
    async def record_interaction(
        self, 
        initiator: str, 
        responder: str, 
        interaction_type: int,
        metadata: str = ""
    ) -> Tuple[bool, Dict[str, Any]]:
        """Record interaction on blockchain
        
        Contract expects 6 parameters:
        - follower (address): initiator of interaction
        - creator (address): responder/recipient
        - linkId (bytes32): unique identifier (hash of metadata)
        - actionType (uint8): interaction type (0=FOLLOW, etc.)
        - weightFollower (uint256): initiator's resonance score
        - weightCreator (uint256): responder's resonance score
        """
        try:
            if not self.resonance_registry:
                return False, {"error": "Resonance Registry contract not initialized"}
            
            initiator_addr = Web3.to_checksum_address(initiator)
            responder_addr = Web3.to_checksum_address(responder)
            
            # Generate linkId from metadata (hash it to bytes32)
            link_id = Web3.keccak(text=metadata) if metadata else Web3.keccak(text=f"{initiator}:{responder}:{interaction_type}")
            
            # Weights auf 1 setzen (Minimum) - Contract validiert weight > 0
            # Scores werden durch Milestone-System + Follow-Bonus verwaltet
            # Minimale Weights (1) vermeiden Double-Minting aber erfüllen Contract-Validierung
            weight_initiator = 1
            weight_responder = 1
            
            # Build transaction with all 6 parameters
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            record_tx = self.resonance_registry.functions.recordInteraction(
                initiator_addr,          # follower
                responder_addr,          # creator
                link_id,                 # linkId (bytes32)
                interaction_type,        # actionType (uint8)
                weight_initiator,        # weightFollower (uint256)
                weight_responder         # weightCreator (uint256)
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 500000,  # Erhöht von 300000 → 500000 (out of gas fix #2)
                'maxFeePerGas': self.w3.eth.gas_price * 2,
                'maxPriorityFeePerGas': self.w3.eth.gas_price,
                'chainId': 84532
            })
            
            # Sign and send
            signed_tx = self.w3.eth.account.sign_transaction(record_tx, self.private_key)
            raw_tx = getattr(signed_tx, 'rawTransaction', getattr(signed_tx, 'raw_transaction', None))
            if raw_tx is None:
                raise ValueError("Could not get raw transaction from signed transaction")
            tx_hash = self.w3.eth.send_raw_transaction(raw_tx)
            tx_hash_hex = tx_hash.hex()
            
            logger.info(f"⛓️ Interaction recorded: {tx_hash_hex}")
            logger.info(f"   → Initiator: {initiator}")
            logger.info(f"   → Responder: {responder}")
            logger.info(f"   → Type: {interaction_type}")
            
            return True, {
                "tx_hash": tx_hash_hex,
                "status": "pending",
                "basescan_url": f"https://sepolia.basescan.org/tx/{tx_hash_hex}"
            }
            
        except Exception as e:
            logger.error(f"Error recording interaction: {e}")
            return False, {"error": str(e)}
    
    async def get_user_interactions(
        self, 
        address: str, 
        offset: int = 0, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get user interactions from blockchain using events"""
        try:
            if not self.resonance_registry:
                logger.warning("Resonance Registry contract not initialized")
                return []
            
            checksum_address = Web3.to_checksum_address(address)
            
            # Get InteractionRecorded events for this user
            # Event signature: InteractionRecorded(address indexed initiator, address indexed responder, uint256 interactionType, uint256 timestamp, string metadata)
            
            # Create event filter for events where user is initiator OR responder
            # Note: BASE Sepolia RPC limits queries to 100k blocks max
            # Query last 50k blocks (roughly last few days at 2 sec/block = ~27 hours)
            current_block = self.w3.eth.block_number
            from_block = max(0, current_block - 50000)
            to_block = 'latest'
            
            logger.info(f"🔍 Querying interactions from block {from_block:,} to {to_block} ({current_block - from_block:,} blocks)")
            
            # Get events where user is initiator (follower) (using get_logs instead of create_filter)
            try:
                initiator_events = self.resonance_registry.events.InteractionRecorded.get_logs(
                    fromBlock=from_block,
                    toBlock=to_block,
                    argument_filters={'follower': checksum_address}
                )
            except Exception as e:
                logger.warning(f"Could not get initiator events: {e}")
                initiator_events = []
            
            # Get events where user is responder (creator)
            try:
                responder_events = self.resonance_registry.events.InteractionRecorded.get_logs(
                    fromBlock=from_block,
                    toBlock=to_block,
                    argument_filters={'creator': checksum_address}
                )
            except Exception as e:
                logger.warning(f"Could not get responder events: {e}")
                responder_events = []
            
            # Combine and deduplicate events
            all_events = list(initiator_events) + list(responder_events)
            seen_tx = set()
            unique_events = []
            
            for event in all_events:
                tx_hash = event['transactionHash'].hex()
                if tx_hash not in seen_tx:
                    seen_tx.add(tx_hash)
                    unique_events.append(event)
            
            # Sort by block number (newest first)
            unique_events.sort(key=lambda x: x['blockNumber'], reverse=True)
            
            # Apply pagination
            paginated_events = unique_events[offset:offset + limit]
            
            # Format response
            result = []
            for event in paginated_events:
                args = event['args']
                result.append({
                    "initiator": args['follower'],        # follower = initiator
                    "responder": args['creator'],         # creator = responder
                    "interaction_type": args['actionType'],
                    "timestamp": args['timestamp'],
                    "link_id": args['linkId'].hex(),      # bytes32 to hex string
                    "weight_follower": args['weightFollower'],
                    "weight_creator": args['weightCreator'],
                    "tx_hash": event['transactionHash'].hex(),
                    "block_number": event['blockNumber']
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting interactions for {address}: {e}")
            return []
    
    async def get_blockchain_health(self) -> Dict[str, Any]:
        """Get blockchain connection health status"""
        try:
            # Test connection
            block_number = self.w3.eth.block_number
            gas_price = self.w3.eth.gas_price
            
            result = {
                "status": "connected",
                "block_number": block_number,
                "gas_price_gwei": float(Web3.from_wei(gas_price, 'gwei')),
                "rpc_url": self.rpc_url,
                "chain_id": 84532
            }
            
            # Add backend wallet info if available
            if self.account:
                balance = self.w3.eth.get_balance(self.account.address)
                balance_eth = Web3.from_wei(balance, 'ether')
                result["backend_balance_eth"] = float(balance_eth)
                result["backend_address"] = self.account.address
            else:
                result["mode"] = "read-only"
            
            return result
            
        except Exception as e:
            logger.error(f"Blockchain health check failed: {e}")
            return {
                "status": "disconnected",
                "error": str(e)
            }


# Global instance
web3_service = Web3Service()
