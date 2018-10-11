import requests
import json
import re
import os
import gzip
import shutil
import tarfile

DATA_FOLDER_NAME = "data_folder"


def retrieve_data():
    print("Retrieving data from server: gdc.cancer.gov")
    get_files_from_uuid_list(get_uuid_list())


def get_uuid_list():
    files_endpt = "https://api.gdc.cancer.gov/files"

    filters = {
        "op": "and",
        "content": [
            {
                "op": "in",
                "content": {
                    "field": "cases.project.primary_site",
                    "value": ["Breast"]
                }
            },
            # {
            #     "op": "in",
            #     "content": {
            #         "field": "cases.project.program.name",
            #         "value": ["TCGA"]
            #     }
            # },
            {
                "op": "in",
                "content": {
                    "field": "cases.project.project_id",
                    "value": ["TCGA-BRCA"]
                }
            },
            {
                "op": "in",
                "content": {
                    "field": "files.analysis.workflow_type",
                    "value": ["HTSeq - FPKM-UQ"]
                }
            },
            {
                "op": "in",
                "content": {
                    "field": "cases.demographic.gender",
                    "value": ["male"]
                }
            }
        ]
    }

    # Here a GET is used, so the filter parameters should be passed as a JSON string.
    params = {
        "filters": json.dumps(filters),
        "fields": "file_id",
        "format": "JSON",
        "size": "2000"  # arbitrary value
    }
    response = requests.get(files_endpt, params=params)

    # This step populates the download list with the file_ids from the previous query
    file_uuid_list = []
    for file_entry in json.loads(response.content.decode("utf-8"))["data"]["hits"]:
        file_uuid_list.append(file_entry["file_id"])

    return file_uuid_list


def get_files_from_uuid_list(uuid_list):
    data_endpt = "https://api.gdc.cancer.gov/data"
    params = {"ids": uuid_list}
    response = requests.post(data_endpt, data=json.dumps(params), headers={"Content-Type": "application/json"})
    response_head_cd = response.headers["Content-Disposition"]
    file_name = re.findall("filename=(.+)", response_head_cd)[0]

    # create the first part of the path, starting from the current dir
    data_folder = os.path.join(os.curdir, DATA_FOLDER_NAME)
    file_name = os.path.join(data_folder, file_name)
    # create dir: if already existing, exist_ok=true suppresses any errors
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "wb") as output_file:
        output_file.write(response.content)
        print("Filename: {}".format(file_name))

    extract_tar_gz(file_name, data_folder)


def extract_tar_gz(archive_name, data_folder):
    with tarfile.open(archive_name, "r") as ap:
        # ap is the archive pointer. For each directory encountered extract it and analyze it
        for element in ap.getmembers():
            if element.name != "MANIFEST.txt":
                # extract dir
                ap.extract(element.name, data_folder)
                file_gz_path = os.path.join(data_folder, os.path.join(element.name.split("/")[0], element.name.split("/")[1]))
                # open and extract the last archive, that contains only the txt file we're interested in
                file_txt_path = os.path.join(data_folder, os.path.basename(file_gz_path)).split(".gz")[0]
                try:
                    # extact the .gz file using the gzip library, opening two fp and copying the content of the 1st into the 2nd
                    with gzip.open(file_gz_path, 'rb') as f_in, open(file_txt_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                except Exception as e:
                    print("Generated exception: {}".format(type(e).__name__))
                # remove the folder that has just been extracted, because now it's useless
                shutil.rmtree(os.path.dirname(file_gz_path))

    # after having extracted the .tar.gz file, remove it
    os.remove(archive_name)


def check_local_files():
    print("Performing check...")
    data_folder = os.path.join(os.curdir, DATA_FOLDER_NAME)
    # check if the data directory exists
    if not os.path.isdir(data_folder) or not os.path.exists(data_folder):
        print("No samples have been found! Downloading them now...\n")
        retrieve_data()
    else:
        n_uuid_files_local = len(os.listdir(data_folder))
        n_uuid_files_online = len(get_uuid_list())
        if n_uuid_files_local != n_uuid_files_online:
            print("The local collection might not be up to date...\n{}/{} samples available".format(n_uuid_files_local, n_uuid_files_online))
        else:
            print("There are {} samples available locally.".format(n_uuid_files_local))
    print("Check completed.")

