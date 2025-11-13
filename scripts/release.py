#!/usr/bin/env python3
import subprocess
import sys


def run_command(cmd: list[str]) -> None:
    """Run a command and exit on failure."""
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)


def main() -> None:
    """Release the package."""
    # Run quality checks
    print("Running quality checks...")
    run_command(["uv", "run", "pytest"])
    run_command(["uv", "run", "black", "--check", "src", "tests"])
    run_command(["uv", "run", "ruff", "check", "src", "tests"])
    run_command(["uv", "run", "mypy", "src"])

    # Build and publish
    print("Building package...")
    run_command(["uv", "build"])

    # print("Publishing package...")
    # run_command(["uv", "publish"])


if __name__ == "__main__":
    main()
