import re

regex_m = re.compile(r" *:-+: *")
regex_l = re.compile(r" *:-+ *")
regex_r = re.compile(r" *-+: *")


class Table:
    def __init__(self, header, alignment, lines):
        self.headers = header.split("|")[1:-1]

        # parse the tubes into LaTeX alignment characters

        tubes = alignment.split("|")[1:-1]
        self.alignment = []
        for tube in tubes:
            if regex_m.match(tube):
                self.alignment.append("c")
            elif regex_l.match(tube):
                self.alignment.append("l")
            elif regex_r.match(tube):
                self.alignment.append("r")

        # parse the Markdown lines into LaTeX table cells

        self.rows = []
        for line in lines:
            self.rows.append(line.split("|")[1:-1])

    def latex_header(self):
        res = ""
        for header in self.headers:
            res += " \\textbf{" + header + "} " + "&"
        res = res[1:-1]
        res += " \\\\"
        return res

    def latex_alignment(self):
        res = ""
        for char in self.alignment:
            res += char + "|"
        return res[0:-1]

    def __str__(self):
        res = "\\begin{center}\n" + \
              "\\begin{tabular}{" + self.latex_alignment() + "}\n" +\
              "    \\hline\n" + \
              "    " + self.latex_header() + "\n" + \
              "    \\hline\n" + \
              "    \\hline\n"
        for row in self.rows:
            res += "    "
            for cell in row:
                res += cell + " & "
            res = res[:-2] + "\\\\\n"
            res += "    \\hline\n"

        res += "\\end{tabular}\n" + \
               "\\end{center}"
        return res
