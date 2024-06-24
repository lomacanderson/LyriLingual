import argparse
import subprocess
from typing import Callable


def task(func: Callable) -> Callable:
    """
    Define function as a valid task using decorator.

    :param func: The function being
    :return: The function to call.
    """
    func.is_command = True  # type: ignore[attr-defined]
    return func


@task
def run_tests() -> None:
    """Run tests using pytest."""
    print("Running tests...")
    subprocess.check_call(["pytest"])


@task
def check_formatting() -> None:
    """Check code for formatting errors and fix where possible."""
    print("Sorting imports...")
    subprocess.check_call(["isort", "."])

    print("Formatting code with Black...")
    subprocess.check_call(["black", "."])

    print("Checking code style with Flake8...")
    subprocess.check_call(["flake8", "."])

    print("Performing type checks with MyPy...")
    subprocess.check_call(["mypy", "."])


def main() -> None:
    """Parse commands from command line."""
    parser = argparse.ArgumentParser(description="Manage project tasks")
    parser.add_argument("task", type=str, help="Task to run")
    args = parser.parse_args()

    task_func = globals().get(args.task)
    if task_func and hasattr(task_func, "is_command"):
        task_func()
    else:
        print(f"Task '{args.task}' is invalid.")


if __name__ == "__main__":
    main()
