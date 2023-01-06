"""A script to experiment with generating html from given md file

Uses top variables to determine which templates to use.
Will default to no title and template without overview menu.

Usage: python -m templates.generate [path_to_md_file]
"""

__author__ = ["Ezri White <ezri@live.unc.edu>"]

from jinja2 import Environment, FileSystemLoader, select_autoescape
import re
import sys
import os
from typing import List, Dict
import subprocess


SITE_DIR = "../site"


def main():
    """Entry point of script. Expects to be run as CLI program."""
    md_file: str = parse_args()
    # pandoc_html(md_file)
    body = capture_pandoc_html(md_file)
    top_section, bottom_section = read_arguments(md_file)
    globals = convert_to_dict(top_section)
    # body: str = parse_body()
    generate_html(globals, body)


def generate_html(globals, body):
    """Use globals to determine variables in order to generate html from jinja."""
    env = Environment(
        loader=FileSystemLoader(SITE_DIR),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True
    )
    base_template = env.get_template(choose_template(globals))
    with open(f"./templates/practice.html", "w") as target:
        result = base_template.render(
            title=globals["title"], page=globals["page"], body=body)
        # We strip the double spaces because pandoc can't handle HTML well :(
        stripped = re.sub(r' {2,}', '', result)
        target.write(stripped)


def choose_template(globals) -> str:
    """Determine which child template to use"""
    if "template" in globals:
        template_path = f"./templates/{globals['template']}.jinja2"
    else:
        template_path = "./templates/generic.jinja2"
    return template_path


def parse_body() -> str:
    """Get body from pandoc.html and return as string"""
    with open("./templates/pandoc.html", 'r') as file:
        lines = file.readlines()
    body = ""
    recording = False
    for line in lines:
        if "</body>" in line:
            recording = False
        if recording:
            body += line
        if "<body>" in line:
            recording = True

    return body


def pandoc_html(source: str) -> None:
    """Generate HTML by shelling out to pandoc.

    Args:
        - source is the markdown file being transformed
        - template is the template HTML file to wrap it in

    Returns:
        None. Outputs to pandoc.html for purposes of reading back in.
    """
    # use -t
    args = ["pandoc", source, f"-o ./templates/pandoc.html",
            "--standalone", "--toc", "--toc-depth=3"]
    command = " ".join(args)
    os.system(command)


def capture_pandoc_html(source: str) -> None:
    """Generate HTML by shelling out to pandoc.

    Args:
        - source is the markdown file being transformed
        - template is the template HTML file to wrap it in

    Returns:
        String containing pandoc output
    """
    output = subprocess.check_output(
        ["pandoc", "-t", "html", source])
    return output


def read_arguments(target: str):
    """Read in md file and split into top variables and markdown pieces."""
    with open(target, 'r') as file:
        lines = file.readlines()
    lines = lines[1:]
    top_section = ""
    markdown = ""
    finished_top = False
    for line in lines:
        if "---" in line:
            finished_top = True
        if finished_top:
            markdown += line
        else:
            top_section += line
    return (top_section, markdown)


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
