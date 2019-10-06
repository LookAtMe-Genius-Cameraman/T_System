// -*- coding: utf-8 -*-

/**
 * @module controlling_modal
 * @fileoverview the top-level module of T_System that contains controlling methods of data that is coming from T_System.
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 * @version 0.0.1
 */


/** @type {!Element} */
const main_container = document.getElementById("main_container");
const controlling_template_sidebar = document.getElementById("controlling_template_sidebar");
const position_list_ul = document.getElementById("position_list_ul");
const scenario_list_ul = document.getElementById("scenario_list_ul");

const controlling_template_content = document.getElementById("controlling_template_content");
const sidebar_toggle_btn = document.getElementById("sidebar_toggle_btn");
const controlling_template_sidebar_close_btn = document.getElementById("controlling_template_sidebar_close_btn");

const dark_deep_background_div = document.getElementById("dark_deep_background_div");

/** @type {!Element} */
const video_area_div = document.getElementById("video_area_div");
const get_preview_span = document.getElementById("get_preview_span");
const stream_area_img = document.getElementById("stream_area_img");

/** @type {!Element} */
const motion_control_div = document.getElementById("motion_control_div");
const prismatic_menu_control_input = document.getElementById("prismatic_menu_control_input");
const prismatic_menu_control_label = document.getElementById("prismatic_menu_control_label");

const rotational_control_nav = document.getElementById("rotational_control_nav");
const rotational_ccw_control_nav = document.getElementById("rotational_ccw_control_nav");

const rotational_menu_control_input = document.getElementById("rotational_menu_control_input");
const rotational_menu_control_label = document.getElementById("rotational_menu_control_label");

const rotational_ccw_menu_control_input = document.getElementById("rotational_ccw_menu_control_input");
const rotational_ccw_menu_control_label = document.getElementById("rotational_ccw_menu_control_label");

/** @type {!Element} */
const rotational_control_div = document.getElementById("rotational_control_div");

/** @type {!Element} */
const prismatic_control_div = document.getElementById("prismatic_control_div");
const x_up_btn = document.getElementById("x_up_btn");
const y_up_btn = document.getElementById("y_up_btn");
const z_up_btn = document.getElementById("z_up_btn");
const x_down_btn = document.getElementById("x_down_btn");
const y_down_btn = document.getElementById("y_down_btn");
const z_down_btn = document.getElementById("z_down_btn");

const x_up_i = document.getElementById("x_up_i");
const y_up_i = document.getElementById("y_up_i");
const z_up_i = document.getElementById("z_up_i");
const x_down_i = document.getElementById("x_down_i");
const y_down_i = document.getElementById("y_down_i");
const z_down_i = document.getElementById("z_down_i");

const record_pos_sce_btn = document.getElementById("record_pos_sce_btn");
const record_pos_sce_div = document.getElementById("record_pos_sce_div");

const pos_sce_select_div = document.getElementById("pos_sce_select_div");
const record_as_pos_btn = document.getElementById("record_as_pos_btn");
const record_in_sce_btn = document.getElementById("record_in_sce_btn");

const record_as_position_div = document.getElementById("record_as_position_div");
const position_div_back_btn = document.getElementById("position_div_back_btn");
const position_name_input = document.getElementById("position_name_input");
const create_pos_btn = document.getElementById("create_pos_btn");

const record_in_scenario_div = document.getElementById("record_in_scenario_div");
const scenario_div_back_btn = document.getElementById("scenario_div_back_btn");
const scenario_name_input = document.getElementById("scenario_name_input");
const create_sce_btn = document.getElementById("create_sce_btn");
const record_in_scenario_list_ul = document.getElementById("record_in_scenario_list_ul");

