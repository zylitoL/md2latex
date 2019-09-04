#!/usr/bin/env python

"""section_latex.py: Converts Markdown section headers to LaTeX."""

__authors__ = "DeVon Young Herr, Jacob Scott Moore"


def section_latex(line: str) -> str:
    """
    This function takes a Markdown line and replaces its header formatting with its LaTeX equivalent.
    :param line: the original Markdown text
    :return: the LaTex equivalent
    """
    if "####" in line:
        return "\\subsubsection{" + line[5:] + "}"

    if "###" in line:
        return "\\subsection{" + line[4:] + "}"

    if "##" in line:
        return "\\section{" + line[3:] + "}"

    if "#" in line:
        return "\\title{" + line[2:] + "}"
        
