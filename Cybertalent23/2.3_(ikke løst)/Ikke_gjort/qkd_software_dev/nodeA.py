# Runs on node A whenever it wants to do QKD with B. Traffic is proxied via C.

import hashlib
import os
import random

import requests

from qkd_utils import (bitstr_to_secret, measure, randomly_measure,
                       sign_json_dict, validate_counterparty_message)

# Regular HTTP endpoints for communicating with B, C. Communication with B is via a TCP proxy (socat) on C.
BNODE_ENDPOINT = os.environ["BNODE_ENDPOINT"]
CNODE_ENDPOINT = os.environ["CNODE_ENDPOINT"]

# QTP addresses of qA, qB
QNODE_A_QADDR = os.environ["QNODE_A_QADDR"]
QNODE_B_QADDR = os.environ["QNODE_B_QADDR"]

# The First-class Level Access Grant - should ONLY be transmitted if we are CERTAIN the QKD succeeded
FLAG = os.environ["FLAG"]

# Node C creates the entangled Bell pair states for us, and, for eahc pair, transmits one half to qA (our qnode), the other to qB
response = requests.post(f"{CNODE_ENDPOINT}/qkd_exchange", json={"n_qubits": 3000})
assert response.status_code == 200

# Next, take our halves of each pair (which are now on qA), and measure them in a basis randomly chosen from the 3 E91-basises (see qkd_utils.randomly_measure)
quuids_ours = response.json()[QNODE_A_QADDR]
quuids_theirs = response.json()[QNODE_B_QADDR]
our_outcomes = []
randseed_quuids, quuids_ours = quuids_ours[:10], quuids_ours[10:]
s = str(measure(randseed_quuids, ["B1"] * len(randseed_quuids)))
random.seed(int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16))
basises, outcomes = randomly_measure(quuids_ours)

for basis, outcome in zip(basises, outcomes):
    our_outcomes.append((basis, outcome))

# The basises we measured in can be publically shared with B, but the outcomes are kept secret for now
# To save on round-trip time, this message also serves to inform B that we are initiating a QKD exchange
# so that they know they have received a bunch of halves of entangled qubit pairs and should measure them in random basises as well
our_basises = [basis for basis, _ in our_outcomes]
payload = {"quuids_B": quuids_theirs, "basises_A": our_basises}
payload["hmac"] = sign_json_dict(payload) # Ensures nobody can tamper with this message

response = requests.post(
    f"{BNODE_ENDPOINT}/perform_qkd",
    json=payload,
)
assert response.status_code == 200, "Error transmitting QKD initialization message!"
d = response.json()
assert validate_counterparty_message(d), "Invalid counterparty message received!"

# We are now in a position to check which qubit pairs we happened to measure using the same basis, and (as they are
# entangled) have given us the same outcome and can be used as key material. B has already done this, and
# given us a checksum we can use to verify the secret, but we additionally compute Bell-esque test statistics
# which can detect an adversary listening in by e.g measuring our qubits

their_basises = d["basises"]
their_outcomes = dict(d["outcomes"])
their_checksum = d["joint_secret_checksum"]

matching_basis_indices = set()
for idx, ((our_basis, outcome), their_basis) in enumerate(
    zip(our_outcomes, their_basises)
):
    if our_basis != their_basis:
        continue
    else:
        matching_basis_indices.add(idx)

# Qubits we measured using the same basis will yield the same outcome, so B can also find this pretty random string
outcome_str = " ".join(
    [str(our_outcomes[quuid_idx][1]) for quuid_idx in sorted(matching_basis_indices)]
)
joint_secret, checksum = bitstr_to_secret(outcome_str)
assert checksum == their_checksum, "Joint secret checksum mismatch - MitM plausible!"


# In order to be certain nobody is snooping in, we verify that the qubits we measured in differing
# basises yield the expected probability of a "match" (that is, e.g. both measuring the first basis
# vector, although it will be in different basises)

num_matches = 0
N = 0
for quuid_idx in range(len(our_outcomes)):
    if quuid_idx not in their_outcomes:
        continue
    our_basis, our_outcome = our_outcomes[quuid_idx]
    their_basis, their_outcome = their_outcomes[quuid_idx]
    assert our_basis != their_basis
    if our_outcome == their_outcome:
        num_matches += 1
    N += 1

# The limits on the below check are somewhat conservative, so false positives may occasionally occur.
match_prob = num_matches / N
assert (0.225 <= match_prob <= 0.275), f"Error: MitM plausible - observed {match_prob:.2%} matches!"


# As the FLAG is so short, and our key is so long, this quick 'n dirty encryption should suffice.
# For longer communication, it should instead be used as key for some symmetric cipher, e.g. eAES.
flag_bytes = FLAG.ljust(64).encode()
assert len(flag_bytes) == 64
key_bytes = hashlib.sha512(joint_secret.encode()).digest()
assert len(key_bytes) == 64
encrypted_flag = bytes(f ^ k for f, k in zip(flag_bytes, key_bytes))

response = requests.post(
    f"{BNODE_ENDPOINT}/secrets",
    json={"encrypted_flag": encrypted_flag.hex()},
)

print("Successfully transmitted encrypted FLAG!")
