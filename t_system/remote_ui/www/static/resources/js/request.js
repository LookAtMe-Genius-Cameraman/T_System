// -*- coding: utf-8 -*-

/**
 * @module jquery
 * @fileoverview the top-level module of T_System that contains the jquery request classes and methods to flask of T_System.
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 */


/**
 * Method to handle of POST request of $.ajax query with application/json content type.
 * @param {string} url: the route address of the flask
 * @param {string} type: the HTTP request type like 'POST'
 * @param {string} content_type: the content type of the HTTP request like 'application/x-www-form-urlencoded; charset=UTF-8'
 * @param data: putting data to route.
 * @param {function} callback: the callback function.
 * @return {ajax} Whether something occurred.
 */
function request_asynchronous(url, type, content_type, data, callback) {

    if ($.isFunction(data)) {
        callback = data;
        data = {}
    }

    let ajax = {
        url: url,
        type: type,
        success: callback,
        data: data,
        contentType: content_type
    };


    if (content_type === 'application/json; charset=UTF-8') {
        ajax.data = JSON.stringify(data);
        ajax.dataType = "json";
    }

    return $.ajax(ajax);
}
