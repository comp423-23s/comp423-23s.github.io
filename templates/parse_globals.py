"""A script to experiment with reading in global variables from md files

Usage: python -m templates.parse_globals [path_to_md_file]
"""
import sys
from typing import Dict, List

__author__ = ["Ezri White <ezri@live.unc.edu>"]


def main():
    """Entry point of script. Expects to be run as CLI program."""
    target: str = parse_args()
    top_section: str = read_arguments(target)
    globals = convert_to_dict(top_section)
    print(globals)


def read_arguments(target: str) -> str:
    with open(target, 'r') as file:
        lines = file.readlines()
    lines = lines[1:]
    top_section = ""
    for line in lines:
        if "---" in line:
            break
        top_section += line
    return top_section


def convert_to_dict(top_section: str) -> Dict:
    """Make top variable information into a usable format.

    Input: String containing all lines in top variable section of md file.
    Returns: Converted dictionary version of this information.
    """
    list: List[str] = top_section.split("\n")
    globals = {}
    i = 0
    while i < len(list):
        if list[i][-1:] == ":":
            key = list[i][:-1].strip()
            globals[key] = []
            while list[i + 1].strip()[0] == "-":
                i += 1
                globals[key].append(list[i].strip()[2:])
        else:
            if ":" in list[i]:
                pair = list[i].split(":")
                globals[pair[0].strip()] = pair[1].strip()
        i += 1

    return globals


def parse_args() -> str:
    """Ensure correct command-line arguments are provided.

    Returns:
        Path of directory or file being bundled.
    """
    if len(sys.argv) < 2:
        print("Usage: python -m templates.parse_globals [path_to_md_file]")
        sys.exit(1)
    return sys.argv[1]


if __name__ == "__main__":
    main()
