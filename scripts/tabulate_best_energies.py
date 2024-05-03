import argparse
import os
import pandas as pd
import re
import tqdm


def _get_total_time(log_text: str, is_dwave_qa: bool) -> float:
    """
    Get the total wall-clock time from the appropriate log line.
    """

    if is_dwave_qa:
        # Quantum annealing logs differ from the traditional format by extending
        # the data to include the total D-Wave API execution time. This "total
        # time" is the last entry in the comma-separated list of measurements.
        return float(log_text.split(',')[-1].strip())
    else:
        # For other algorithms, the solve time is used for `total_time`.
        return float(log_text.split(',')[7].strip())


def _get_energy_and_solve_times(path: str) -> tuple:
    """
    Get important solution and timing data from the log file. Returns a tuple
    containing the solve time, total wall-clock time, and best energy obtained.
    """

    # Check for existence of the input file.
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path) as f:
        # Read the file as a string.
        file_string = f.read()

        # Ensure file string contains a `BQP_DATA` entry.
        if "BQP_DATA" not in file_string:
            raise ValueError(f"No `BQP_DATA` entry found in file: {path}")

        # Get line corresponding to the `BQP_DATA` entry.
        line = re.findall("BQP_DATA.*$", file_string, re.MULTILINE)[0]

        # Get measured energy, solve time, and total time.
        energy = float(line.split(',')[3].strip())
        solve_time = float(line.split(',')[7].strip())
        is_dwave_qa = 'qa' in path and '_dwave_' in path
        total_time = _get_total_time(line, is_dwave_qa)

        if total_time < solve_time:
            # The "total time" should not be less than the "solve time," which
            # does not include API-related execution time.
            raise ValueError(f"Total time is less than solve time in {path}.")

        # Return solve time, total wall-clock time, and best energy obtained.
        return solve_time, total_time, energy


def _path_has_bqp_data(path: str) -> bool:
    """
    Check if the output file contains a `BQP_DATA` field.
    """

    if os.path.exists(path):
        with open(path) as f:
            file_string = f.read()
            return "BQP_DATA" in file_string
    else:
        return False


def _get_master_df(experiment_directory: str) -> pd.DataFrame:
    """
    Get a master dataframe containing all solution data.
    """

    # Instantiate the dataframe where solution data will be stored.
    df = pd.DataFrame(columns = ['instance', 'time_group', 'solver', 'energy', 'solve_time'])

    # Get all subdirectories containing solution data with the desired instance prefix.
    subdirectories = [f.path for f in os.scandir(experiment_directory) if f.is_dir()]
    solution_subdirectories = [f for f in subdirectories]

    for subdirectory in tqdm.tqdm(solution_subdirectories):
       # Get important metadata by parsing the path of the file.
       time_group = subdirectory.split('/')[-1].split('_')[-1]
       solver = '_'.join(subdirectory.split('/')[-1].split('_')[:-1])

       # Get the directory containing the output fies in the subdirectory. There
       # should only be one directory in the subdirectory due to the structure.
       directory = [f for f in os.scandir(subdirectory)][0].path
       output_names = [f for f in os.listdir(directory) if '.stdout' in f]

       for path in [os.path.join(directory, f) for f in output_names]:
           if _path_has_bqp_data(path):
                # Get important solution and timing data from the log file.
                solve_time, total_time, energy = _get_energy_and_solve_times(path)

                # Get the full instance name (e.g., `Pegasus-Lattice_Size-16_00027`).
                instance = os.path.basename(path).replace('.stdout', '')

                # Construct a new row to be appended to the dataframe.
                new_row = pd.DataFrame(
                    [
                        {
                            'instance': instance,
                            'solver': solver,
                            'time_group': time_group,
                            'energy': energy,
                            'solve_time': solve_time,
                            'total_time': total_time
                        }
                    ]
                )
    
                # Append the new row to the dataframe.
                df = pd.concat(
                    [
                        df if not df.empty else None, new_row
                    ],
                    ignore_index = True
                )

    # Return the master dataframe.
    return df

def tabulate_best_energies(experiment_directory: str, output_path: str):
    """
    Tabulate the best solutions found by each solver for each instance. Write
    the results to a CSV file at the specified output path.
    """

    # Get the master dataframe containing all solution data.
    df = _get_master_df(experiment_directory)

    # Build a dataframe where columns are the solvers and rows are the
    # instances. For each instance, show the minimum energy for each solver.
    pivot_df = df.pivot_table(
        index = 'instance',
        columns = 'solver',
        values = 'energy',
        aggfunc = 'min'
    )

    # Add a new column to the pivot table showing the best (minimum) energy
    # found for each instance across all solvers.
    pivot_df['best_energy'] = pivot_df.min(axis = 1)

    # Write the pivot table to a CSV file.
    pivot_df.to_csv(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_directory",
        "-i",
        type = str,
        required = True,
        help = "Path to the experiment directory."
    )
    parser.add_argument(
        "--output_path",
        "-o",
        type = str,
        required = True,
        help = "Path to the output CSV file."
    )
    args = parser.parse_args()

    tabulate_best_energies(args.input_directory, args.output_path)