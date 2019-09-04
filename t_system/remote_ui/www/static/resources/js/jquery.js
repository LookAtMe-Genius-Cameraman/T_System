// -*- coding: utf-8 -*-

/**
 * @module jquery
 * @fileoverview the top-level module of T_System that contains the jquery request classes and methods to flask of T_System.
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 */


/**
 * Method to handle of PUT request of $.ajax query.
 * @param {string} url: the route address of the flask
 * @param data: posting data to route.
 * @param {function} callback: the callback function.
 * @return {ajax} Whether something occurred.
 */
$.put = function (url, data, callback) {

    if ($.isFunction(data)) {
        callback = data;
        data = {}
    }

    return $.ajax({
        url: url,
        type: 'PUT',
        success: callback,
        data: data,
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8'  // Default one.
    });
};

/**
 * Method to handle of PATCH request of $.ajax query.
 * @param {string} url: the route address of the flask
 * @param data: posting data to route.
 * @param {function} callback: the callback function.
 * @return {ajax} Whether something occurred.
 */
$.patch = function (url, data, callback) {

    if ($.isFunction(data)) {
        callback = data;
        data = {}
    }

    return $.ajax({
        url: url,
        type: 'PATCH',
        success: callback,
        data: data,
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8'  // Default one.
    });
};


/**
 * Method to handle of DELETE request of $.ajax query.
 * @param {string} url: the route address of the flask
 * @param data: posting data to route.
 * @param {function} callback: the callback function.
 * @return {ajax} Whether something occurred.
 */
$.delete = function (url, data, callback) {

    if ($.isFunction(data)) {
        callback = data;
        data = {}
    }

    return $.ajax({
        url: url,
        type: 'DELETE',
        success: callback,
        data: data,
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8'

    });
};


/**
 * Class to define a AJAX JQuery communication method manager object.
 */
class JQueryManager {

    constructor() {
    }

    /**
     * Method to sending data that is given with data parameter to the route.
     * @param {string} route: the route address of the flask
     * @param {dict} data: posting data to route.
     * @return {string} Whether something occurred.
     */
    static post_data(route, data) {

        let success = "";
        // console.log(data);
        $.post(route, data, function (req, err, resp) {
            response_data = JSON.parse(resp.responseText);
            // console.log(response_datavfdv);

            success = err
        });
        // stop link reloading the page
        // event.preventDefault();

        return success
    }

    /**
     * Method to getting data from given route as response.
     * The getting dictionary data from python flask assigns to `requested_data` variable.
     * @param {string} route: the route address of the flask
     */
    static get_data(route) {
        let success = "";

        $.get(route, function (data, err) {
            success = err;

            if (success === "success") {
                requested_data = data;
            }
        });
    }

    /**
     * Method to send PUT request to given route.
     * The response of request assigns to `response_data` variable.
     * @param {string} route: the route address of the flask
     * @param data: putting data to route.
     * @return {string} Whether something occurred.
     */
    static put_data(route, data) {
        let success = "";
        $.put(route, data, function (req, err, resp) {
            response_data = JSON.parse(resp.responseText);
            success = err
        });
        // stop link reloading the page
        // event.preventDefault();

        return success
    }

    /**
     * Method to send PATCH request to given route.
     * The response of request assigns to `response_data` variable.
     * @param {string} route: the route address of the flask
     * @param data: putting data to route.
     * @return {string} Whether something occurred.
     */
    static patch_data(route, data) {
        let success = "";
        $.put(route, data, function (req, err, resp) {
            response_data = JSON.parse(resp.responseText);
            success = err
        });
        // stop link reloading the page
        // event.preventDefault();

        return success
    }

    /**
     * Method to send DELETE request to given route.
     * The response of request assigns to `response_data` variable.
     * @param {string} route: the route address of the flask
     */
    static delete_data(route) {
        let success = "";

        $.delete(route, function (req, err, resp) {

            success = err;
            if (success === "success") {
                response_data = JSON.parse(resp.responseText);
                success = err
            }
        });
    }
}
