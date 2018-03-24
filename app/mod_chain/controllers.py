from flask import Blueprint, jsonify

from app import blockchain

mod_chain = Blueprint("chain", __name__, url_prefix="/chain")

@mod_chain.route("", methods=["GET"])
def full_chain():
    blockchain.resolve_conflicts()
    return jsonify(blockchain.chain)
