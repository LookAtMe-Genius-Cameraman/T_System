// -*- coding: utf-8 -*-

/**
 * @module rotational_arm_control
 * @fileoverview the top-level module of T_System that contains the communication methods with python flask move API of T_System about the moving the arm joint by joint.
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 */


joint_1_cw_btn.addEventListener("mousedown", function () {

    let route = "/api/move?id=1&admin_id=" + admin_id;
    let data = {"type": "joint", "id": "1", "quantity": 5};

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.put_data(route, data);
    }, 300);
});


joint_1_ccw_btn.addEventListener("mousedown", function () {

    let route = "/api/move?id=1&admin_id=" + admin_id;
    let data = {"type": "joint", "id": "1", "quantity": -5};

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.put_data(route, data);
    }, 300);
});


joint_2_cw_btn.addEventListener("mousedown", function () {

    let route = "/api/move?id=2&admin_id=" + admin_id;
    let data = {"type": "joint", "id": "2", "quantity": 5};

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.put_data(route, data);
    }, 300);
});


joint_2_ccw_btn.addEventListener("mousedown", function () {

    let route = "/api/move?id=2&admin_id=" + admin_id;
    let data = {"type": "joint", "id": "2", "quantity": -5};

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.put_data(route, data);
    }, 300);
});


joint_3_cw_btn.addEventListener("mousedown", function () {

    let route = "/api/move?id=3&admin_id=" + admin_id;
    let data = {"type": "joint", "id": "3", "quantity": 5};

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.put_data(route, data);
    }, 300);
});


joint_3_ccw_btn.addEventListener("mousedown", function () {

    let route = "/api/move?id=3&admin_id=" + admin_id;
    let data = {"type": "joint", "id": "3", "quantity": -5};

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.put_data(route, data);
    }, 300);
});


let elements_rotational = [joint_1_cw_btn, joint_1_ccw_btn, joint_2_cw_btn, joint_2_ccw_btn, joint_3_cw_btn, joint_3_ccw_btn];


add_listener_to_elements(elements_rotational, "mouseup", function () {
    clearInterval(interval);
});


function add_listener_to_elements(elements, type, func) {

    for(let i = 0; i<elements.length ;i++){
        elements[i].addEventListener(type, func)
    }
}
