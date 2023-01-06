"""A script to generate static HTML files in production build.

Usage: python -m prod [path_to_md_file]
"""

__author__ = ["Kris Jordan <kris@cs.unc.edu>", "Ezri White <ezri@live.unc.edu"]

import time
import sys
import os
import subprocess
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import List, Dict


SITE_DIR = "."


def main() -> None:
    """Entrypoint of Program."""
    path = parse_args(sys.argv)
    md_file = f'{path}.md'
    body: str = capture_pandoc_html(md_file)
    top_section, bottom_section = read_arguments(md_file)
    globals = convert_to_dict(top_section)
    fixed_navbar = choose_navbar(globals)
    site_branch = choose_site_branch(globals)
    if is_overview(globals):
        overview = create_overview(md_file)
        generate_html(md_file, globals, body,
                      fixed_navbar, site_branch, overview)
    elif is_columns(globals):
        bodies = split_body(body)
        generate_html(md_file, globals, bodies, fixed_navbar, site_branch)
    elif is_rows(globals):
        bodies = split_body(body)
        generate_html(md_file, globals, bodies, fixed_navbar, site_branch)
    elif is_grid(globals):
        bodies = parse_grid(body, globals)
        generate_html(md_file, globals, bodies, fixed_navbar, site_branch)
    else:
        generate_html(md_file, globals, body, fixed_navbar, site_branch)


def choose_navbar(globals):
    """"""
    if "navbar" in globals:
        if globals["navbar"] == "fixed":
            return True
    return False


def choose_site_branch(globals):
    """Determines which branch of the site."""
    if "site-branch" in globals:
        return globals["site-branch"]
    return "student"


def is_overview(globals):
    """"""
    if "template" in globals:
        return globals["template"] == "overview"
    return False


def is_columns(globals):
    """Determines if the page should have a column layout."""
    if "template" in globals:
        return globals["template"] == "columns"
    return False


def is_rows(globals):
    """Determines if the page should have a row layout."""
    if "template" in globals:
        return globals["template"] == "rows"
    return False


def is_grid(globals):
    """Determines if the page should have a row layout."""
    if "template" in globals:
        return globals["template"] == "grid"
    return False


def split_body(body):
    """"""
    bodies = body.split('//split//')
    return bodies


def parse_grid(body, globals):
    """"""
    row_length = int(globals["row-length"])
    items = body.split('//split//')
    bodies = []
    for i in range(len(items)):
        if i % row_length == 0:
            bodies.append([])
        bodies[int(i / row_length)].append(items[i])

    return bodies


def create_overview(source):
    """"""
    output = subprocess.check_output(
        ["pandoc", "-t", "html", source, "--standalone", "--toc", "--toc-depth=3"])
    cleaned_output = output.decode("utf-8")
    cut_output = cleaned_output.split("nav")[1]
    return cut_output[26:]


def generate_html(source: str, globals, body, fixed_navbar, site_branch, overview=""):
    """Use globals to determine variables in order to generate html from jinja."""
    env = Environment(
        loader=FileSystemLoader(SITE_DIR),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True
    )
    base_template = env.get_template(choose_template(globals))
    time_stamp = time.time()
    path = source.replace("md", "html")

    with open(path, "w") as target:
        if overview == "":
            result = base_template.render(
                title=globals["title"], page=globals["page"], author=globals["author"], body=body, fixed_navbar=fixed_navbar, time_stamp=time_stamp, site_branch=site_branch)
        else:
            result = base_template.render(
                title=globals["title"], page=globals["page"], author=globals["author"], body=body, overview=overview, fixed_navbar=fixed_navbar, time_stamp=time_stamp, site_branch=site_branch)
        target.write(result)


def choose_template(globals) -> str:
    """Determine which child template to use"""
    if "template" in globals:
        template_path = f"./templates/{globals['template']}.jinja2"
    else:
        template_path = "./templates/generic.jinja2"
    return template_path


def capture_pandoc_html(source: str) -> str:
    """Generate HTML by shelling out to pandoc.

    Args:
        - source is the markdown file being transformed
        - template is the template HTML file to wrap it in

    Returns:
        - String containing pandoc output
    """
    output = subprocess.check_output(
        ["pandoc", "-t", "html", source])
    cleaned_output = output.decode("utf-8")
    return str(cleaned_output)


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


def parse_args(argv: List[str]) -> str:
    """Confirm correct usage of command and parse input.

    Args:
        - argv are the process's input arguments

    Returns:
        The path of the markdown file to convert.
    """
    if len(argv) != 2:
        print("Usage: python -m prod [path_to_md_file]", file=sys.stderr)
        exit(1)
    else:
        return argv[1]


def pandoc_html(source: str, template: str) -> None:
    """Generate HTML by shelling out to pandoc.

    Args:
        - source is the markdown file being transformed
        - template is the template HTML file to wrap it in

    Returns:
        None. Outputs a file in same path as source but html.
    """
    target = f"{source}.html"
    source = f"{source}.md"
    args = ["pandoc", source, f"-o {target}", "--standalone",
            f"--template={template}", "--toc", "--toc-depth=3"]
    command = " ".join(args)
    os.system(command)


if __name__ == "__main__":
    main()
