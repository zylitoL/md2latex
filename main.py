def main():
    try:
        fr = open(r"C:\Users\Jacob\PycharmProjects\untitled\md.txt", 'r')
        try:
            fw = open(r"C:\Users\Jacob\PycharmProjects\untitled\latex.txt", 'w')

            #############################

            for line in fr:
                line = line_latex(line)
                fw.write(line)
        finally:
            fw.close()
    finally:
        fr.close()
