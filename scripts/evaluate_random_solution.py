import argparse
import os
import bqpjson
import json
import random


def evaluate_random_solution(input_path: str):
    """
    Load an Ising instance from a JSON file and evaluate a random solution.
    """

    # Check for existence of the input file.
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    # Read the input file and parse the JSON data.
    with open(input_path, "r") as f:
        data = json.load(f)

    # Validate data against bqpjson schema.
    bqpjson.validate(data)

    # Ensure the model is in the spin domain.
    if data["variable_domain"] != "spin":
        raise ValueError("Model must be in the spin domain.")

    # Get the set of all variable ids.
    variable_ids = set(data["variable_ids"])

    # Generate a random assignment of spins.
    assignment = {vid: random.choice([1, -1]) for vid in variable_ids}

    # Compute the energy of the assignment.
    energy = _compute_energy(data, assignment)

    # Print the energy of the assignment.
    print(f"Energy: {energy}")


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="path to instance", required=True)
    args = parser.parse_args()
    evaluate_random_solution(args.input_path)
