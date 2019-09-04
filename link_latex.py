#!/usr/bin/env python

"""link_latex.py: Converts Markdown format links to LaTeX."""

__authors__ = "Jacob Scott Moore, DeVon Young Herr"


def link_latex(line: str) -> str:
    """
    Function takes line input from markdown and looks for Markdown's in-text hyperlink method of "[url]{text}" and
    replaces it with the LaTeX equivalent.
    :param line: The line with a link to be processed
    :return: the LaTeX equivalent
    """

    # Look for alias-links
    while "[" in line and "(" in line:
        url = line[line.find("(") + 1: line.find(")")]
        alias = line[line.find("[") + 1: line.find("]")]
        line = line[:line.find("[")] + "\\href{" + url + "}{" + alias + "}" + line[line.find(")") + 1:]

    # Look for non-alias links
    line = line.replace("[", "\\href{")
    line = line.replace("]", "}")

    return line
