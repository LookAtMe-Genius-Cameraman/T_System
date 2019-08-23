#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: scenario
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for T_System's arm motion scenarios.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.scenario import create_scenario, get_scenario, get_scenarios, update_scenario, delete_scenario
from t_system.remote_ui.api.data_schema import SCENARIO_SCHEMA

api_bp = Blueprint('scenario_api', __name__)
api = Api(api_bp)


class ScenarioApi(Resource):
    """Class to define an API of the scenarios of the arm.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.scenario.ScenarioApi.get`for the provide get scenario data from database,
         :func:`t_system.remote_ui.api.scenario.ScenarioApi.post` for provide creating new scenario,
         :func:`t_system.remote_ui.api.scenario.ScenarioApi.put` for provide updating the scenario,
         :func:`t_system.remote_ui.api.scenario.ScenarioApi.delete` for provide deleting the scenario
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.scenario.ScenarioApi` class.
        """

    def get(self):
        """The API method to get request for flask.
        """

        scenario_id = request.args.get('id', None)
        admin_id = request.args.get('admin_id', None)

        if scenario_id:
            scenario = get_scenario(admin_id, scenario_id)
            return {'status': 'OK', 'data': scenario}

        scenarios = get_scenarios(admin_id)

        return {'status': 'OK', 'data': scenarios}

    def post(self):
        """The API method to post request for flask.
        """
        admin_id = request.args.get('admin_id', None)

        try:
            form = request.form.to_dict(flat=True)
            data = SCENARIO_SCHEMA.validate(form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}
        result, scenario_id = create_scenario(admin_id, data)

        return {'status': 'OK' if result else 'ERROR', 'id': scenario_id}

    def put(self):
        """The API method to put request for flask.
        """
        scenario_id = request.args.get('id')
        admin_id = request.args.get('admin_id', None)

        if not scenario_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}
        try:
            form = request.form.to_dict(flat=True)
            data = SCENARIO_SCHEMA.validate(form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        result = update_scenario(admin_id, scenario_id, data)
        return {'status': 'OK' if result else 'ERROR'}

    def delete(self):
        """The API method to delete request for flask.
        """
        scenario_id = request.args.get('id')
        admin_id = request.args.get('admin_id', None)

        if not scenario_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        result = delete_scenario(admin_id, scenario_id)

        return {'status': 'OK' if result else 'ERROR'}


api.add_resource(ScenarioApi, '/api/scenario')
