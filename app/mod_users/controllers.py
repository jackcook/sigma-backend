from flask import Blueprint, jsonify, request
from uuid import uuid4

from app import blockchain, node_identifier
from app.mod_users.models import User

mod_users = Blueprint("users", __name__, url_prefix="/users")

@mod_users.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    # Set initial values to be modified as we read through blocks
    user_id = None
    name = None
    balance = 0
    transactions = []

    # Loop through all blocks in the blockchain
    for block in blockchain.chain:
        # Loop through all transactions in each block
        for transaction in block["transactions"]:
            if transaction["type"] == "new_user" and transaction["user_id"] == user_id:
                # Save initial user data
                user_id = transaction["user_id"]
                name = transaction["name"]
                balance += transaction["balance"]
            elif transaction["type"] == "transaction":
                if transaction["recipient"] == user_id:
                    # Add to the balance if this user received coins
                    balance += transaction["amount"]
                    transactions.append(transaction)
                elif transaction["sender"] == user_id:
                    # Subtract from the balance if this user spent coins
                    balance -= transaction["amount"]
                    transactions.append(transaction)

    # Create the resulting user object
    user = User(user_id, name, balance, transactions)
    return jsonify(user.serialize())

@mod_users.route("", methods=["POST"])
def create_user():
    blockchain.resolve_conflicts()

    # Run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # Generate a globally unique address for this user
    user_identifier = str(uuid4()).replace("-", "")

    # Retrieve user data from request
    values = request.get_json()
    name = values["name"]

    # Add an initial amount to the new user's balance
    blockchain.new_transaction({
        "user_id": user_identifier,
        "balance": 10,
        "name": name,
        "type": "new_user"
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

    return jsonify(response)
