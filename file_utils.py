import os
import numpy as np
from sys import getsizeof

DATA_FOLDER_NAME = "data_folder"


def get_data_from_files():
    data_folder = os.path.join(os.curdir, DATA_FOLDER_NAME)
    M = []
    ensembl_gene_list = []
    i = 0
    for filename in os.listdir(data_folder):
        filename = os.path.join(data_folder, filename)
        with open(filename, "r") as fp:
            j = 0
            gene_data = []
            line = fp.readline()
            while line:
                gene_data.append(float(line.split("\t")[1]))
                if i==0:
                    ensembl_gene_list.append(line.split("\t")[0])
                line = fp.readline()
                j += 1
            M.append(np.array(gene_data))
            i += 1



