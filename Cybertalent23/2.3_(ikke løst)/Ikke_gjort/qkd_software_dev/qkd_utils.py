import hashlib
import hmac
import json
import os
import random
from hashlib import sha1
from math import cos, pi, sin

import requests


QNODE_ADDR = os.environ["QNODE_ADDR"]
VALIDATION_SECRET = bytes.fromhex(os.environ["VALIDATION_SECRET"])

BASISES = {
    "B0": [[[1, 0], [0, 0]], [[0, 0], [1, 0]]],  # standard basis
    "B1": [
        [[cos(2 * pi / 3), 0], [sin(2 * pi / 3), 0]],
        [[sin(2 * pi / 3), 0], [-cos(2 * pi / 3), 0]],
    ],  # standard basis rotated by 2pi/3
    "B2": [
        [[cos(4 * pi / 3), 0], [sin(4 * pi / 3), 0]],
        [[sin(4 * pi / 3), 0], [-cos(4 * pi / 3), 0]],
    ],  # standard basis rotated by 4pi/3
}


def measure(quuids, basises):

    assert len(quuids) == len(basises)

    payload = {
        "quuids": [],
        "basis_1s": [],
        "basis_2s": [],
    }
    for quuid, basis in zip(quuids, basises):
        payload["quuids"].append(quuid)
        payload["basis_1s"].append(BASISES[basis][0])
        payload["basis_2s"].append(BASISES[basis][1])

    response = requests.post(
        f"{QNODE_ADDR}/measure_qubits",
        json=payload,
    )

    assert response.status_code == 200, "Error measuring qubits!"

    return response.json()["measurement_outcomes"]


def randomly_measure(quuids):
    basises = [random.choice(("B0", "B1", "B2")) for _ in range(len(quuids))]
    return basises, measure(quuids, basises)


def sign_json_dict(json_dict):
    s = json.dumps(json_dict, sort_keys=True)
    return hmac.new(VALIDATION_SECRET, s.encode("utf-8"), sha1).hexdigest()


def validate_counterparty_message(json_dict):
    if "hmac" not in json_dict:
        return False
    mac = json_dict["hmac"]
    del json_dict["hmac"]
    expected_mac = sign_json_dict(json_dict)
    return expected_mac == mac


def _hash(s):
    return hashlib.sha512(s.encode()).digest().hex()


def bitstr_to_secret(s):
    secret_str = _hash(s)

    # Set aside 2 bytes of the joint secret to use as checksum, then re-hash it
    # to expand entropy back from 496 actual to 512 effective
    secret_str, checksum = secret_str[:-4], secret_str[-4:]
    return _hash(secret_str), checksum
