#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: job
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for managing the T_System's work with specified scenarios and parameters.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.job import JobManager
from t_system.remote_ui.api.data_schema import JOB_SCHEMA

api_bp = Blueprint('job_api', __name__)
api = Api(api_bp)

job_manager = JobManager()


class JobApi(Resource):
    """Class to define an API of the positions of the arm.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.job.JobApi.get` INVALID,
         :func:`t_system.remote_ui.api.job.JobApi.post` for setting seer's work parameters,
         :func:`t_system.remote_uia.api.job.JobApi.put` for starting work of seer,
         :func:`t_system.remote_uia.api.job.JobApi.patch` for resuming paused work of seer,
         :func:`t_system.remote_ui.api.job.JobApi.delete` for stopping or pausing work of seer.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.job.JobApi` class.
        """

    def get(self):
        """The API method to GET request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}

    def post(self):
        """The API method to POST request for flask.
        """
        admin_id = request.args.get('admin_id', None)

        try:
            form = request.form.to_dict(flat=True)
            data = JOB_SCHEMA.validate(form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}
        result = job_manager.set_seer(admin_id, data)

        return {'status': 'OK' if result else 'ERROR'}

    def put(self):
        """The API method to PUT request for flask.
        """
        running_type = request.args.get('type')
        admin_id = request.args.get('admin_id', None)

        if not running_type:
            return {'status': 'ERROR', 'message': '\'type\' parameter is missing'}

        result = job_manager.start_job(admin_id, running_type)
        return {'status': 'OK' if result else 'ERROR'}

    def patch(self):
        """The API method to PATCH request for flask.
        """
        admin_id = request.args.get('admin_id', None)

        result = job_manager.resume_job(admin_id)
        return {'status': 'OK' if result else 'ERROR'}

    def delete(self):
        """The API method to DELETE request for flask.
        """
        pause = request.args.get('pause', None)
        admin_id = request.args.get('admin_id', None)

        if pause:
            result = job_manager.pause_job(admin_id)
        else:
            result = job_manager.stop_job(admin_id)

        return {'status': 'OK' if result else 'ERROR'}


api.add_resource(JobApi, '/api/job')
