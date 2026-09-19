# Mini Blockchain

**Blockchain Technology — Project 1: Building a Mini-Blockchain**
Industrial Training Project (DecodeLabs)

## Project Objective

The goal of this project is to understand the **cryptographic foundation of a
distributed ledger** by building a simplified blockchain from scratch, using
only Python's standard library. Rather than using an existing blockchain
framework, this project implements the underlying data structures, hashing,
linking, mining, and validation logic manually, so the core concepts are
fully transparent.

## Technologies Used

- **Python 3** (standard library only)
- `hashlib` — for SHA-256 cryptographic hashing
- `time` — for block timestamps

No external packages or blockchain libraries are used. No database, web
framework, or real cryptocurrency network is involved — this is a
self-contained educational simulation of a **single-node** blockchain.

## What Blockchain Is Being Demonstrated

This project demonstrates the fundamental structure common to almost all
blockchains: a sequence of data records ("blocks") that are cryptographically
chained together, where any attempt to alter past data is detectable. It
does **not** implement networking, peer-to-peer consensus across multiple
nodes, wallets, or real cryptocurrency transfer — those are outside the
scope of Project 1, which focuses specifically on the cryptographic
foundation (hashing, linking, and validation) of a single ledger.

## What a Block Is

A **block** is one entry in the ledger. In this project, each `Block` object
stores:

| Field           | Meaning                                                        |
|-----------------|------------------------------------------------------------------|
| `index`         | The block's position in the chain (0 is the genesis block)     |
| `timestamp`     | The moment the block was created                                |
| `transaction`   | The data/payload being stored (e.g. `"Alice -> Bob: 10 coins"`) |
| `previous_hash` | The hash of the block immediately before this one               |
| `nonce`         | A counter adjusted during mining (Proof of Work)                |
| `hash`          | This block's own SHA-256 hash, derived from all fields above    |

## What Hashing Is, and Why SHA-256

A **hash function** takes any input data and deterministically converts it
into a fixed-length string of characters (a "digital fingerprint"). SHA-256
(Secure Hash Algorithm, 256-bit) is used here because it has properties that
make it ideal for this purpose:

- **Deterministic** — the same input always produces the same hash, so any
  node can independently verify a block.
- **One-way** — it is computationally infeasible to reconstruct the original
  data from the hash alone.
- **Avalanche effect** — changing even a single character of the input
  produces a completely different hash, making tampering easy to spot.
- **Collision-resistant** — it's astronomically unlikely for two different
  inputs to produce the same hash.

SHA-256 is also the same hash function used by Bitcoin, making it a natural
and realistic choice for an educational blockchain.

## The Genesis Block

The **genesis block** is the very first block in the chain (`index = 0`). It
has no real predecessor, so its `previous_hash` is hardcoded to `"0"` by
convention. Every other block in the chain ultimately traces its lineage
back to this one block.

## How Blocks Are Linked

Every block (other than the genesis block) stores the hash of the block
that came directly before it, in its `previous_hash` field. This turns the
chain into a kind of cryptographic linked list:

```
Block 0 (Genesis)        Block 1                    Block 2
previous_hash = "0"      previous_hash = hash(B0)   previous_hash = hash(B1)
hash = H0        ------> hash = H1          ------> hash = H2
```

Because each block's hash is calculated *from* its `previous_hash`, changing
any block also changes that block's hash — which breaks the link expected by
every block that comes after it.

## How Mining Works

Mining in this project is a simplified **Proof of Work (PoW)** mechanism.
Each `Blockchain` has a configurable `difficulty` (default: `2`). To "mine"
a new block, the program:

1. Sets `nonce = 0`.
2. Calculates the block's SHA-256 hash from its index, timestamp,
   transaction, previous hash, and nonce.
3. Checks whether the resulting hash starts with `difficulty` leading
   zeros (e.g. `"00..."` for difficulty 2).
4. If not, increments the nonce by 1 and repeats from step 2.
5. Once a qualifying hash is found, the block is considered "mined" and is
   appended to the chain.

This models — in a simplified, fast-running way — the real-world idea that
producing a valid block should require measurable computational effort,
rather than being instant and free.

## How Validation Works

`Blockchain.is_chain_valid()` walks through the chain from block 1 onward
(the genesis block has no parent to check against) and performs **two
checks on every block**:

1. **Stored Hash Integrity** — recalculate the block's hash from its
   *current* data and compare it to the hash stored on the block. If they
   differ, the block's data was changed after being mined.
2. **Previous Hash Linkage** — confirm that the block's `previous_hash`
   still equals the actual hash of the block before it. If they differ, a
   block was altered upstream, removed, inserted, or reordered.

If either check fails for any block, the entire chain is reported invalid.

## How Tampering Is Detected

`main.py` demonstrates this directly: after building the chain, it modifies
`chain[1].transaction` **without** re-mining that block. This simulates an
attacker secretly editing historical data. When `is_chain_valid()` runs
again:

- **Check 1 fails immediately** for Block #1, because recalculating its
  hash from the new (tampered) transaction no longer matches the hash that
  was stored when it was originally mined.

In a full multi-block tamper scenario, this mismatch would also cascade:
every block after the tampered one would fail Check 2, since their
`previous_hash` values were computed against the *original* hash, not the
new, changed one. The demo above stops as soon as the first check fails,
which is enough to prove the chain is invalid.

## Project Structure

```
mini-blockchain/
│
├── README.md          # This file
├── requirements.txt    # Dependency information (none required)
├── blockchain.py        # Block and Blockchain classes (core logic)
├── main.py              # Demonstration script
└── .gitignore           # Standard Python ignore rules
```

## Installation / Setup

