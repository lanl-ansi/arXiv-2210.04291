import argparse
import os
import bqpjson
import json
import re


def _read_assignment_values(path: str) -> list:
    """
    Read the assignment of spins from a result log file.
    """

    # Ensure the file exists.
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path) as f:
        # Read the file as a string.
        file_string = f.read()

        # Ensure file string contains a `BQP_SOLUTION` entry.
        if "BQP_SOLUTION" not in file_string:
            raise ValueError(f"No `BQP_SOLUTION` entry found in file: {path}")

        # Get the line corresponding to the `BQP_SOLUTION` entry.
        line = re.findall("BQP_SOLUTION.*$", file_string, re.MULTILINE)[0]

        # Extract the assignment of spins from the line.
        values = [float(x.strip().replace(' ', '')) for x in line.split(',')[5:]]

    # Return the assignment of spins.
    return values


def _read_bqpjson(path: str) -> dict:
    # Check for existence of the input file.
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    # Read the input file and parse the JSON data.
    with open(path, "r") as f:
        data = json.load(f)

    # Validate data against bqpjson schema.
    bqpjson.validate(data)

    # Return the parsed JSON data.
    return data


def _compute_energy(data: dict, assignment: dict) -> float:
    """
    Compute the energy of an assignment for a given Ising instance.
    """

    energy = sum(
        lt["coeff"] * assignment[lt["id"]]
        for lt in data["linear_terms"]
    )

    energy += sum(
        qt["coeff"] * assignment[qt["id_tail"]] * assignment[qt["id_head"]]
        for qt in data["quadratic_terms"]
    )

    return energy


def evaluate_assignment(instance_path: str, result_path: str):
    """
    Evaluate the energy of an assignment of spins, found in a result log file,
    for a given Ising instance, stored in a JSON file.
    """

    data = _read_bqpjson(instance_path)
    values = _read_assignment_values(result_path)
    assignment = {vid: values[i] for (i, vid) in enumerate(data["variable_ids"])}
    energy = _compute_energy(data, assignment)
    print("Energy of assignment:", energy)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance_path", help="path to instance", required=True)
    parser.add_argument("-r", "--result_path", help="path to result log", required=True)
    args = parser.parse_args()
    evaluate_assignment(args.instance_path, args.result_path)
