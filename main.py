#!/usr/bin/env python

"""main.py: Converts Markdown files to LaTeX files"""

__authors__ = "DeVon Young Herr, Jacob Scott Moore"

from line_latex import*
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

    # parameters to track delimited environments

    itemize = False
    code = False
    highlight = False

    for line in md:

        line = line.rstrip()  # strip trailing newlines

        line = line_latex(line)  # convert in-line markdown formatting to LaTeX formatting

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
        latex.append(line)
        itemize = False

        previous_line = line # track the previous line in next iteration for definitions

    # write LaTeX list to file

    with open(r"latex.txt", "w") as file_out:
        for line in latex:
            file_out.write("%s\n" % line)


main()
