// -*- coding: utf-8 -*-

/**
 * @module prismatic_arm_control
 * @fileoverview the top-level module of T_System that contains the communication methods with python flask move API of T_System about the moving the arm by direction axis(x, y or z).
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 */


x_up_btn.setAttribute("data-id", "x");
x_up_btn.setAttribute("data-move-type", "axis");
x_up_btn.setAttribute("data-quantity", 5);

x_down_btn.setAttribute("data-id", "x");
x_down_btn.setAttribute("data-move-type", "axis");
x_down_btn.setAttribute("data-quantity", -5);

y_up_btn.setAttribute("data-id", "y");
y_up_btn.setAttribute("data-move-type", "axis");
y_up_btn.setAttribute("data-quantity", 5);

y_down_btn.setAttribute("data-id", "y");
y_down_btn.setAttribute("data-move-type", "axis");
y_down_btn.setAttribute("data-quantity", -5);

z_up_btn.setAttribute("data-id", "z");
z_up_btn.setAttribute("data-move-type", "axis");
z_up_btn.setAttribute("data-quantity", 5);

z_down_btn.setAttribute("data-id", "z");
z_down_btn.setAttribute("data-move-type", "axis");
z_down_btn.setAttribute("data-quantity", -5);

x_up_i.setAttribute("data-id", "x");
x_up_i.setAttribute("data-move-type", "axis");
x_up_i.setAttribute("data-quantity", 5);

x_down_i.setAttribute("data-id", "x");
x_down_i.setAttribute("data-move-type", "axis");
x_down_i.setAttribute("data-quantity", -5);

y_up_i.setAttribute("data-id", "y");
y_up_i.setAttribute("data-move-type", "axis");
y_up_i.setAttribute("data-quantity", 5);

y_down_i.setAttribute("data-id", "y");
y_down_i.setAttribute("data-move-type", "axis");
y_down_i.setAttribute("data-quantity", -5);

z_up_i.setAttribute("data-id", "z");
z_up_i.setAttribute("data-move-type", "axis");
z_up_i.setAttribute("data-quantity", 5);

z_down_i.setAttribute("data-id", "z");
z_down_i.setAttribute("data-move-type", "axis");
z_down_i.setAttribute("data-quantity", -5);


interact('.prismatic_control_button')
    .on('tap', function (event) {
        let button = event.target;

        let route = "/api/move?id=" + button.getAttribute("data-id") + "&admin_id=" + admin_id;
        let data = {"type": button.getAttribute("data-move-type"), "id": button.getAttribute("data-id"), "quantity": button.getAttribute("data-quantity")};

        jquery_manager.put_data(route, data);
    })
    .on('doubletap', function (event) {
    })
    .on('hold', function (event) {
        let button = event.target;

        let route = "/api/move?id=" + button.getAttribute("data-id") + "&admin_id=" + admin_id;
        let data = {"type": button.getAttribute("data-move-type"), "id": button.getAttribute("data-id"), "quantity": button.getAttribute("data-quantity")};

        interval = setInterval(function () {
            // console.log("gönderdi");
            jquery_manager.put_data(route, data);
        }, 300);

    })
    .on('down', function (event) {
    })
    .on('up', function (event) {
        clearInterval(interval);
    });
