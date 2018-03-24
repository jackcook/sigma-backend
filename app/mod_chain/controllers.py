from flask import Blueprint, jsonify

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
