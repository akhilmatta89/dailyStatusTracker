import os.path

import logging_lib

from flask import Flask, jsonify, request

import constants
import db_operations.init
import exceptions.exceptions
from db_operations import init, create_data, get_data, delete, update
from logging_lib.logging_lib import Logger

app = Flask(__name__)
Logger = Logger().get_logger()

@app.route("/init", methods=['POST'])
def initialize():
    try:
        Logger.info("Initialization triggered")
        if not os.path.exists(db_operations.constants.DB_PATH.split("/")[1]):
            os.mkdir(db_operations.constants.DB_PATH.split("/")[1])
        initObj = db_operations.init.Init()
        initObj.check_initialization_status()
        initObj.intialize_db()
        data = {"message": "Initialization Success", "status": "success"}
        return jsonify(data), constants.STATUS_CODE_201
    except FileExistsError:
        return jsonify({"error": "Init already performed"}), constants.STATUS_CODE_CONFLICT
    except Exception as ex:
        return jsonify({"error": "Database initialization failed"}), constants.STATUS_CODE_INTERNAL_ERROR


@app.route("/add-status", methods=["POST"])
def add_status():
    req_data = request.get_json()
    try:
        create_obj = db_operations.create_data.Create()
        create_obj.verify_req_body(req_data)
        create_obj.add_status_into_db(req_data)
        return jsonify({"message": "Successfully created entry into server"}), constants.STATUS_CODE_SUCCESS
    except exceptions.exceptions.InvalidRequestBody as irb:
        return jsonify({"error": f"{irb.message}"})
    except Exception as ex:
        return jsonify({"error": "Creation failed"}), constants.STATUS_CODE_INTERNAL_ERROR


@app.route("/get-all-status", methods=["Get"])
def get_all_status():
    try:
        get_obj = get_data.GetData()
        data = get_obj.get_all_data()
        return jsonify(data), constants.STATUS_CODE_SUCCESS
    except Exception as ex:
        return jsonify({"error": "Creation failed"}), constants.STATUS_CODE_INTERNAL_ERROR


@app.route("/get-status/<string:date>", methods=['GET'])
def get_status(date):
    try:
        get_obj = get_data.GetData()
        data = get_obj.get_data(date)
        return jsonify(data), constants.STATUS_CODE_SUCCESS
    except exceptions.exceptions.InvalidKey as ik:
        return jsonify({"error": ik.get_error_message()})
    except Exception as ex:
        return jsonify({"error": "Retrieve failed"}), constants.STATUS_CODE_INTERNAL_ERROR

@app.route("/delete-status/<string:date>", methods=['DELETE'])
def delete_status(date):
    try:
        del_obj = delete.DeleteData()
        del_obj.delete_data(date)
        return jsonify({"message": "Deletion Success"}), constants.STATUS_CODE_SUCCESS
    except exceptions.exceptions.InvalidKey as ik:
        return jsonify({"error": ik.get_error_message()})
    except Exception as ex:
        return jsonify({"error": "Deletion failed"}), constants.STATUS_CODE_INTERNAL_ERROR

@app.route("/update-status/<string:date>", methods=['PATCH'])
def update_status(date):
    data = request.get_json()

    # If no data is provided, return an error
    if not data:
        return jsonify({"error": "No data provided for update"}), constants.STATUS_CODE_BAD_REQUEST

    upd_obj = update.UpdateData()
    return upd_obj.update_status_based_on_date(date, data)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
