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

function stop_stream(type) {
    jquery_manager.delete_data("/api/stream?type=" + type + "&admin_id=" + admin_id);

}

function get_move_info(cause=null) {
    jquery_manager.get_data("/api/move?cause=" + cause + "&admin_id=" + admin_id);
}

function get_position_s(id = null) {

    if (id == null) {
        jquery_manager.get_data("/api/position?admin_id=" + admin_id);

    } else {
        jquery_manager.get_data("/api/position?id=" + id + "&admin_id=" + admin_id);

    }
}

function get_scenario_s(id = null) {

    if (id == null) {
        jquery_manager.get_data("/api/scenario?admin_id=" + admin_id);

    } else {
        jquery_manager.get_data("/api/scenario?id=" + id + "&admin_id=" + admin_id);
    }
}


sidebar_toggle_btn.addEventListener("click", function () {

    get_position_s();

    let timer_settings_cont = setInterval(function () {

        if (requested_data !== {}) {
            if (requested_data["status"] === "OK") {

                console.log(requested_data["data"]);

                for (let c = 0; c < requested_data["data"].length; c++) {
                    let li = document.createElement('li');
                    let section = document.createElement('section');

                    let name_output = document.createElement('output');

                    name_output.value = requested_data["data"][c]["name"];

                    li.appendChild(section);
                    section.appendChild(name_output);

                    position_list_ul.appendChild(li);
                }

                controlling_template_sidebar.classList.toggle("active");
                dark_deep_background_div.classList.toggle("focused");
                hide_element(controlling_template_content)
            }
            requested_data = {};
            clearInterval(timer_settings_cont)
        }
    }, 300);

    get_scenario_s();

    timer_settings_cont = setInterval(function () {

        if (requested_data !== {}) {
            if (requested_data["status"] === "OK") {

                console.log(requested_data["data"]);

                for (let c = 0; c < requested_data["data"].length; c++) {
                    let li = document.createElement('li');
                    let section = document.createElement('section');

                    let name_output = document.createElement('output');

                    name_output.value = requested_data["data"][c]["name"];

                    li.appendChild(section);
                    section.appendChild(name_output);

                    position_list_ul.appendChild(li);
                }

                controlling_template_sidebar.classList.toggle("active");
                dark_deep_background_div.classList.toggle("focused");
                hide_element(controlling_template_content)
            }
            requested_data = {};
            clearInterval(timer_settings_cont)
        }
    }, 300);


    // controlling_template_sidebar.classList.toggle("active");
    // dark_deep_background_div.classList.toggle("focused");
    // hide_element(controlling_template_content)
});

