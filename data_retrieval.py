import requests
import json
import re
import time


def retrieve_data():
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
            }
        ]
    }

    # Here a GET is used, so the filter parameters should be passed as a JSON string.

    params = {
        "filters": json.dumps(filters),
        "fields": "file_id",
        "format": "JSON",
        "size": "2000"
    }

    response = requests.get(files_endpt, params=params)

    file_uuid_list = []

    i = 1
    # This step populates the download list with the file_ids from the previous query
    for file_entry in json.loads(response.content.decode("utf-8"))["data"]["hits"]:
        print("{}:".format(i), end=" ")
        file_uuid_list.append(file_entry["file_id"])
        print("{}".format(file_entry["file_id"]))
        i += 1

    data_endpt = "https://api.gdc.cancer.gov/data"

    params = {"ids": file_uuid_list}

    response = requests.post(data_endpt, data=json.dumps(params), headers={"Content-Type": "application/json"})

    response_head_cd = response.headers["Content-Disposition"]

    file_name = re.findall("filename=(.+)", response_head_cd)[0]

    with open(file_name, "wb") as output_file:
        output_file.write(response.content)
        print("Filename: {}".format(file_name))
        time.sleep(5)


def test_esempio():
    import requests
    import json
    import re

    files_endpt = "https://api.gdc.cancer.gov/files"

    filters = {
        "op": "and",
        "content": [
            {
                "op": "in",
                "content": {
                    "field": "cases.project.primary_site",
                    "value": ["Lung"]
                }
            },
            {
                "op": "in",
                "content": {
                    "field": "cases.demographic.race",
                    "value": ["white"]
                }
            },
            {
                "op": "in",
                "content": {
                    "field": "cases.demographic.gender",
                    "value": ["female"]
                }
            },
            {
                "op": "in",
                "content": {
                    "field": "files.analysis.workflow_type",
                    "value": ["HTSeq - FPKM"]
                }
            }
        ]
    }

    # Here a GET is used, so the filter parameters should be passed as a JSON string.

    params = {
        "filters": json.dumps(filters),
        "fields": "file_id",
        "format": "JSON",
        "size": "1000"
    }

    response = requests.get(files_endpt, params=params)

    file_uuid_list = []

    # This step populates the download list with the file_ids from the previous query
    for file_entry in json.loads(response.content.decode("utf-8"))["data"]["hits"]:
        file_uuid_list.append(file_entry["file_id"])

    data_endpt = "https://api.gdc.cancer.gov/data"

    params = {"ids": file_uuid_list}

    response = requests.post(data_endpt, data=json.dumps(params), headers={"Content-Type": "application/json"})

    response_head_cd = response.headers["Content-Disposition"]

    file_name = re.findall("filename=(.+)", response_head_cd)[0]

    with open(file_name, "wb") as output_file:
        output_file.write(response.content)

def show_file():
    return
