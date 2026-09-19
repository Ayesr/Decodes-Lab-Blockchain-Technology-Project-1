"""
blockchain.py
--------------
Core data structures for a minimal educational blockchain.

This module defines two classes:

1. Block       - a single unit of data in the chain (a "ledger entry").
2. Blockchain  - a container that links Blocks together and can verify
                  that the whole chain is still intact.

Everything here uses only Python's standard library. The cryptographic
hashing algorithm used throughout is SHA-256 (via hashlib), which is the
same hashing primitive used by real-world blockchains such as Bitcoin.
"""

import hashlib
import time


class Block:
    """
    Represents a single block in the blockchain.

    Each block stores:
        index         - the block's position in the chain (0 = genesis block)
        timestamp     - when the block was created
        transaction   - the payload / data being stored (e.g. "Alice -> Bob: 10 coins")
        previous_hash - the hash of the block that comes before this one
        nonce         - a counter used during mining (Proof of Work)
        hash          - this block's own hash, calculated from all the fields above

    The "previous_hash" field is what actually creates the *chain*: every
    block cryptographically points to the block before it. If any earlier
    block's data changes, its hash changes, which breaks this link.
    """

    def __init__(self, index, transaction, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.nonce = 0  # Will be adjusted during mining (Proof of Work)
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculate the SHA-256 hash of this block's contents.

        The hash is calculated from index, timestamp, transaction data,
        previous_hash, and nonce. Because this is deterministic, hashing
        the exact same inputs will ALWAYS produce the exact same output.
        If even a single character of the transaction data changes, the
        resulting hash will be completely different (the "avalanche effect").

        We build one combined string from all the important fields, encode
        it to bytes, and feed it into hashlib.sha256().
        """
        block_contents = (
            str(self.index)
            + str(self.timestamp)
            + str(self.transaction)
            + str(self.previous_hash)
            + str(self.nonce)
        )
        # hexdigest() returns the hash as a readable hexadecimal string
        return hashlib.sha256(block_contents.encode()).hexdigest()

    def mine_block(self, difficulty):
        """
        Very simple Proof-of-Work mining loop.

        "Mining" here means: keep changing the nonce and recalculating the
        hash until the hash happens to start with a certain number of
        leading zeros (defined by `difficulty`). This simulates the idea
        that creating a valid block should require real computational
        effort, not just cost nothing.

        This is a simplified teaching version of Proof of Work - it is
        NOT the actual Bitcoin mining algorithm, just enough logic to
        demonstrate the concept clearly.
        """
        target = "0" * difficulty  # e.g. difficulty=2 -> target = "00"

        # Keep trying new nonce values until the hash starts with `target`
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

        return self.hash

    def __str__(self):
        """Human-readable representation of the block, used when printing."""
        readable_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp)
        )
        return (
            f"Block #{self.index}\n"
            f"Timestamp: {readable_time}\n"
            f"Transaction: {self.transaction}\n"
            f"Previous Hash: {self.previous_hash}\n"
            f"Hash: {self.hash}\n"
            f"Nonce: {self.nonce}"
        )


class Blockchain:
    """
    Represents the full chain of blocks.

    Responsibilities:
        - Create the very first block (the "genesis block")
        - Add new blocks, linking each one to the block before it
        - Validate the entire chain to detect tampering
    """

    def __init__(self, difficulty=2):
        # difficulty controls how many leading zeros a mined hash must have.
        # Higher difficulty = more mining work required. Kept small here
        # (2) so the demo runs almost instantly.
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """
        The genesis block is the very first block in the chain.

        It has no real predecessor, so its previous_hash is hardcoded to
        "0" by convention. Every other block in the chain will eventually
        trace its lineage back to this one block.
        """
        return Block(index=0, transaction="Genesis Block", previous_hash="0")

    def get_latest_block(self):
        """Return the most recently added block (the current end of the chain)."""
        return self.chain[-1]

    def add_block(self, transaction):
        """
        Create a new block for the given transaction, mine it, and append
        it to the chain.

        The new block's previous_hash is set to the hash of the current
        last block - this is the step that actually "links" the new block
        into the chain.
        """
        previous_block = self.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            transaction=transaction,
            previous_hash=previous_block.hash,
        )

        # Mine the block: repeatedly hash until we find a valid nonce.
        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        """
        Walk through the entire chain and verify two things for every
        block (starting from block #1, since block #0 has no parent):

        Check 1 - Stored Hash Integrity:
            Recalculate the block's hash from its current data and compare
            it to the hash stored on the block. If they don't match, the
            block's data (e.g. the transaction) was modified after the
            fact, WITHOUT re-mining it - i.e. tampering.

        Check 2 - Previous Hash Linkage:
            Confirm that this block's `previous_hash` still matches the
            actual hash of the block before it in the chain. If it
            doesn't, a block was removed, inserted, or blocks were
            reordered.

        If either check fails for any block, the whole chain is considered
        invalid - a single broken link invalidates everything after it.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check 1: has this block's own data been tampered with?
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check 2: is this block still correctly linked to its parent?
            if current_block.previous_hash != previous_block.hash:
                return False

        return True
