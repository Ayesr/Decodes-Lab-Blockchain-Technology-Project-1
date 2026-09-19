"""
main.py
-------
Demonstration program for the mini-blockchain.

This script:
    1. Creates a new Blockchain (which automatically creates the genesis block).
    2. Adds three sample transactions as new, mined blocks.
    3. Prints every block in a readable format.
    4. Validates the blockchain and prints the result.
    5. Tampers with a block's data directly (bypassing normal mining) and
       validates the chain again to prove that tampering is detected.
"""

from blockchain import Blockchain


def print_block(block):
    """Print a single block in a clean, readable format."""
    print(f"Block #{block.index}")
    print(f"Timestamp:     {block.timestamp}")
    print(f"Transaction:   {block.transaction}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Hash:          {block.hash}")
    print(f"Nonce:         {block.nonce}")
    print("-" * 50)


def print_chain(blockchain):
    """Print every block currently in the blockchain."""
    for block in blockchain.chain:
        print_block(block)


def main():
    print("=" * 50)
    print("MINI BLOCKCHAIN DEMONSTRATION")
    print("=" * 50)
    print()

    # Step 1: Create the blockchain (genesis block is created automatically)
    demo_chain = Blockchain(difficulty=2)

    # Step 2: Add sample transactions as new blocks
    print("Mining blocks, please wait...\n")
    demo_chain.add_block("Alice -> Bob: 10 coins")
    demo_chain.add_block("Bob -> Charlie: 5 coins")
    demo_chain.add_block("Charlie -> David: 2 coins")

    # Step 3: Display every block in the chain
    print_chain(demo_chain)

    # Step 4: Validate the untouched blockchain
    print("Blockchain valid:", demo_chain.is_chain_valid())

    # Step 5: Demonstrate tampering
    print()
    print("-" * 50)
    print("TAMPERING TEST")
    print("-" * 50)
    print()

    # We directly modify the transaction data of Block #1, WITHOUT
    # re-mining it. This simulates an attacker trying to secretly rewrite
    # history in the ledger.
    demo_chain.chain[1].transaction = "Alice -> Bob: 1000000 coins"
    print("Modified Block #1 transaction (without re-mining).")
    print()

    # Step 6: Validate again - this should now report the chain as invalid
    print("Blockchain valid after tampering:", demo_chain.is_chain_valid())
    print()
    print("=" * 50)
    print("END OF DEMONSTRATION")
    print("=" * 50)


if __name__ == "__main__":
    main()
