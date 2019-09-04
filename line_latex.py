#!/usr/bin/env python

"""section_latex.py: Converts Markdown lines to LaTeX."""

__authors__ = "DeVon Young Herr, Jacob Scott Moore"


from link_latex import*
from section_latex import*
from emph_latex import*


def line_latex(line: str) -> str:
    """
    This function converts all in-lane Markdown formatting to its equivalent LaTeX code.
    :param line: the Markdown text
    :return: the equivalent LaTeX code
    """
    # handling headers
    line = section_latex(line)

    # handling links
    line = link_latex(line)

    # dictionary of in-line Markdown formatting tokens and LaTeX commands
    md_latex_commands = {
        "***": ["\\textbf{\\textit{", "}}"],
        "___": ["\\textbf{\\textit{", "}}"],
        "~~": ["\\sout{", "}"],
        "**": ["\\textbf{", "}"],
        "__": ["\\textbf{", "}"],
        "*": ["\\textit{", "}"],
        "_": ["\\textit{", "}"]
    }
    
    # loop through all key-value pairs
    for md, latex in md_latex_commands.items():
        line = emph_latex(line, md, latex[0], latex[1])

    return line
