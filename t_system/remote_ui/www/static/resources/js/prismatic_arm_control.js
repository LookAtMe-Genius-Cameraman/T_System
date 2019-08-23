// -*- coding: utf-8 -*-

/**
 * @module prismatic_arm_control
 * @fileoverview the top-level module of T_System that contains the communication methods with python flask move API of T_System about the moving the arm by direction axis(x, y or z).
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 */


x_up_btn.addEventListener("mousedown", function () {

    let route = "/api/move?id=x&admin_id=" + admin_id;
    let data = {"type": "axis", "id": "x", "quantity": "10"};

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.put_data(route, data);
    }, 300);
});


x_down_btn.addEventListener("mousedown", function () {

    let route = "/api/move?id=x&admin_id=" + admin_id;
    let data = {"type": "axis", "id": "x", "quantity": "-10"};

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.put_data(route, data);
    }, 300);
});


y_up_btn.addEventListener("mousedown", function () {

    let route = "/api/move?id=y&admin_id=" + admin_id;
    let data = {"type": "axis", "id": "y", "quantity": "10"};

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.put_data(route, data);
    }, 300);
});


y_down_btn.addEventListener("mousedown", function () {

    let route = "/api/move?id=y&admin_id=" + admin_id;
    let data = {"type": "axis", "id": "y", "quantity": "-10"};

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.put_data(route, data);
    }, 300);
});


z_up_btn.addEventListener("mousedown", function () {

    let route = "/api/move?id=z&admin_id=" + admin_id;
    let data = {"type": "axis", "id": "z", "quantity": "10"};

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.put_data(route, data);
    }, 300);
});


z_down_btn.addEventListener("mousedown", function () {

    let route = "/api/move?id=z&admin_id=" + admin_id;
    let data = {"type": "axis", "id": "z", "quantity": "-10"};

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.put_data(route, data);
    }, 300);
});


let elements_prismatic = [x_up_btn, x_down_btn, y_up_btn, y_down_btn, z_up_btn, z_down_btn];


add_listener_to_elements(elements_prismatic, "mouseup", function () {
    clearInterval(interval);
});


function add_listener_to_elements(elements, type, func) {

    for(let i = 0; i<elements.length ;i++){
        elements[i].addEventListener(type, func)
    }
}
