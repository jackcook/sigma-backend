from flask import Blueprint, jsonify, request
import json
from uuid import uuid4

# Import blockchain and shelter identifier from application
from app import blockchain, node_identifier
from app.mod_shelters.models import Shelter

# Create the shelters blueprint
mod_shelters = Blueprint("shelters", __name__, url_prefix="/shelters")

@mod_shelters.route("", methods=["GET"])
def get_shelters():
    # Set initial values to be modified as we read through blocks
    shelters = []

    # Loop through all blocks in the blockchain
    for block in blockchain.chain:
        # Loop through all transactions in each block
        for transaction in block["transactions"]:
            if transaction["type"] == "new_shelter" or transaction["type"] == "update_shelter":
                shelter_id = transaction["shelter_id"]
                name = transaction["name"]
                address = transaction["address"]
                lat = transaction["lat"]
                lng = transaction["lng"]
                data = transaction["data"]

                shelter = Shelter(shelter_id, name, address, lat, lng, data)

                if transaction["type"] == "update_shelter":
                    # If this shelter is already in the list, remove it first
                    for idx, temp_shelter in enumerate(shelters):
                        if temp_shelter.shelter_id == shelter_id:
                            shelters.pop(idx)
                            break

                shelters.append(shelter)

    # Return resulting shelters array
    return jsonify([x.serialize() for x in shelters])

@mod_shelters.route("", methods=["POST"])
def create_shelter():
    # Resolve chain conflicts before making changes
    blockchain.resolve_conflicts()

    # Run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # Generate a globally unique address for this shelter
    shelter_identifier = str(uuid4()).replace('-', '')

    # Retrieve shelter data from request
    values = request.get_json()
    name = values["name"]
    address = values["address"]
    lat = float(values["lat"])
    lng = float(values["lng"])
    data = json.loads(values["data"])

    # Create this shelter in the blockchain
    blockchain.new_transaction({
        "shelter_id": shelter_identifier,
        "name": name,
        "address": address,
        "lat": lat,
        "lng": lng,
        "data": data,
        "type": "new_shelter"
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

@mod_shelters.route("/<shelter_id>", methods=["PUT"])
def update_shelter(shelter_id):
    # Resolve chain conflicts before making changes
    blockchain.resolve_conflicts()

    # Run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # Retrieve shelter data from request
    values = request.get_json()
    name = values["name"]
    address = values["address"]
    lat = float(values["lat"])
    lng = float(values["lng"])
    data = json.loads(values["data"])

    # Create this shelter in the blockchain
    blockchain.new_transaction({
        "shelter_id": shelter_id,
        "name": name,
        "address": address,
        "lat": lat,
        "lng": lng,
        "data": data,
        "type": "update_shelter"
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
