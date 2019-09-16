import re

regex_definition = re.compile(r"^~ ([\s\S]*)")


class Definition:
    def __init__(self, lines):
        self.terms = []
        self.definitions = []
        for line in lines:
            l = regex_definition.match(line)
            if l:
                self.definitions.append(l.group(1))
            else:
                self.terms.append(line)

    def __str__(self):
        res = "\\begin{center} \n" + \
              "    \\begin{tabularx}{\linewidth}{>{\\raggedleft\\arraybackslash}p{2in}X} \n" + \
              "    \\hline \n"
        for i in range(len(self.terms)):
            res += "        \\textbf{ " + self.terms[i] + " } & " + self.definitions[i] + "\\\\ \n" \
                   "    \\hline \n"
        res += "    \\end{tabularx} \n" + \
               "\end{center}"
        return res