sidebar_toggle_btn.addEventListener("click", function () {

    while (position_list_ul.firstChild) {
        position_list_ul.removeChild(position_list_ul.firstChild);
    }

    while (scenario_list_ul.firstChild) {
        scenario_list_ul.removeChild(scenario_list_ul.firstChild);
    }

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    controlling_template_sidebar.classList.toggle("active");
    hide_element(controlling_template_content);

    let positions = [];
    let scenarios = [];


    request_asynchronous('/api/position?db=' + action_db_name + '&admin_id=' + admin_id, 'GET',
        'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
            // err = "success"
            // requested_data = {"status": "OK", "data": [{"id": "j470138f-agcb-11e9-b130-ce4f744661fd", "name": "position_name", "cartesian_coords": [30, 25, 42], "polar_coords": [1.5, 1.02, 0.5]}]};

            if (err === "success") {
                if (requested_data["status"] === "OK") {

                    positions = requested_data["data"];
                    // console.log(positions);

                    for (let c = 0; c < positions.length; c++) {

                        let position_div = document.createElement('div');
                        let position_span = document.createElement('span');

                        position_div.classList.add("draggable_position", "drag-drop", "ml-1", "mr-1", "position_div");
                        position_div.setAttribute("data-position-name", positions[c]["name"]);
                        position_div.setAttribute("data-cartesian-coords", positions[c]["cartesian_coords"]);
                        position_div.setAttribute("data-polar-coords", positions[c]["polar_coords"]);

                        position_span.classList.add("shine_in_dark");
                        position_span.innerHTML = positions[c]["name"];

                        position_span.addEventListener("click", function () {

                            position_div.removeChild(position_span);

                            let position_input = document.createElement('input');

                            position_input.type = "text";
                            position_input.placeholder = position_span.innerHTML;
                            position_input.classList.add("action_name_input");

                            position_input.addEventListener("focusout", function () {
                                if (position_input.value !== position_span.innerHTML && position_input.value !== "") {
                                    let data = {"name": position_input.value, "cartesian_coords": positions[c]["cartesian_coords"], "polar_coords": positions[c]["polar_coords"]};

                                    request_asynchronous('/api/position?db=' + action_db_name + '&id=' + positions[c]["id"] + '&admin_id=' + admin_id, 'PUT',
                                        'application/json; charset=UTF-8', data, function (req, err, response) {
                                            if (err === "success") {
                                                let response_data = JSON.parse(response.responseText);
                                            }
                                        });

                                    position_span.innerHTML = position_input.value
                                }

                                position_div.removeChild(position_input);
                                position_div.appendChild(position_span);

                            });
                            position_div.appendChild(position_input);
                        });

                        position_div.appendChild(position_span);
                        position_list_ul.appendChild(position_div);
                    }

                }
            }
        });

    request_asynchronous('/api/scenario?db=' + action_db_name + '&admin_id=' + admin_id, 'GET',
        'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
            // err = "success"
            // requested_data = {"status": "OK", "data": [{"id": "b97tr40a-alcb-31w9-b150-ce2f6156l1ed", "name": "scenario_name1", "positions": [{"name": "pos1"}, {"name": "pos2"}]}, {"id": "b97dr48a-aecb-11e9-b130-cc2f7156l1ed", "name": "scenario_name2", "positions": [{}, {}]}]};

            if (err === "success") {
                if (requested_data["status"] === "OK") {

                    scenarios = requested_data["data"];
                    // console.log(scenarios);

                    for (let c = 0; c < scenarios.length; c++) {

                        let scenario_dropdown_div = document.createElement('div');
                        let scenario_btn = document.createElement('button');
                        let scenario_dd_btn = document.createElement('button');
                        let scenario_dd_span = document.createElement('span');
                        let scenario_dropdown_container_div = document.createElement('div');

                        scenario_dropdown_div.classList.add("dropdown", "mt-1", "ml-1", "mr-1", "scenario_name_btn");
                        scenario_dropdown_div.id = scenarios[c]["id"] + "_dropdown_div";

                        scenario_btn.classList.add("btn", "btn-dark");
                        scenario_btn.type = "button";
                        scenario_btn.id = scenarios[c]["id"] + "_btn";
                        scenario_btn.innerHTML = scenarios[c]["name"];

                        scenario_btn.addEventListener("click", function () {

                            scenario_dropdown_div.removeChild(scenario_btn);
                            scenario_dropdown_div.removeChild(scenario_dd_btn);
                            scenario_dropdown_div.removeChild(scenario_dropdown_container_div);


                            let scenario_input = document.createElement('input');

                            scenario_input.type = "text";
                            scenario_input.placeholder = scenario_btn.innerHTML;
                            scenario_input.classList.add("action_name_input");

                            scenario_input.addEventListener("focusout", function () {
                                if (scenario_input.value !== scenario_btn.innerHTML && scenario_input.value !== "") {
                                    let data = {"name": scenario_input.value, "positions": scenarios[c]["positions"]};

                                    request_asynchronous('/api/scenario?db=' + action_db_name + '&id=' + scenarios[c]["id"] + '&admin_id=' + admin_id, 'PUT',
                                        'application/json; charset=UTF-8', data, function (req, err, response) {
                                            if (err === "success") {
                                                let response_data = JSON.parse(response.responseText);
                                            }
                                        });
                                    scenario_btn.innerHTML = scenario_input.value
                                }

                                scenario_dropdown_div.removeChild(scenario_input);

                                scenario_dropdown_div.appendChild(scenario_btn);
                                scenario_dropdown_div.appendChild(scenario_dd_btn);
                                scenario_dropdown_div.appendChild(scenario_dropdown_container_div);

                            });
                            scenario_dropdown_div.appendChild(scenario_input);
                        });

                        interact('#' + scenario_btn.id).dropzone({
                            // only accept elements matching this CSS selector
                            accept: '.draggable_position',
                            // Require a 75% element overlap for a drop to be possible
                            overlap: 0.75,

                            // listen for drop related events:

                            ondropactivate: function (event) {
                            },
                            ondragenter: function (event) {
                                scenario_dd_btn.click();
                                event.target.classList.add('actions-drop-target');

                            },
                            ondragleave: function (event) {
                                event.target.classList.remove('actions-drop-target');

                            },
                            ondrop: function (event) {
                            },

                            ondropdeactivate: function (event) {
                                // scenario_dd_btn.click()
                            }
                        });

                        scenario_dd_btn.classList.add("btn", "btn-dark", "dropdown-toggle", "dropdown-toggle-split");
                        scenario_dd_btn.type = "button";
                        scenario_dd_btn.setAttribute("data-toggle", "dropdown");
                        scenario_dd_btn.setAttribute("aria-haspopup", "true");
                        scenario_dd_btn.setAttribute("aria-expanded", "false");
                        // scenario_dd_btn.innerHTML = "";

                        scenario_dd_span.classList.add("sr-only");

                        scenario_dropdown_container_div.classList.add("dropdown-menu", "dropdown-menu-right", "dropdown_menu", "scenario_dropdown_menu");
                        scenario_dropdown_container_div.id = scenarios[c]["id"] + "_container_div";
                        // scenario_dropdown_container_div.setAttribute("aria-labelledby", date_btn.id);
                        let drop_timeout;
                        interact('#' + scenario_dropdown_container_div.id).dropzone({
                            // only accept elements matching this CSS selector
                            accept: '.draggable_position',
                            // Require a 75% element overlap for a drop to be possible
                            overlap: 0.01,

                            // listen for drop related events:

                            ondropactivate: function (event) {
                                // add active dropzone feedback
                                event.target.classList.add('actions-drop-active');
                            },
                            ondragenter: function (event) {
                                let draggableElement = event.relatedTarget;
                                let dropzoneElement = event.target;

                                // feedback the possibility of a drop
                                dropzoneElement.classList.add('actions-drop-target');
                                draggableElement.classList.add('action-can-drop');

                                drop_timeout = setTimeout(function () {

                                    let position = event.relatedTarget;
                                    let position_info = {"name": position.getAttribute("data-position-name"), "cartesian_coords": position.getAttribute("data-cartesian-coords"), "polar_coords": position.getAttribute("data-polar-coords")};

                                    let existing_positions = scenarios[c]["positions"];
                                    existing_positions.push(position_info);

                                    let data = {"name": scenario_btn.innerHTML, "positions": existing_positions};

                                    request_asynchronous('/api/scenario?db=' + action_db_name + '&id=' + scenarios[c]["id"] + '&admin_id=' + admin_id, 'PUT',
                                        'application/json; charset=UTF-8', data, function (req, err, response) {
                                            if (err === "success") {

                                                let response_data = JSON.parse(response.responseText);

                                                if (response_data["status"] === "OK") {
                                                    controlling_template_sidebar_close_btn.click();
                                                    sidebar_toggle_btn.click();
                                                    scenario_dd_btn.click();
                                                }
                                            }
                                        });
                                }, 1000);
                            },
                            ondragleave: function (event) {
                                // remove the drop feedback style
                                event.target.classList.remove('actions-drop-target');
                                event.relatedTarget.classList.remove('action-can-drop');
                                clearTimeout(drop_timeout);
                            },
                            ondrop: function (event) {
                                // event.preventDefault();
                                event.relatedTarget.textContent = 'Dropped';
                            },

                            ondropdeactivate: function (event) {
                                // remove active dropzone feedback
                                event.target.classList.remove('actions-drop-active');
                                event.target.classList.remove('actions-drop-target');

                            }
                        });

                        for (let i = 0; i < scenarios[c]["positions"].length; i++) {
                            let position_div = document.createElement('div');
                            let position_span = document.createElement('span');

                            position_div.classList.add("dropdown-item", "draggable_position", "drag-drop", "position_of_scenario");

                            position_span.classList.add("cut-text");
                            position_span.innerHTML = scenarios[c]["positions"][i]["name"];

                            position_div.appendChild(position_span);
                            scenario_dropdown_container_div.appendChild(position_div);
                        }

                        scenario_dd_btn.appendChild(scenario_dd_span);

                        scenario_dropdown_div.appendChild(scenario_btn);
                        scenario_dropdown_div.appendChild(scenario_dd_btn);
                        scenario_dropdown_div.appendChild(scenario_dropdown_container_div);

                        scenario_list_ul.appendChild(scenario_dropdown_div);
                    }
                }

            }
        });
});

