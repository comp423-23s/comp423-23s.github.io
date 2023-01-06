"""A development server for working with markdown."""

__author__ = ["Ezri White <ezri@live.unc.edu>"]

import time
import os
import subprocess
from shelljob.proc import CommandException
from flask import Flask, Response, abort, render_template, escape
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import List, Dict

SITE_DIR = "."


app = Flask(__name__)


@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def index(path):

    # Find target markdown file
    target: str
    if path == "":
        target = "index.md"
    elif os.path.isdir(path):
        target = f"{path}/index.md"
    else:
        path = path.replace(".html", ".md")
        if os.path.isfile(path):
            target = path
        else:
            abort(404, description="Resource not found")

    md_file: str = target
    body: str = capture_pandoc_html(md_file)
    top_section, bottom_section = read_arguments(md_file)
    globals = convert_to_dict(top_section)
    fixed_navbar = choose_navbar(globals)
    site_branch = choose_site_branch(globals)
    if is_overview(globals):
        overview = create_overview(md_file)
        generated_html = generate_html(
            globals, body, fixed_navbar, site_branch, overview)
    elif is_columns(globals):
        bodies = split_body(body)
        generated_html = generate_html(
            globals, bodies, fixed_navbar, site_branch)
    elif is_rows(globals):
        bodies = split_body(body)
        generated_html = generate_html(
            globals, bodies, fixed_navbar, site_branch)
    elif is_grid(globals):
        bodies = parse_grid(body, globals)
        generated_html = generate_html(
            globals, bodies, fixed_navbar, site_branch)
    else:
        generated_html = generate_html(
            globals, body, fixed_navbar, site_branch)
    return Response(generated_html, mimetype="text/html")


def choose_navbar(globals):
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
    """Determines if the page should have an overview layout."""
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


def generate_html(globals, body, fixed_navbar, site_branch, overview=""):
    """Use globals to determine variables in order to generate html from jinja."""
    env = Environment(
        loader=FileSystemLoader(SITE_DIR),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True
    )
    base_template = env.get_template(choose_template(globals))
    time_stamp = time.time()
    if overview == "":
        return base_template.render(
            title=globals["title"], page=globals["page"], author=globals["author"], body=body, fixed_navbar=fixed_navbar, time_stamp=time_stamp, site_branch=site_branch)
    else:
        return base_template.render(
            title=globals["title"], page=globals["page"], author=globals["author"], body=body, overview=overview, fixed_navbar=fixed_navbar, time_stamp=time_stamp, site_branch=site_branch)


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
    with open(target, 'r', encoding="utf8") as file:
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


@app.errorhandler(CommandException)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
