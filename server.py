from uuid import uuid4
from flask import Flask, jsonify, request

from blockchain import Blockchain
from json_encoder import CustomJSONEncoder

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    # reward the miner
    blockchain.new_transaction(
        sender='0',
        recipient=node_identifier,
        amount=1
    )

    previous_hash = last_block.hash
    block = blockchain.new_block(proof, previous_hash)

    return jsonify(block), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
