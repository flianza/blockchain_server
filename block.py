import json
import hashlib

from time import time
from json_encoder import CustomJSONEncoder


class Block(object):
    def __init__(self, index, transactions, proof, previous_hash):
        self.index = index
        self.timestamp = time()
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash
        self.hash = Block.hash(self)

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True, cls=CustomJSONEncoder).encode()
        return hashlib.sha256(block_string).hexdigest()

