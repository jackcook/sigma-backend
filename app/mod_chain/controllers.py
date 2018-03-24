from flask import Blueprint, jsonify, request

# Import blockchain from application
from app import blockchain

# Create the chain blueprint
mod_chain = Blueprint("chain", __name__, url_prefix="/chain")

@mod_chain.route("", methods=["GET"])
def full_chain():
    # Resolve conflicts before returning full blockchain data
    blockchain.resolve_conflicts()

    # Return all blockchain data
    return jsonify(blockchain.chain)

@mod_chain.route("/nodes", methods=["POST"])
def add_node():
    # Register node that was passed in request body
    node = request.get_json()["node"]
    blockchain.register_node(node)

    # Return all blockchain nodes
    return jsonify(list(blockchain.nodes)), 201

@mod_chain.route("/resolve", methods=["GET"])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            "message": "Our chain was replaced",
            "new_chain": blockchain.chain
        }
    else:
        response = {
            "message": "Our chain is authoritative",
            "chain": blockchain.chain
        }

    return jsonify(response)