controlling_template_sidebar_close_btn.addEventListener("click", function () {
    controlling_template_sidebar.classList.toggle("active");
    dark_deep_background_div.classList.toggle("focused");
    show_element(controlling_template_content)
});

let position_drop_timeout;
interact('#position_list_ul').dropzone({
    // only accept elements matching this CSS selector
    accept: '.draggable_position',
    // Require a 75% element overlap for a drop to be possible
    overlap: 0.75,

    // listen for drop related events:

    ondropactivate: function (event) {
        // add active dropzone feedback
        event.target.classList.add('actions-drop-active')
    },
    ondragenter: function (event) {
        let draggableElement = event.relatedTarget;
        let dropzoneElement = event.target;

        // feedback the possibility of a drop
        dropzoneElement.classList.add('actions-drop-target');
        draggableElement.classList.add('action-can-drop');

        position_drop_timeout = setTimeout(function () {

            let position = event.relatedTarget;

            let single_positions = document.getElementsByClassName("position_div");

            let is_position_exist = false;
            for (let i = 0; i < single_positions.length; i++) {
                if (single_positions[i].getAttribute("data-position-name") === position.getAttribute("data-position-name")) {
                    is_position_exist = true;
                }
            }
            if (!is_position_exist) {
                let data = {};
                data = {"name": position.getAttribute("data-position-name"), "cartesian_coords": position.getAttribute("data-cartesian-coords"), "polar_coords": position.getAttribute("data-polar-coords")};

                request_asynchronous('/api/position?db=' + action_db_name + '&admin_id=' + admin_id, 'POST',
                    'application/x-www-form-urlencoded; charset=UTF-8', data, function (req, err, response) {
                        if (err === "success") {
                            let response_data = JSON.parse(response.responseText);
                            if (response_data["status"] === "OK") {
                                controlling_template_sidebar_close_btn.click();
                                sidebar_toggle_btn.click();
                            }
                        }
                    });
            }
        }, 1000);
    },
    ondragleave: function (event) {
        // remove the drop feedback style
        event.target.classList.remove('actions-drop-target');
        event.relatedTarget.classList.remove('action-can-drop');
        clearTimeout(position_drop_timeout);
    },
    ondrop: function (event) {
    },  // drop is partially works.
    ondropdeactivate: function (event) {
        // remove active dropzone feedback
        event.target.classList.remove('drop-active');
        event.target.classList.remove('drop-target')
    }
});

