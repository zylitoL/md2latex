#!/usr/bin/env python

"""line_latex.py: Converts Markdown lines to LaTeX."""

__authors__ = "DeVon Young Herr, Jacob Scott Moore"


def line_latex(line: str) -> str:
    """
    This function converts all in-lane Markdown formatting to its equivalent LaTeX code.
    :param line: the Markdown text
    :return: the equivalent LaTeX code
    """

    if not line:
        return ""

    if "$$" in line:
        return line

    # check for horizontal rule

    if line == "***" or line == "---" or line == "___":
        return "\\noindent\\rule{\\textwidth}{0.4pt}"

    if line[0:5] == "#### ":
        return "\\subsubsection{" + line_latex(line[5:]) + "}"
    elif line[0:4] == "### ":
        return "\\subsection{" + line_latex(line[4:]) + "}"
    elif line[0:3] == "## ":
        return "\\section{" + line_latex(line[3:]) + "}"
    elif line[0:2] == "# ":
        return "\\title{" + line_latex(line[2:]) + "}\n" + "\\maketitle"

    # various formatting modes to be in
    math = False

    asterisks = 0
    bf = False
    it = False

    tildes = 0
    sout = False

    verb = False

    latex = ""

    for char in line:
        if char == "`":
            if math:
                latex += char
            elif verb:
                latex += "|"
                verb = False
            else:
                latex += "\\verb|"
                verb = True

        elif char == "$":
            if verb:
                latex += char
            elif math:
                latex += "$"
                math = False
            else:
                latex += "$"
                math = True

        elif char == "*":
            asterisks += 1
        elif char == "~":
            tildes += 1

        elif math or verb or (asterisks == 0 and tildes == 0):
            latex += char

        elif asterisks == 3:
            if bf or it:
                latex += "}}" + char
                asterisks = 0
                bf, it = False, False
            else:
                latex += "\\textbf{\\textit{" + char
                asterisks = 0
                bf, it, = True, True
        elif asterisks == 2:
            if bf:
                latex += "}" + char
                asterisks = 0
                bf = False
            else:
                latex += "\\textbf{" + char
                asterisks = 0
                bf = True
        elif asterisks == 1:
            if it:
                latex += "}" + char
                asterisks = 0
                it = False
            else:
                latex += "\\textit{" + char
                asterisks = 0
                it = True
        elif tildes == 2:
            if sout:
                latex += "}" + char
                tildes = 0
                sout = False
            else:
                latex += "\\sout{" + char
                tildes = 0
                sout = True
        elif tildes == 1:
            latex += "~" + char
            tildes = 0

    if bf and it:
        latex += "}}"
    elif bf or it:
        latex += "}"

    return latex
