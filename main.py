#!/usr/bin/env python

"""main.py: Converts Markdown files to LaTeX files"""

__authors__ = "DeVon Young Herr, Jacob Scott Moore"

from line_latex import*
from table_latex import*
from definition_latex import*
import re


def main():
    """
    This function calls in-line formatting functions and handles multi-line Markdown environments and converts to LaTeX.
    """

    # create a list of all the Markdown text

    with open(r"md.txt") as file_in:
        md = file_in.readlines()

    latex = []  # create a list to store the latex code

    # define regular expressions for later

    regex_number = re.compile(r"(^\d+)\.(.*)")
    regex_bullet = re.compile(r"^- (.*)")
    regex_highlight = re.compile(r"^```(\w+)")
    regex_table = re.compile(r"\|([\s\S]*\|)+")
    regex_admonition = re.compile(r"!!! note ([\s\S]*)")
    regex_display = re.compile(r"\$\$([\s\S]*)\$\$")

    # parameters to track delimited environments

    itemize = False
    code = False
    highlight = False
    toc = False
    table = False
    admonition = False
    definition = False
    display = False

    subset = []  # for table lines

    for line in md:

        line = line.rstrip()  # strip trailing newlines

        if "(:storage" in line:
            latex.append("% Image here.")
            continue

        # check if the line contains a definition

        l = regex_definition.match(line)

        if l and not definition:
            # remove most recent line
            subset = [latex.pop(-1), line_latex(line)]
            definition = True
            continue
        elif definition and line == "":
            # end definition environment
            latex_definition = Definition(subset)
            latex.append(str(latex_definition))
            definition = False
            subset = []
        elif l or definition:
            subset.append(line_latex(line))
            continue

        # check if the line signifies table of contents

        if line == "<!-- toc -->":
            latex.append("\\tableofcontents")
            toc = True
            continue
        # if table of contents ends, do so
        if line == "<!-- tocstop -->":
            toc = False
            continue
        # dont process the line if its a table of contents reference
        elif toc:
            continue

        # check if the line begins or ends an admonition

        l = regex_admonition.match(line)
        if l:
            # if we are in an admonition, start it
            latex.append("\\begin{tcolorbox}[title = " + line_latex(l.group(1)) + "]")
            admonition = True
            continue

        elif admonition and "!!!" in line:
            # if the current line contains !!!, end admonition
            latex.append("\\end{tcolorbox}")
            admonition = False
            continue

        # check if the line is display math

        if "$$" in line:
            l = regex_display.match(line)
            if l:
                latex.append("\\begin{equation*}")
                latex.append(l.group(1).strip())
                latex.append("\\end{equation*}")

            elif display:
                latex.append("\\end{equation*}")

            else:
                latex.append("\\begin{equation*}")

            continue

        # check if lines starts or ends code block environments

        if line == r"```":
            # if we are currently in a code environment, end it
            if code:
                latex.append("\\end{verbatim}")
                code = False
                continue
            # if we are currently in a syntax highlight environment, end it
            if highlight:
                latex.append("\\end{minted}")
                highlight = False
                continue
            # if we are not currently in a code environment, start it
            if not code:
                latex.append("\\begin{verbatim}")
                code = True
                continue

        # check if line starts a syntax highlight environment

        l = regex_highlight.match(line)
        if l:
            # if the previous line is not in a syntax highlighted environment, the current line starts a new one
            latex.append("\\begin{minted}[breaklines, linenos]{" + l.group(1) + "}")
            highlight = True
            continue
        # if we are currently in a code environment, dont modify the line
        if code or highlight:
            latex.append(line)
            continue

        line = line_latex(line)  # convert in-line markdown formatting to LaTeX formatting

        # check if line starts table environment

        l = regex_table.match(line)
        if l:
            # if the current line contains some sort of table environment, add it to the table list
            subset.append(line)
            table = True
            continue
        else:
            # if the current line does not, check to see if we are currently in a table environment
            if table:
                # if we are in a table environment, write table to list of LaTeX line
                subset.append(line)
                latex_table = Table(subset[0], subset[1], subset[2:-1])
                latex.append(latex_table)
                table = False
                subset = []
                continue

        # check if line should be in an itemize environment

        l = regex_number.match(line)
        if l:
            # if the previous line is not in an itemize environment, the current line starts a new one
            if not itemize:
                latex.append("\\begin{itemize}")
            line = "    \item[" + l.group(1) + "]" + l.group(2)
            latex.append(line)
            itemize = True
            continue

        l = regex_bullet.match(line)
        if l:
            if not itemize:
                latex.append("\\begin{itemize}")

            line = "    \item " + l.group(1)
            itemize = True
            latex.append(line)
            continue
        # if the previous line was in an itemize environment, the current line ends it
        if itemize:
            latex.append("\\end{itemize}")
            itemize = False
        latex.append(line)

        previous_line = line  # track the previous line in next iteration for definitions

    if definition:
        latex_definition = Definition(subset)
        latex.append(latex_definition)

    # write LaTeX list to file

    with open(r"latex.txt", "w") as file_out:
        for line in latex:
            file_out.write("%s\n" % line)


if __name__ == '__main__':
    main()
