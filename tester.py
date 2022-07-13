import os
import sys

comd_1 = "python3 main.py {in_file_1} {in_file_2} {out_file}".format(in_file_1 = str(sys.argv[1]), in_file_2 = str(sys.argv[2]), out_file = str(sys.argv[3]))

os.system(comd_1)