interact('.drag-drop')
    .draggable({
        inertia: true,
        modifiers: [
            interact.modifiers.restrictRect({
                restriction: 'parent',
                endOnly: true
            })
        ],
        autoScroll: true,
        // dragMoveListener from the dragging demo above
        onmove: function (event) {
            dragMoveListener(event);
        }
    });


stream_area_img.addEventListener("mouseover", function () {

    get_preview_span.style.color = "#008CBA";
});

stream_area_img.addEventListener("mouseout", function () {

    get_preview_span.style.color = "#000000";
});


let stream_area_img_click_count = 0;
let single_click_timeout;


video_area_div.addEventListener("click", function () {
    single_click_timeout = setTimeout(function () {

        stream_area_img_click_count++;

        if (stream_area_img_click_count <= 1) {
            stream_area_img.src = "/api/stream?type=preview&admin_id=" + admin_id;   // this url assigning creates a GET request.

            hide_element(sidebar_toggle_btn);

            dark_deep_background_div.classList.toggle("focused");
            stream_area_img.classList.toggle("focused");
            video_area_div.classList.toggle("focused");

        } else {
            request_asynchronous('/api/stream?type=preview&admin_id=' + admin_id, 'DELETE',
                'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                    if (err === "success") {
                        let response_data = JSON.parse(response.responseText);
                    }
                });
            stream_area_img.src = "";
            dark_deep_background_div.classList.toggle("focused");
            stream_area_img.classList.toggle("focused");
            video_area_div.classList.toggle("focused");
            show_element(sidebar_toggle_btn);

            stream_area_img_click_count = 0;
        }
    }, 300)
    // Todo: click and dblclick have still conflict. Solve this.
});