controlling_template_sidebar_close_btn.addEventListener("click", function () {

    controlling_template_sidebar.classList.toggle("active");
    dark_deep_background_div.classList.toggle("focused");
    show_element(controlling_template_content)
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
            stop_stream("preview");
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
    console.log("clicked_rotational");
    rotational_ccw_menu_control_label.click();
    // rotational_ccw_menu_control_label.classList.toggle("hidden_element");

    rotational_control_div.classList.toggle("focused");
    prismatic_control_div.classList.toggle("hidden_element");

    rotational_ccw_control_nav.classList.toggle("focused");

    rotational_menu_control_label.classList.toggle("fa-sync-alt");
    rotational_menu_control_label.classList.toggle("fa-times");

    if (rotational_menu_control_input.checked) {
        // get_move_info("joint_count");
        requested_data = {"status": "OK", "data": "5"};

        let timer_settings_cont = setInterval(function () {

            if (requested_data !== {}) {
                if (requested_data["status"] === "OK") {

                    $("#rotational_control_nav button").remove();
                    $("#rotational_ccw_control_nav button").remove();

                    let joint_count = requested_data["data"];
                    // console.log(requested_data["data"]);

                    for (let i = 0; i < joint_count; i++) {
                        let joint_number = i + 1;

                        let arm_joint_right_btn = document.createElement('button');
                        let arm_joint_right_i = document.createElement('i');

                        let arm_joint_left_btn = document.createElement('button');
                        let arm_joint_left_i = document.createElement('i');

                        arm_joint_right_btn.classList.add("rotational-menu-item", "joint_btn");
                        arm_joint_right_btn.id = "joint_" + joint_number + "cw_btn";
                        arm_joint_right_btn.innerHTML = translate_text_item("j-" + joint_number + " ");

                        arm_joint_right_btn.addEventListener("mousedown", function () {

                            let route = "/api/move?id=" + joint_number + "&admin_id=" + admin_id;
                            let data = {"type": "joint", "id": joint_number.toString(), "quantity": 5};

                            interval = setInterval(function () {
                                // console.log("gönderdi");
                                jquery_manager.put_data(route, data);
                            }, 300);
                        });

                        arm_joint_right_btn.addEventListener("mouseup", function () {
                            clearInterval(interval);
                        });


                        arm_joint_right_i.classList.add("fas", "fa-redo");

                        arm_joint_left_btn.classList.add("rotational-menu-item", "joint_btn");
                        arm_joint_left_btn.id = "joint_" + joint_number + "ccw_btn";
                        arm_joint_left_btn.innerHTML = translate_text_item("j-" + joint_number + " ");

                        arm_joint_left_btn.addEventListener("mousedown", function () {

                            let route = "/api/move?id=" + joint_number + "&admin_id=" + admin_id;
                            let data = {"type": "joint", "id": joint_number.toString(), "quantity": -5};

                            interval = setInterval(function () {
                                // console.log("gönderdi");
                                jquery_manager.put_data(route, data);
                            }, 300);
                        });

                        arm_joint_left_btn.addEventListener("mouseup", function () {
                            clearInterval(interval);
                        });

                        arm_joint_left_i.classList.add("fas", "fa-undo");

                        arm_joint_right_btn.appendChild(arm_joint_right_i);
                        arm_joint_left_btn.appendChild(arm_joint_left_i);

                        rotational_control_nav.appendChild(arm_joint_right_btn);
                        rotational_ccw_control_nav.appendChild(arm_joint_left_btn);
                    }
                }
                requested_data = {};
                clearInterval(timer_settings_cont)
            }
        }, 300);

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

        get_move_info();
        let timer_settings_cont = setInterval(function () {

            if (requested_data !== {}) {
                if (requested_data["status"] === "OK") {

                    current_arm_position = requested_data["data"];
                    // console.log(requested_data["data"]);
                }
                requested_data = {};
                clearInterval(timer_settings_cont)
            }
        }, 300);

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

    let name_dict = {"name": position_name_input.value};
    let data = Object.assign({}, name_dict, current_arm_position);

    jquery_manager.post_data("/api/position?db=" + "predicted_missions" + "&admin_id=" + admin_id, data);

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

    // get_scenario_s();
    requested_data = {
        "status": "OK", "data": [
            {
                "id": "b97tr40a-alcb-31w9-b150-ce2f6156l1ed",
                "name": "scenario_name1",
                "positions": [{}, {}]
            }, {
                "id": "b97dr48a-aecb-11e9-b130-cc2f7156l1ed",
                "name": "scenario_name2_name2",
                "positions": [{}, {}]
            }
        ]
    };

    while (record_in_scenario_list_ul.firstChild) {
            record_in_scenario_list_ul.removeChild(record_in_scenario_list_ul.firstChild);
        }

    let timer_settings_cont = setInterval(function () {
        if (requested_data !== {}) {
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

                            jquery_manager.put_data("/api/scenario?db=" + db_name + "&id=" + id + "&admin_id=" + admin_id, scenarios[i])
                        });

                        scenario_div.appendChild(scenario_btn);
                        record_in_scenario_list_ul.appendChild(scenario_div);
                    }
                }
                requested_data = {};
                clearInterval(timer_settings_cont)
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

    // jquery_manager.post_data("/api/position?db=" + "predicted_missions" + "&admin_id=" + admin_id, data);

    //Todo: Handle the scenario creating and adding position new scenario processes.

    scenario_name_input.value = "";
    scenario_div_back_btn.click();
    record_pos_sce_btn.click();

    swal(translate_text_item("Position Added in New Scenario!"), "", "success");
});



