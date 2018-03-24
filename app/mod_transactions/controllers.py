from flask import Blueprint, jsonify, request

# Import blockchain and shelter identifier from application
from app import blockchain, node_identifier

# Create the transactions blueprint
mod_transactions = Blueprint("transactions", __name__, url_prefix="/transactions")

@mod_transactions.route("/purchase", methods=["POST"])
def create_purchase_transaction():
    # Resolve chain conflicts before making changes
    blockchain.resolve_conflicts()

    # Run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # Get data from the URL request
    values = request.get_json()

    # Create a new transaction
    blockchain.new_transaction({
        "sender": values["sender"],
        "recipient": node_identifier,
        "amount": int(values["amount"]),
        "type": "transaction"
    })

    # Forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }

    return jsonify(response), 201

@mod_transactions.route("/reward", methods=["POST"])
def create_reward_transaction():
    # Resolve chain conflicts before making changes
    blockchain.resolve_conflicts()

    # Run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # Get data from the URL request
    values = request.get_json()

    # Create a new transaction
    blockchain.new_transaction({
        "sender": node_identifier,
        "recipient": values["recipient"],
        "amount": int(values["amount"]),
        "type": "transaction"
    })

    # Forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }

    return jsonify(response), 201