video_area_div.addEventListener("dblclick", function () {
    clearTimeout(single_click_timeout);
    if (stream_area_img.requestFullScreen) {
        stream_area_img.requestFullScreen();
    } else if (stream_area_img.webkitRequestFullScreen) {
        stream_area_img.webkitRequestFullScreen();
    } else if (stream_area_img.mozRequestFullScreen) {
        stream_area_img.mozRequestFullScreen();
    }
});


prismatic_menu_control_input.addEventListener("change", function () {
    prismatic_control_div.classList.toggle("focused");
    rotational_control_div.classList.toggle("hidden_element");

    prismatic_menu_control_label.classList.toggle("fa-arrows-alt");
    prismatic_menu_control_label.classList.toggle("fa-times");

    if (prismatic_menu_control_input.checked) {


    }
});


rotational_menu_control_input.addEventListener("change", function () {

    rotational_ccw_menu_control_label.click();
    // rotational_ccw_menu_control_label.classList.toggle("hidden_element");

    rotational_control_div.classList.toggle("focused");
    prismatic_control_div.classList.toggle("hidden_element");

    rotational_ccw_control_nav.classList.toggle("focused");

    rotational_menu_control_label.classList.toggle("fa-sync-alt");
    rotational_menu_control_label.classList.toggle("fa-times");

    if (rotational_menu_control_input.checked) {

        request_asynchronous('/api/move?cause=joint_count&admin_id=' + admin_id, 'GET',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {

                if (err === "success") {
                    if (requested_data["status"] === "OK") {

                        $("#rotational_control_nav button").remove();
                        $("#rotational_ccw_control_nav button").remove();

                        let joint_count = requested_data["data"];

                        for (let i = 0; i < joint_count; i++) {
                            let joint_number = i + 1;

                            let arm_joint_right_btn = document.createElement('button');
                            let arm_joint_right_i = document.createElement('i');

                            let arm_joint_left_btn = document.createElement('button');
                            let arm_joint_left_i = document.createElement('i');

                            arm_joint_right_btn.classList.add("rotational-menu-item", "joint_btn");
                            arm_joint_right_btn.id = "joint_" + joint_number + "cw_btn";
                            arm_joint_right_btn.innerHTML = translate_text_item("j-" + joint_number + " ");

                            interact('#' + arm_joint_right_btn.id)
                                .on('tap', function (event) {
                                    let route = "/api/move?id=" + joint_number + "&admin_id=" + admin_id;
                                    let data = {"type": "joint", "id": joint_number.toString(), "quantity": 5};

                                    request_asynchronous(route, 'PUT',
                                        'application/x-www-form-urlencoded; charset=UTF-8', data, function (req, err, response) {
                                            if (err === "success") {
                                                let response_data = JSON.parse(response.responseText);
                                            }
                                        });
                                })
                                .on('doubletap', function (event) {
                                })
                                .on('hold', function (event) {
                                    let route = "/api/move?id=" + joint_number + "&admin_id=" + admin_id;
                                    let data = {"type": "joint", "id": joint_number.toString(), "quantity": 5};

                                    interval = setInterval(function () {

                                        request_asynchronous(route, 'PUT',
                                            'application/x-www-form-urlencoded; charset=UTF-8', data, function (req, err, response) {
                                                if (err === "success") {
                                                    let response_data = JSON.parse(response.responseText);
                                                }
                                            });
                                    }, 300);

                                })
                                .on('down', function (event) {
                                })
                                .on('up', function (event) {
                                    clearInterval(interval);
                                });


                            arm_joint_right_i.classList.add("fas", "fa-redo");

                            arm_joint_left_btn.classList.add("rotational-menu-item", "joint_btn");
                            arm_joint_left_btn.id = "joint_" + joint_number + "ccw_btn";
                            arm_joint_left_btn.innerHTML = translate_text_item("j-" + joint_number + " ");

                            interact('#' + arm_joint_left_btn.id)
                                .on('tap', function (event) {
                                    let route = "/api/move?id=" + joint_number + "&admin_id=" + admin_id;
                                    let data = {"type": "joint", "id": joint_number.toString(), "quantity": -5};

                                    request_asynchronous(route, 'PUT',
                                        'application/x-www-form-urlencoded; charset=UTF-8', data, function (req, err, response) {
                                            if (err === "success") {
                                                let response_data = JSON.parse(response.responseText);
                                            }
                                        });
                                })
                                .on('doubletap', function (event) {
                                })
                                .on('hold', function (event) {
                                    let route = "/api/move?id=" + joint_number + "&admin_id=" + admin_id;
                                    let data = {"type": "joint", "id": joint_number.toString(), "quantity": -5};

                                    interval = setInterval(function () {

                                        request_asynchronous(route, 'PUT',
                                            'application/x-www-form-urlencoded; charset=UTF-8', data, function (req, err, response) {
                                                if (err === "success") {
                                                    let response_data = JSON.parse(response.responseText);
                                                }
                                            });
                                    }, 300);

                                })
                                .on('down', function (event) {
                                })
                                .on('up', function (event) {
                                    clearInterval(interval);
                                });

                            arm_joint_left_i.classList.add("fas", "fa-undo");

                            arm_joint_right_btn.appendChild(arm_joint_right_i);
                            arm_joint_left_btn.appendChild(arm_joint_left_i);

                            rotational_control_nav.appendChild(arm_joint_right_btn);
                            rotational_ccw_control_nav.appendChild(arm_joint_left_btn);
                        }
                    }
                }
            });
    }
});


