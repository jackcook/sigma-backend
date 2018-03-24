from flask import Blueprint, jsonify, request

from app import blockchain, node_identifier

mod_transactions = Blueprint("transactions", __name__, url_prefix="/transactions")

@mod_transactions.route("/purchase", methods=["POST"])
def create_purchase_transaction():
    blockchain.resolve_conflicts()
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # Create a new Transaction
    blockchain.new_transaction(
        sender=values['sender'],
        recipient=node_identifier,
        amount=int(values['amount'])
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

    return jsonify(response), 201

@mod_transactions.route("/reward", methods=["POST"])
def create_reward_transaction():
    blockchain.resolve_conflicts()
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # Create a new Transaction
    blockchain.new_transaction(
        sender=node_identifier,
        recipient=values['recipient'],
        amount=int(values['amount'])
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

    return jsonify(response), 201
