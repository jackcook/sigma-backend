from uuid import uuid4

# Relative import from blockchain file
from .blockchain import Blockchain

# Create the blockchain
blockchain = Blockchain()

# Generate a globally unique address for this node
node_identifier = "shelter-" + str(uuid4()).replace('-', '')

# Configure the backend application, register all blueprints
def configure_app(app):
    from app.mod_chain.controllers import mod_chain as chain_module
    from app.mod_shelters.controllers import mod_shelters as shelters_module
    from app.mod_transactions.controllers import mod_transactions as transactions_module
    from app.mod_users.controllers import mod_users as users_module

    app.register_blueprint(chain_module)
    app.register_blueprint(shelters_module)
    app.register_blueprint(transactions_module)
    app.register_blueprint(users_module)