let record_pos_sce_btn_click_count = 0;

record_pos_sce_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    record_pos_sce_div.classList.toggle("focused");
    motion_control_div.classList.toggle("hidden_element");
    video_area_div.classList.toggle("hidden_element");
    controlling_template_sidebar.classList.toggle("hidden_element");
    sidebar_toggle_btn.classList.toggle("hidden_element");

    record_pos_sce_btn_click_count++;
    if (record_pos_sce_btn_click_count <= 1) {

        record_pos_sce_btn.innerHTML = translate_text_item("cancel");

        current_arm_position = {};

        request_asynchronous('/api/stream?admin_id=' + admin_id, 'GET',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
                if (err === "success") {
                    if (requested_data["status"] === "OK") {

                        current_arm_position = requested_data["data"];
                        console.log(requested_data["data"]);
                    }
                }
            });

    } else {
        record_pos_sce_btn.innerHTML = translate_text_item("save");
        position_div_back_btn.click();
        scenario_div_back_btn.click();

        record_pos_sce_btn_click_count = 0
    }
});


record_as_pos_btn.addEventListener("click", function () {
    pos_sce_select_div.classList.add("inactive");
    create_pos_btn.disabled = true;

    setTimeout(function () {
        record_as_position_div.classList.add("focused");
    }, 175)
});


position_div_back_btn.addEventListener("click", function () {
    record_as_position_div.classList.remove("focused");
    setTimeout(function () {
        pos_sce_select_div.classList.remove("inactive");
    }, 175)
});


