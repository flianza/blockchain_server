import hashlib

from block import Block
from transaction import Transaction


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # genesis block
        self.new_block(proof=100, previous_hash=1)

    def new_block(self, proof, previous_hash=None):
        block = Block(index=len(self.chain) + 1,
                      transactions=self.current_transactions,
                      proof=proof,
                      previous_hash=previous_hash or self.chain[-1].hash)

        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append(Transaction(sender, recipient, amount))
        return self.last_block.index + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0

        while Blockchain.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha3_256(guess).hexdigest()
        return guess_hash[:4] == "0000"

