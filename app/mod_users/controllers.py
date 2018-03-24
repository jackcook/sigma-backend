from flask import Blueprint, jsonify
from uuid import uuid4

from app import blockchain, node_identifier
from app.mod_users.models import User

mod_users = Blueprint("users", __name__, url_prefix="/users")

@mod_users.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    # Set initial values to be modified
    balance = 0
    transactions = []

    for block in blockchain.chain:
        for transaction in block["transactions"]:
            if transaction["recipient"] == user_id:
                balance += transaction["amount"]
                transactions.append(transaction)
            elif transaction["sender"] == user_id:
                balance -= transaction["amount"]
                transactions.append(transaction)

    user = User(balance, transactions, user_id)
    return jsonify(user.serialize())

@mod_users.route("", methods=["POST"])
def create_user():
    blockchain.resolve_conflicts()

    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # Generate a globally unique address for this user
    user_identifier = str(uuid4()).replace('-', '')

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender=node_identifier,
        recipient=user_identifier,
        amount=10,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200
