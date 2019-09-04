#!/usr/bin/env python

"""emph_latex.py: Converts Markdown with specified tokens to specified LaTeX commands"""

__authors__ = "DeVon Young Herr, Jacob Scott Moore"


def emph_latex(target: str, md: str, latex_head: str, latex_tail: str) -> str:
    """
    this function takes a given markdown string, an emphasis string (such as ***), a LaTeX command (such as \textbf{)
    and its corresponding end (such as }) and converts it to LaTeX.
    :param target: The markdown string
    :param md: The emphasis string
    :param latex_head: The LaTeX command
    :param latex_tail: The end of the LaTeX command
    :return: The LaTeX equivalent of the markdown string
    """
    # Check if the markdown is a horizontal rule
    if target == "***" or target == "---" or target == "___":
        return "\\noindent\\rule{\\textwidth}{0.4pt}"

    # Repeatedly replace pairs of markdown emphasis strings with LaTeX commands and its ends
    while md in target:
        target = target[:target.find(md)] + latex_head + \
                 target[target.find(md) + len(md):target.find(md, target.find(md) + 1)] + latex_tail +\
                 target[target.find(md, target.find(md) + 1) + len(md):]

    return target