1. Make sure **Python 3.7+** is installed:
   ```
   python3 --version
   ```
2. No external packages need to be installed — this project uses only the
   Python standard library. (See `requirements.txt`.)
3. Place all project files in a single folder, `mini-blockchain/`, exactly
   as shown in the project structure above.

## How to Run the Project

From inside the `mini-blockchain/` folder, run:

```
python3 main.py
```

The program will:
1. Create the blockchain and its genesis block.
2. Mine and add three sample transactions.
3. Print every block's details.
4. Report whether the chain is valid.
5. Tamper with a block and report that the chain is now invalid.

## Expected Output

Output will vary slightly (timestamps, hashes, and nonces depend on the
current time and the mining process), but the structure will look like
this:

```
==================================================
MINI BLOCKCHAIN DEMONSTRATION
==================================================

Mining blocks, please wait...

Block #0
Timestamp:     1234567890.12
Transaction:   Genesis Block
Previous Hash: 0
Hash:          8ef8da1df565dcfe7cd060bbdfcaffcb...
Nonce:         0
--------------------------------------------------
Block #1
Timestamp:     1234567890.45
Transaction:   Alice -> Bob: 10 coins
Previous Hash: 8ef8da1df565dcfe7cd060bbdfcaffcb...
Hash:          00e4b4658a483dc5eb36ba13fcef4884...
Nonce:         107
--------------------------------------------------
Block #2
Transaction:   Bob -> Charlie: 5 coins
...
--------------------------------------------------
Block #3
Transaction:   Charlie -> David: 2 coins
...
--------------------------------------------------
Blockchain valid: True

--------------------------------------------------
TAMPERING TEST
--------------------------------------------------

Modified Block #1 transaction (without re-mining).

Blockchain valid after tampering: False

==================================================
END OF DEMONSTRATION
==================================================
```

Note that the mined hashes for blocks 1–3 begin with `00`, because the
default mining difficulty is `2`. Hashes and nonce values themselves are
never hard-coded — they are calculated dynamically every time the program
runs.

## Possible Future Improvements

- Increase mining `difficulty` to make Proof of Work more noticeable.
- Persist the chain to a file (e.g. JSON) so it survives between runs.
- Support multiple transactions per block instead of one payload per block.
- Simulate multiple nodes and a basic peer-to-peer consensus mechanism.
- Add digital signatures (e.g. using `hmac` or asymmetric keys) so
  transactions can be cryptographically attributed to a sender.
- Add a Merkle tree to summarize multiple transactions within one block.

## How Each Part Satisfies the Assignment Requirements

| Requirement                                   | Where it's implemented                                             |
|------------------------------------------------|----------------------------------------------------------------------|
| Block class with payload + hash               | `Block` class in `blockchain.py`                                    |
| Index, timestamp, previous hash, current hash | `Block.__init__` fields                                              |
| Cryptographic hashing algorithm               | `Block.calculate_hash()` using `hashlib.sha256`                     |
| Blockchain class maintaining a chain          | `Blockchain.chain` (a list of `Block` objects)                      |
| Chain validation                              | `Blockchain.is_chain_valid()`                                       |
| Detects modified block data/hash              | Check 1 in `is_chain_valid()`                                       |
| Detects tampered block relationships          | Check 2 in `is_chain_valid()`                                       |
| Simple mining logic using hashing             | `Block.mine_block()`                                                 |
| New block connects to previous block          | `Blockchain.add_block()` sets `previous_hash` from the last block   |
| Genesis block                                 | `Blockchain.create_genesis_block()`                                  |
| Demo: add several blocks + display hashes     | `main.py`                                                             |
| Demo: valid chain, then tampering detection   | `main.py`, tampering test section                                    |

## How to Demonstrate This Project to Your Instructor

1. Open a terminal in the `mini-blockchain/` folder and run `python3 main.py`
   live, so the instructor sees the mining and output happen in real time.
2. Point out that the genesis block's `Previous Hash` is `0`, and that each
   following block's `Previous Hash` exactly matches the `Hash` of the block
   before it — this is the visual proof of the chain linkage.
3. Note that the mined hashes for blocks 1–3 start with `00` (the
   configured difficulty), showing Proof of Work in action, and that the
   `Nonce` values differ block to block, since each required a different
   amount of "work" to find a valid hash.
4. Show `Blockchain valid: True` for the untouched chain.
5. Walk through the tampering section of `main.py`: explain that
   `chain[1].transaction` is changed directly, without re-mining.
6. Show `Blockchain valid after tampering: False`, and explain (using the
   README's "How Tampering Is Detected" section) exactly which validation
   check caught it.
7. Optionally, open `blockchain.py` and walk through `calculate_hash()`,
   `mine_block()`, and `is_chain_valid()` line by line to show the logic is
   original and fully understood, not copied from an external tutorial.

## Assumptions Made

Since the official brief did not specify every detail, the following
reasonable assumptions were made:

- **Mining difficulty** defaults to `2` (hashes must start with `"00"`).
  This is high enough to visibly demonstrate Proof of Work but low enough
  that the demo runs almost instantly, which suits a classroom
  demonstration.
- **One transaction per block** (a single string payload) is used, rather
  than a list of multiple transactions per block, to keep the data
  structure simple per the "keep implementation understandable" guidance.
- **Timestamps** are stored as raw Unix time (`time.time()`) internally for
  determinism and hashing, and are only formatted as human-readable dates
  when printing (see `Block.__str__` in `blockchain.py`).
- **Tampering demonstration** modifies a block's `transaction` field
  directly in memory (simulating an attacker editing stored data) rather
  than modifying the `hash` field itself, since editing the transaction
  without re-mining is the more realistic and more illustrative attack
  scenario.
