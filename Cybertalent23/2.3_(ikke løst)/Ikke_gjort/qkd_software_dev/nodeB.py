# Constantly runs on node B. This server handle QKD with A. See nodeA.py for an explanation.


import random
import hashlib

import flask

from qkd_utils import (bitstr_to_secret, measure, randomly_measure,
                       sign_json_dict, validate_counterparty_message)

app = flask.Flask(__name__)


@app.route("/perform_qkd", methods=["POST"])
def qkd_handler():
    body = flask.request.json
    assert validate_counterparty_message(body)

    quuids_ours = body["quuids_B"]
    their_basises = body["basises_A"]
    our_outcomes = []
    randseed_quuids, quuids_ours = quuids_ours[:10], quuids_ours[10:]
    s = str(measure(randseed_quuids, ["B2"] * len(randseed_quuids)))
    random.seed(int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16))
    basises, outcomes = randomly_measure(quuids_ours)

    for basis, outcome in zip(basises, outcomes):
        our_outcomes.append((basis, outcome))

    matching_basis_indices = set()
    for idx, ((our_basis, outcome), their_basis) in enumerate(
        zip(our_outcomes, their_basises)
    ):
        if our_basis != their_basis:
            continue
        else:
            matching_basis_indices.add(idx)

    outcome_str = " ".join(
        [
            str(our_outcomes[quuid_idx][1])
            for quuid_idx in sorted(matching_basis_indices)
        ]
    )
    joint_secret, checksum = bitstr_to_secret(outcome_str)

    our_basises = [basis for (basis, _) in our_outcomes]
    outcomes_to_publicize = {
        quuid_idx: (basis, outcome)
        for quuid_idx, (basis, outcome) in enumerate(our_outcomes)
        if quuid_idx not in matching_basis_indices
    }

    payload = {
        "basises": our_basises,
        "outcomes": sorted(
            list(outcomes_to_publicize.items())
        ),  # JSON treats integer keys as strings
        "joint_secret_checksum": checksum,
    }
    payload["hmac"] = sign_json_dict(payload)
    return payload, 200


@app.route("/secrets", methods=["POST"])
def secrets_handler():
    # ---The behavior of this endpoint is classified.---
    return "REDACTED"
