import os
import numpy as np
from sys import getsizeof

DATA_FOLDER_NAME = "data_folder"
INPUT_LABEL_DATA = "input.txt"


def get_data_from_files():
    data_folder = os.path.join(os.curdir, DATA_FOLDER_NAME)
    ensembl_gene_list = []
    M = []
    y = []
    # "y" is the list containing the labels of the matrix of the data
    #label_mapping = }{ # ["Luminal A"] = 0, ["Luminal B"] = 1, etc...
    label_mapping = []  # list: [0] = "Luminal A", [1] = "Luminal B", etc...
    id_label = build_associative_array_caseID_label()   # dictionary: {"TCGA-AAAA": "Luminal A"}
    i = 0
    label_counter = 0
    for filename in os.listdir(data_folder):
        # check if the data we are analyzing is labeled, if not, skip it
        if filename in id_label.keys():
            # check if we already encoutered a certain label: if not, add it to the collection of labels
            if id_label[filename] not in label_mapping:
                #label_mapping[id_label[filename]] = label_counter
                label_mapping.append(id_label[filename])
                label_counter += 1
            # add the label of the i-th element inside the Y list, containing all the labels of each sample
            y.append(label_mapping.index(id_label[filename]))
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
    return M, ensembl_gene_list, y, label_mapping


def build_associative_array_caseID_label():
    label_file = os.path.join(os.curdir, INPUT_LABEL_DATA)
    label_array = {}
    print("Entro nel ciclo")
    i=0
    with open(label_file, "r") as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            else:
                label=line.split("\t")[20]
                if label=="NA":
                    break
                CaseID = line.split("\t")[0]
                label_array[CaseID] = label

    #sort_dictionary(label_array)

    # print("Prova: {}".format(label_array["TCGA-A2-A0EM"]))
    # print(len(label_array))
    return label_array