position_name_input.addEventListener("mousemove", function () {
    create_pos_btn.disabled = position_name_input.value === "";
});


create_pos_btn.addEventListener("click", function () {

    let data = {};
    data = {"name": position_name_input.value, "cartesian_coords": current_arm_position["cartesian_coords"], "polar_coords": current_arm_position["polar_coords"]};
    // let data = {};
    // data = Object.assign({}, name_dict, current_arm_position);

    console.log(data);

    request_asynchronous('/api/position?db=' + action_db_name + '&admin_id=' + admin_id, 'POST',
        'application/json; charset=UTF-8', data, function (req, err, response) {
            if (err === "success") {
                let response_data = JSON.parse(response.responseText);
            }
        });

    position_name_input.value = "";
    position_div_back_btn.click();
    record_pos_sce_btn.click();

    swal(translate_text_item("Position Created!"), "", "success");
});

record_in_sce_btn.addEventListener("click", function () {
    pos_sce_select_div.classList.add("inactive");
    create_sce_btn.disabled = true;

    setTimeout(function () {
        record_in_scenario_div.classList.add("focused");
    }, 175);


    while (record_in_scenario_list_ul.firstChild) {
        record_in_scenario_list_ul.removeChild(record_in_scenario_list_ul.firstChild);
    }

    request_asynchronous('/api/scenario?db=' + action_db_name + '&admin_id=' + admin_id, 'GET',
        'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
            // err = "success"
            // requested_data = {"status": "OK", "data": [{"id": "b97tr40a-alcb-31w9-b150-ce2f6156l1ed", "name": "scenario_name1", "positions": [{}, {}]}, {"id": "b97dr48a-aecb-11e9-b130-cc2f7156l1ed", "name": "scenario_name2_name2", "positions": [{}, {}]}]};
            if (err === "success") {
                if (requested_data["status"] === "OK") {
                    let scenarios = requested_data["data"];

                    for (let i = 0; i < scenarios.length; i++) {
                        let scenario_div = document.createElement('div');
                        let scenario_btn = document.createElement('button');

                        scenario_div.classList.add("mt-1", "border_try", "select_existing_scenario_div", "text-center");
                        scenario_div.id = scenarios[i]["id"];

                        scenario_btn.classList.add("btn", "btn-info");
                        scenario_btn.innerHTML = scenarios[i]["name"];

                        scenario_btn.addEventListener("click", function () {
                            let position_init = {"id": null, "name": "position_of_" + scenarios[i]["name"]};

                            let position = Object.assign({}, position_init, current_arm_position);

                            scenarios[i]["positions"].push(position);

                            request_asynchronous('/api/scenario?db=' + action_db_name + "&id=" + scenarios[i]["id"] + '&admin_id=' + admin_id, 'PUT',
                                'application/x-www-form-urlencoded; charset=UTF-8', scenarios[i], function (req, err, response) {
                                    if (err === "success") {
                                        let response_data = JSON.parse(response.responseText);
                                    }
                                });
                        });

                        scenario_div.appendChild(scenario_btn);
                        record_in_scenario_list_ul.appendChild(scenario_div);
                    }
                }
            }
        });
});

scenario_div_back_btn.addEventListener("click", function () {
    record_in_scenario_div.classList.remove("focused");
    setTimeout(function () {
        pos_sce_select_div.classList.remove("inactive");
    }, 175)
});

scenario_name_input.addEventListener("mousemove", function () {
    create_sce_btn.disabled = scenario_name_input.value === "";
});

create_sce_btn.addEventListener("click", function () {

    // let name_dict = {"name": position_name_input.value};
    // let data = Object.assign({}, name_dict, current_arm_position);

    // request_asynchronous('/api/position?db=' + action_db_name + '&admin_id=' + admin_id, 'POST',
    //     'application/x-www-form-urlencoded; charset=UTF-8', data, function (req, err, response) {
    //         if (err === "success") {
    //             let response_data = JSON.parse(response.responseText);
    //         }
    //     });

    //Todo: Handle the scenario creating and adding position new scenario processes.

    scenario_name_input.value = "";
    scenario_div_back_btn.click();
    record_pos_sce_btn.click();

    swal(translate_text_item("Position Added in New Scenario!"), "", "success");
});
