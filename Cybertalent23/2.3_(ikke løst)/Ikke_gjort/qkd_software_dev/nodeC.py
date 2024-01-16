# Constantly runs on node C.

import os

import requests
import flask
from math import sqrt


app = flask.Flask(__name__)


# various addresses, endpoints used to talk to our qnode (qC)
QNODE_ENDPOINT = os.environ["QNODE_ADDR"]
PREPARE_ENDPOINT = f"{QNODE_ENDPOINT}/prepare_states"
TRANSMIT_ENDPOINT = f"{QNODE_ENDPOINT}/transmit_qubits"

# QTP-addresses for qA, qB, so qC can send them qubits
QNODE_A_QADDR = os.environ["QADDR_A"]
QNODE_B_QADDR = os.environ["QADDR_B"]

# the vector of the EPR-/Bell pair state (|00> + |11>)/sqrt(2) in the standard basis
BP_STATE_VEC = [[1 / sqrt(2), 0], [0, 0], [0, 0], [1 / sqrt(2), 0]]


def prepare_bell_pairs_and_split(n_bpairs):
    response = requests.post(
        PREPARE_ENDPOINT,
        json={"states": [BP_STATE_VEC] * n_bpairs},
    )
    assert response.status_code == 200, "Error preparing state!"
    d = response.json()

    r = {QNODE_A_QADDR: [], QNODE_B_QADDR: []}

    for l in d:
        [qb1_quuid, qb2_quuid] = l
        r[QNODE_A_QADDR].append(qb1_quuid)
        r[QNODE_B_QADDR].append(qb2_quuid)

    for (qaddr, quuids) in r.items():

        response = requests.post(
            TRANSMIT_ENDPOINT,
            json={"quuids": quuids, "recipient_node_id": qaddr},
        )
        d = response.json()

        assert response.status_code == 200, "Error transmitting qubits!"

    return r


@app.route("/qkd_exchange", methods=["POST"])
def qkd_handler():
    """As A and B are not directly connected via qnet, we must make entangled pairs of qubits and give them one half of each pair."""

    a_quuids = []
    b_quuids = []
    N_BPAIRS = flask.request.json["n_qubits"]
    d = prepare_bell_pairs_and_split(N_BPAIRS)
    a_quuids = d[QNODE_A_QADDR]
    b_quuids = d[QNODE_B_QADDR]

    return flask.jsonify({QNODE_A_QADDR: a_quuids, QNODE_B_QADDR: b_quuids}), 200
