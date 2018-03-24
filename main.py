from blockchain import Blockchain
from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)
blockchain = Blockchain()

# Generate a globally unique address for this node
node_identifier = "shelter-" + str(uuid4()).replace('-', '')

@app.route("/users", methods=["POST"])
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

@app.route("/transactions/purchase", methods=["POST"])
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

@app.route("/transactions/reward", methods=["POST"])
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

@app.route("/chain", methods=["GET"])
def full_chain():
    blockchain.resolve_conflicts()
    return jsonify(blockchain.chain), 200

@app.route("/users/<user_id>", methods=["GET"])
def get_balance(user_id):
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

    response = {
        "user_id": user_id,
        "balance": balance,
        "transactions": transactions
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
