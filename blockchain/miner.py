import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random
import math


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...999123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    """

    start = timer()

    print("Searching for next proof")
    proof = last_proof
    #  TODO: Your code here
    # hashlib.sha256(block_string).hexdigest()

    prev_hash = hashlib.sha256(str(last_proof).encode()).hexdigest()

    while not valid_proof(prev_hash, proof):
        proof += math.floor(random.random() * 15)
        #proof = proof * -1
        #Get new proof every number of seconds, start searching for proof from that value on
        #May need to adjust timer
        # if timer() - start > 30:
        #     r = requests.get(url=node + "/last_proof")
        #     data = r.json()
        #     prev_hash = hashlib.sha256(str(data.get('proof')).encode()).hexdigest()
        #     print(f"Got new proof: {data.get('proof')}, hashed to {prev_hash}")
        #     #proof = data.get('proof')
        #     start = timer()
    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the last hash match the first six characters of the proof?

    IE:  last_hash: ...999123456, new hash 123456888...
    """

    # TODO: Your code here!
    current = hashlib.sha256(str(proof).encode()).hexdigest()
    #print(f'Checking proof {proof}, comparing {last_hash[-6:]} to {current[:6]}')

    return last_hash[-6] == current[:6]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    if len(id) == 0:
        f = open("my_id.txt", "w")
        # Generate a globally unique ID
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
