import sys

file = open("{}/testfile.txt".format(sys.argv[1]))
file.write("Hello\n")
file.close()
