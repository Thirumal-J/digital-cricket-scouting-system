import json
from flask import jsonify

response = {"statusCode": "-1", "statusMsg": "",
            "statusDesc": "Recheck return json status method call", "statusType": "", "data": ""}


def createJSONResponse(status="default", status_who="NoWho", data="No Data To Display"):
    with open('process_status.JSON') as f:
        data_json = json.load(f)

    dict_status = data_json[status.lower()]
    if status != "default" and status_who != "NoWho":
        response["statusCode"] = dict_status["status"][status_who.lower()]["status_code"]
        response["statusDesc"] = dict_status["status"][status_who]["status_desc"]
    response["statusMsg"] = dict_status["status_message"]
    response["statusType"] = dict_status["status_type"]
    response["data"] = data
    return jsonify(response)
