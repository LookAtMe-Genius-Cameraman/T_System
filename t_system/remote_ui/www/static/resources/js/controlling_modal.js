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

const advanced_edit_div = document.getElementById("advanced_edit_div");

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

sidebar_toggle_btn.addEventListener("click", function (x) {

    setSwiperSwiping(false);

    clearElement(position_list_ul);
    clearElement(scenario_list_ul);

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    controlling_template_sidebar.classList.toggle("active");
    hide_element(controlling_template_content);

    let positions = [];
    let scenarios = [];


    request_asynchronous('/api/position?db=' + action_db_name + '&admin_id=' + admin_id + '&root=' + allow_root, 'GET',
        'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
            // err = "success"
            // requested_data = {"status": "OK", "data": [{"id": "j470138f-agcb-11e9-b130-ce4f744661fd", "name": "position_name", "cartesian_coords": [30, 25, 42], "polar_params": {"coords": [1.5, 1.02, 0.5], "delays": [1, 0.5, 1], "divide_counts": [3, 2, 1]}}]};

            if (err === "success") {
                if (requested_data["status"] === "OK") {

                    positions = requested_data["data"];
                    // console.log(positions);

                    for (let c = 0; c < positions.length; c++) {

                        let position_div = document.createElement('div');
                        let position_span = document.createElement('span');

                        let position_context_menu = document.createElement('div');
                        let position_cm_remove_a = document.createElement('a');
                        let position_cm_rename_a = document.createElement('a');

                        position_div.classList.add("draggable_position", "drag-drop", "ml-1", "mr-1", "position_div");
                        position_div.setAttribute("data-position-name", positions[c]["name"]);
                        position_div.setAttribute("data-cartesian-coords", positions[c]["cartesian_coords"]);
                        position_div.setAttribute("data-polar-coords", positions[c]["polar_params"]["coords"]);
                        position_div.setAttribute("data-polar-delays", positions[c]["polar_params"]["delays"]);
                        position_div.setAttribute("data-polar-divide-counts", positions[c]["polar_params"]["divide_counts"]);

                        position_span.classList.add("shine_in_dark");
                        position_span.innerHTML = positions[c]["name"];
                        position_span.id = positions[c]["name"] + "_span_" + c;

                        function hide_context_menu() {
                            $("#" + position_context_menu.id).removeClass("show").hide();
                            document.removeEventListener("click", hide_context_menu);
                        }

                        interact('#' + position_span.id)
                            .on('tap', function (event) {
                                if (!position_context_menu.classList.contains("show")) {
                                    let data = {};
                                    request_asynchronous('/api/move?db=' + action_db_name + '&action=' + positions[c]["name"] + '&a_type=position' + '&admin_id=' + admin_id + '&root=' + allow_root, 'POST',
                                        'application/json; charset=UTF-8', data, function (req, err, response) {
                                            if (err === "success") {
                                                let response_data = JSON.parse(response.responseText);
                                                if (response_data["status"] === "OK") {
                                                } else {
                                                }
                                            }
                                        });
                                }
                            })
                            .on('doubletap', function (event) {
                            })
                            .on('hold', function (event) {
                                position_span.classList.add("disable_pointer");

                                let target = event.target;
                                let x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
                                let y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

                                position_context_menu.setAttribute('data-x', x);
                                position_context_menu.setAttribute('data-y', y);

                                $("#" + position_context_menu.id).css({
                                    display: "block",
                                    transform: 'translate(' + x + 'px, ' + y + 'px)',
                                }).addClass("show");

                                setTimeout(function () {
                                    position_span.classList.remove("disable_pointer");
                                    document.addEventListener("click", hide_context_menu);
                                }, 500);

                                return false; //blocks default WebBrowser right click menu
                            })
                            .on('down', function (event) {
                            })
                            .on('up', function (event) {
                            });

                        position_context_menu.classList.add("position-relative", "dropdown-menu", "dropdown-menu-sm");
                        position_context_menu.id = positions[c]["name"] + "context-menu_" + c;

                        $("#" + position_context_menu.id + " a").on("click", function () {
                            $(this).parent().removeClass("show").hide();
                        });

                        position_cm_remove_a.classList.add("dropdown-item");
                        position_cm_remove_a.innerHTML = translate_text_item("remove");

                        position_cm_remove_a.addEventListener("click", function () {
                            JSalert(translate_text_item("Position Deleting!"),
                                translate_text_item("You are about to delete the position: ") + "\n" + positions[c]["name"],
                                translate_text_item("OK"), translate_text_item("CANCEL"), function () {
                                    request_asynchronous('/api/position?db=' + action_db_name + '&id=' + positions[c]["id"] + '&admin_id=' + admin_id + '&root=' + allow_root, 'DELETE',
                                        'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                                            if (err === "success") {
                                                let response_data = JSON.parse(response.responseText);
                                            }
                                        });
                                })
                        });

                        position_cm_rename_a.classList.add("dropdown-item");
                        position_cm_rename_a.innerHTML = translate_text_item("rename");

                        position_cm_rename_a.addEventListener("click", function () {
                            position_div.removeChild(position_span);
                            position_div.removeChild(position_context_menu);

                            let position_input = document.createElement('input');

                            position_input.type = "text";
                            position_input.placeholder = position_span.innerHTML;
                            position_input.classList.add("action_name_input");

                            position_input.addEventListener("focusout", function () {
                                if (position_input.value !== position_span.innerHTML && position_input.value !== "") {
                                    let data = {"name": position_input.value, "cartesian_coords": positions[c]["cartesian_coords"], "polar_params": positions[c]["polar_params"]};

                                    request_asynchronous('/api/position?db=' + action_db_name + '&id=' + positions[c]["id"] + '&admin_id=' + admin_id + '&root=' + allow_root, 'PUT',
                                        'application/json; charset=UTF-8', data, function (req, err, response) {
                                            if (err === "success") {
                                                let response_data = JSON.parse(response.responseText);
                                            }
                                        });
                                    position_span.innerHTML = position_input.value
                                }
                                position_div.removeChild(position_input);
                                position_div.appendChild(position_span);
                                position_div.appendChild(position_context_menu);

                            });
                            position_div.appendChild(position_input);
                            position_input.focus();
                        });

                        position_context_menu.appendChild(position_cm_remove_a);
                        position_context_menu.appendChild(position_cm_rename_a);

                        position_div.appendChild(position_span);
                        position_div.appendChild(position_context_menu);

                        position_list_ul.appendChild(position_div);
                    }
                }
            }
        });

    request_asynchronous('/api/scenario?db=' + action_db_name + '&admin_id=' + admin_id + '&root=' + allow_root, 'GET',
        'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
            // err = "success"
            // requested_data = {"status": "OK", "data": [{"id": "b97tr40a-alcb-31w9-b150-ce2f6156l1ed", "name": "scenario_name1", "positions": [{"name": "pos1"}, {"name": "pos2"}]}, {"id": "b97dr48a-aecb-11e9-b130-cc2f7156l1ed", "name": "scenario_name2", "positions": [{}, {}]}]};

            if (err === "success") {
                if (requested_data["status"] === "OK") {

                    scenarios = requested_data["data"];
                    console.log(scenarios);

                    for (let c = 0; c < scenarios.length; c++) {

                        let scenario_dropdown_div = document.createElement('div');
                        let scenario_btn = document.createElement('button');
                        let scenario_dd_btn = document.createElement('button');
                        let scenario_dd_span = document.createElement('span');
                        let scenario_dropdown_container_div = document.createElement('div');

                        let scenario_context_menu = document.createElement('div');
                        let scenario_cm_remove_a = document.createElement('a');
                        let scenario_cm_rename_a = document.createElement('a');
                        let scenario_cm_advanced_a = document.createElement('a');

                        scenario_dropdown_div.classList.add("dropdown", "mt-1", "ml-1", "mr-1", "scenario_name_btn");
                        scenario_dropdown_div.id = scenarios[c]["id"] + "_dropdown_div";

                        scenario_context_menu.classList.add("position-relative", "dropdown-menu", "dropdown-menu-sm");
                        scenario_context_menu.id = scenarios[c]["id"] + "context-menu";

                        scenario_cm_remove_a.classList.add("dropdown-item");
                        scenario_cm_remove_a.innerHTML = translate_text_item("remove");

                        scenario_cm_remove_a.addEventListener("click", function () {
                            JSalert(translate_text_item("Scenario Deleting!"),
                                translate_text_item("You are about to delete this scenario: ") + "\n" + scenarios[c]["name"],
                                translate_text_item("OK"), translate_text_item("CANCEL"), function () {
                                    request_asynchronous('/api/scenario?db=' + action_db_name + '&id=' + scenarios[c]["id"] + '&admin_id=' + admin_id + '&root=' + allow_root, 'DELETE',
                                        'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                                            if (err === "success") {
                                                let response_data = JSON.parse(response.responseText);
                                            }
                                        });
                                })
                        });

                        scenario_cm_rename_a.classList.add("dropdown-item");
                        scenario_cm_rename_a.innerHTML = translate_text_item("rename");

                        scenario_cm_rename_a.addEventListener("click", function () {
                            scenario_dropdown_div.removeChild(scenario_btn);
                                    scenario_dropdown_div.removeChild(scenario_dd_btn);
                                    scenario_dropdown_div.removeChild(scenario_dropdown_container_div);
                                    scenario_dropdown_div.removeChild(scenario_context_menu);

                                    let scenario_input = document.createElement('input');

                                    scenario_input.type = "text";
                                    scenario_input.placeholder = scenario_btn.innerHTML;
                                    scenario_input.classList.add("action_name_input");

                                    scenario_input.addEventListener("focusout", function () {
                                        if (scenario_input.value !== scenario_btn.innerHTML && scenario_input.value !== "") {
                                            let data = {"name": scenario_input.value, "positions": scenarios[c]["positions"]};

                                            request_asynchronous('/api/scenario?db=' + action_db_name + '&id=' + scenarios[c]["id"] + '&admin_id=' + admin_id + '&root=' + allow_root, 'PUT',
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
                                        scenario_dropdown_div.appendChild(scenario_context_menu);
                                    });
                                    scenario_dropdown_div.appendChild(scenario_input);
                                    scenario_input.focus();
                        });

                        scenario_cm_advanced_a.classList.add("dropdown-item");
                        scenario_cm_advanced_a.innerHTML = translate_text_item("advanced edit");

                        scenario_cm_advanced_a.addEventListener("click", function () {

                            advanced_edit_div.classList.add("active");

                            let scenario_backup = scenarios[c];

                            let advance_sce_close_a = document.createElement('a');

                            let advance_sce_title_div = document.createElement('div');
                            let advance_sce_header_a = document.createElement('a');
                            let advance_sce_name_span = document.createElement('span');

                            let advance_positions_list_ul = document.createElement('ul');

                            let advance_sce_btns_div = document.createElement('div');
                            let advance_sce_simulate_btn = document.createElement('button');
                            let advance_sce_save_btn = document.createElement('button');

                            advance_sce_close_a.classList.add("close", "advance_sce_close_a");
                            advance_sce_close_a.innerHTML = "X";
                            advance_sce_close_a.title = translate_text_item("Close");

                            advance_sce_close_a.addEventListener("click", function () {
                                scenarios[c] = scenario_backup;

                                clearElement(advanced_edit_div);
                                advanced_edit_div.classList.remove("active");
                            });

                            advance_sce_title_div.classList.add("position-absolute", "advanced_title_div", "mb-2");

                            advance_sce_header_a.innerHTML = translate_text_item("Scenario name: ");

                            advance_sce_name_span.classList.add("cut-text", "advanced_scenario_name");
                            advance_sce_name_span.innerHTML = scenarios[c]["name"];
                            advance_sce_name_span.title = scenarios[c]["name"];

                            for (let i = 0; i < scenarios[c]["positions"].length; i++) {

                                let advance_position_dd_div = document.createElement('div');
                                let advance_position_dd_a = document.createElement('a');
                                let advance_position_dd_container_div = document.createElement('div');

                                let advance_po_ca_co_div = document.createElement('div');
                                let advance_po_ca_co_header_a = document.createElement('a');
                                let advance_po_ca_co_name_span = document.createElement('span');

                                let advance_po_divider_div = document.createElement('div');

                                advance_position_dd_div.classList.add("dropdown", "mb-2");
                                // advance_position_dd_div.classList.add("dropdown", "show", "draggable_position", "drag-drop");

                                advance_position_dd_a.classList.add("dropdown-toggle", "btn", "btn-outline-info");

                                advance_position_dd_a.role = "button";
                                advance_position_dd_a.id = scenarios[c]["positions"][i]["id"] + "_a";
                                advance_position_dd_a.setAttribute("data-toggle", "dropdown");
                                advance_position_dd_a.setAttribute("aria-haspopup", "true");
                                advance_position_dd_a.setAttribute("aria-expanded", "false");
                                advance_position_dd_a.innerHTML = scenarios[c]["positions"][i]["name"];
                                advance_position_dd_a.title = advance_position_dd_a.innerHTML;

                                advance_position_dd_a.addEventListener("click", function () {
                                    advance_position_dd_container_div.classList.toggle("show")
                                });

                                advance_position_dd_container_div.classList.add("position-relative", "dropdown-menu", "dropdown-menu-right", "dropdown_menu", "advanced_pos_dropdown_menu");
                                advance_position_dd_container_div.classList.add("container");
                                advance_position_dd_container_div.setAttribute("aria-labelledby", advance_position_dd_a.id);

                                advance_po_ca_co_div.classList.add("dropdown-item", "ml-0", "advanced_cartesian_div");

                                advance_po_ca_co_header_a.innerHTML = translate_text_item("Cartesian coordinates: ");
                                let rounded_c_coords = [];
                                for (let count = 0; count < scenarios[c]["positions"][i]["cartesian_coords"].length; count++) {
                                    rounded_c_coords.push(scenarios[c]["positions"][i]["cartesian_coords"][count].toFixed(2));
                                }

                                advance_po_ca_co_name_span.classList.add("cut-text", "advanced_cartesian_span");
                                advance_po_ca_co_name_span.innerHTML = rounded_c_coords.toString();

                                advance_po_divider_div.classList.add("dropdown-divider");

                                advance_position_dd_container_div.appendChild(advance_po_ca_co_div);
                                advance_position_dd_container_div.appendChild(advance_po_divider_div);

                                for (let a = 0; a < scenarios[c]["positions"][i]["polar_params"]["coords"].length; a++) {

                                    let ad_po_joint_div = document.createElement('div');

                                    let ad_po_joint_header_div = document.createElement('div');
                                    let ad_po_joint_header_a = document.createElement('a');
                                    let ad_po_joint_theta_span = document.createElement('span');

                                    let ad_po_joint_slider_div = document.createElement('div');

                                    let ad_po_joint_speed_div = document.createElement('div');
                                    let ad_po_joint_speed_a = document.createElement('a');
                                    let ad_po_joint_speed_input = document.createElement('input');

                                    let ad_po_joint_precision_div = document.createElement('div');
                                    let ad_po_joint_precision_a = document.createElement('a');
                                    let ad_po_joint_precision_input = document.createElement('input');

                                    ad_po_joint_div.classList.add("ml-0", "dropdown-item", "row", "advance_joint_div");

                                    ad_po_joint_header_div.classList.add("row", "mb-1", "advance_joint_header_div");

                                    ad_po_joint_header_a.classList.add("advance_small_font", "mr-2");
                                    ad_po_joint_header_a.innerHTML = translate_text_item("j-" + (a + 1)) + ":";

                                    ad_po_joint_theta_span.classList.add("advance_small_font");
                                    ad_po_joint_theta_span.innerHTML = Math.round(scenarios[c]["positions"][i]["polar_params"]["coords"][a] * 180 / 3.1416) + "°";

                                    ad_po_joint_slider_div.classList.add("row");

                                    ad_po_joint_speed_div.classList.add("row", "mt-1", "mb-2", "advance_slider_div");

                                    ad_po_joint_speed_a.classList.add("mr-2", "advance_small_font", "advance_slider_title");
                                    ad_po_joint_speed_a.innerHTML = translate_text_item("speed: ");

                                    ad_po_joint_speed_input.classList.add("custom-range", "advance_slider");
                                    ad_po_joint_speed_input.type = "range";
                                    ad_po_joint_speed_input.value = (scenarios[c]["positions"][i]["polar_params"]["delays"][a] * 10) / 2;
                                    ad_po_joint_speed_input.id = scenarios[c]["name"] + "_" + scenarios[c]["positions"][i]["name"] + "_speed_slider_" + a;
                                    ad_po_joint_speed_input.setAttribute("min", "1");
                                    ad_po_joint_speed_input.setAttribute("max", "5");
                                    ad_po_joint_speed_input.setAttribute("step", "1");

                                    ad_po_joint_speed_input.addEventListener("change", function () {
                                        scenarios[c]["positions"][i]["polar_params"]["delays"][a] = (ad_po_joint_speed_input.value / 10) * 2;
                                    });

                                    ad_po_joint_precision_div.classList.add("row", "mt-2", "advance_slider_div");

                                    ad_po_joint_precision_a.classList.add("mr-2", "advance_small_font", "advance_slider_title");
                                    ad_po_joint_precision_a.innerHTML = translate_text_item("precision: ");

                                    ad_po_joint_precision_input.classList.add("custom-range", "advance_slider");
                                    ad_po_joint_precision_input.type = "range";
                                    ad_po_joint_precision_input.value = scenarios[c]["positions"][i]["polar_params"]["divide_counts"][a];
                                    ad_po_joint_precision_input.id = scenarios[c]["name"] + "_" + scenarios[c]["positions"][i]["name"] + "_precision_slider_" + a;
                                    ad_po_joint_precision_input.setAttribute("min", "1");
                                    ad_po_joint_precision_input.setAttribute("max", "5");
                                    ad_po_joint_precision_input.setAttribute("step", "1");

                                    ad_po_joint_precision_input.addEventListener("change", function () {
                                        scenarios[c]["positions"][i]["polar_params"]["divide_counts"][a] = ad_po_joint_precision_input.value;
                                    });

                                    ad_po_joint_header_div.appendChild(ad_po_joint_header_a);
                                    ad_po_joint_header_div.appendChild(ad_po_joint_theta_span);

                                    ad_po_joint_speed_div.appendChild(ad_po_joint_speed_a);
                                    ad_po_joint_speed_div.appendChild(ad_po_joint_speed_input);

                                    ad_po_joint_precision_div.appendChild(ad_po_joint_precision_a);
                                    ad_po_joint_precision_div.appendChild(ad_po_joint_precision_input);

                                    ad_po_joint_slider_div.appendChild(ad_po_joint_speed_div);
                                    ad_po_joint_slider_div.appendChild(ad_po_joint_precision_div);

                                    ad_po_joint_div.appendChild(ad_po_joint_header_div);
                                    ad_po_joint_div.appendChild(ad_po_joint_slider_div);

                                    advance_position_dd_container_div.appendChild(ad_po_joint_div);
                                }
                                advance_po_ca_co_div.appendChild(advance_po_ca_co_header_a);
                                advance_po_ca_co_div.appendChild(advance_po_ca_co_name_span);

                                advance_position_dd_div.appendChild(advance_position_dd_a);
                                advance_position_dd_div.appendChild(advance_position_dd_container_div);

                                advance_positions_list_ul.appendChild(advance_position_dd_div);
                            }
                            advance_positions_list_ul.classList.add("mt-5", "mb-2", "advance_positions_ul");

                            advance_sce_btns_div.classList.add("position-absolute", "mt-2", "advance_sce_btns_div");

                            advance_sce_simulate_btn.classList.add("btn", "btn-outline-warning", "mr-2");
                            advance_sce_simulate_btn.innerHTML = translate_text_item("simulate");

                            advance_sce_simulate_btn.addEventListener("click", function () {

                                advance_sce_save_btn.disabled = true;

                                let data = {};

                                request_asynchronous('/api/move?db=' + action_db_name + '&action=' + scenarios[c]["name"] + '&a_type=scenario' + '&admin_id=' + admin_id + '&root=' + allow_root, 'POST',
                                    'application/json; charset=UTF-8', data, function (req, err, response) {
                                        if (err === "success") {
                                            let response_data = JSON.parse(response.responseText);
                                            if (response_data["status"] === "OK") {
                                                advance_sce_save_btn.disabled = false;
                                            } else {
                                            }
                                        }
                                    });
                            });


                            advance_sce_save_btn.classList.add("btn", "btn-outline-success", "mr-2");
                            advance_sce_save_btn.innerHTML = translate_text_item("save changes");

                            advance_sce_save_btn.addEventListener("click", function () {
                                let data = {"name": scenarios[c]["name"], "positions": scenarios[c]["positions"]};

                                request_asynchronous('/api/scenario?db=' + action_db_name + '&id=' + scenarios[c]["id"] + '&admin_id=' + admin_id + '&root=' + allow_root, 'PUT',
                                    'application/json; charset=UTF-8', data, function (req, err, response) {
                                        if (err === "success") {
                                            let response_data = JSON.parse(response.responseText);

                                            if (response_data["status"] === "OK") {
                                                scenario_cm_advanced_a.click();
                                                swal(translate_text_item("Changes saved."), "", "success");
                                            } else {
                                                swal(translate_text_item("Scenario editing failed!"), "", "error");
                                            }
                                        }
                                    });

                                clearElement(advanced_edit_div);
                                advanced_edit_div.classList.remove("active");

                                controlling_template_sidebar_close_btn.click();
                                sidebar_toggle_btn.click();
                            });

                            advance_sce_title_div.appendChild(advance_sce_header_a);
                            advance_sce_title_div.appendChild(advance_sce_name_span);

                            advance_sce_btns_div.appendChild(advance_sce_simulate_btn);
                            advance_sce_btns_div.appendChild(advance_sce_save_btn);

                            advanced_edit_div.appendChild(advance_sce_close_a);
                            advanced_edit_div.appendChild(advance_sce_title_div);
                            advanced_edit_div.appendChild(advance_positions_list_ul);
                            advanced_edit_div.appendChild(advance_sce_btns_div);
                        });

                        scenario_btn.classList.add("btn", "btn-dark");
                        scenario_btn.type = "button";
                        scenario_btn.id = scenarios[c]["name"] + "_btn";
                        scenario_btn.innerHTML = scenarios[c]["name"];

                        interact('#' + scenario_btn.id).dropzone({
                            accept: '.draggable_position',
                            overlap: 0.75,

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

                        function hide_context_menu() {
                            $("#" + scenario_context_menu.id).removeClass("show").hide();
                            document.removeEventListener("click", hide_context_menu);
                        }

                        interact('#' + scenario_btn.id)
                            .on('tap', function (event) {

                                if (!scenario_context_menu.classList.contains("show")) {
                                    let data = {};

                                request_asynchronous('/api/move?db=' + action_db_name + '&action=' + scenarios[c]["name"] + '&a_type=scenario' + '&admin_id=' + admin_id + '&root=' + allow_root, 'POST',
                                    'application/json; charset=UTF-8', data, function (req, err, response) {
                                        if (err === "success") {
                                            let response_data = JSON.parse(response.responseText);
                                            if (response_data["status"] === "OK") {} else {}
                                        }
                                    });
                                }
                            })
                            .on('doubletap', function (event) {
                            })
                            .on('hold', function (event) {
                                scenario_btn.classList.add("disable_pointer");
                                let target = event.target;
                                let x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
                                let y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

                                scenario_context_menu.setAttribute('data-x', x);
                                scenario_context_menu.setAttribute('data-y', y);

                                $("#" + scenario_context_menu.id).css({
                                    display: "block",
                                    transform: 'translate(' + x + 'px, ' + y - 50 + 'px)',
                                }).addClass("show");

                                document.addEventListener("click", hide_context_menu);

                                setTimeout(function () {
                                    scenario_btn.classList.remove("disable_pointer");
                                }, 500);

                                return false; //blocks default WebBrowser right click menu
                            })
                            .on('down', function (event) {
                            })
                            .on('up', function (event) {
                            });

                        $("#" + scenario_context_menu.id + " a").on("click", function () {
                            $(this).parent().removeClass("show").hide();
                        });

                        scenario_dd_btn.classList.add("btn", "btn-dark", "dropdown-toggle", "dropdown-toggle-split");
                        scenario_dd_btn.type = "button";
                        scenario_dd_btn.setAttribute("data-toggle", "dropdown");
                        scenario_dd_btn.setAttribute("aria-haspopup", "true");
                        scenario_dd_btn.setAttribute("aria-expanded", "false");
                        // scenario_dd_btn.innerHTML = "";

                        let scenario_dd_btn_click_count = 0;
                        scenario_dd_btn.addEventListener("click", function () {

                            scenario_dropdown_container_div.classList.toggle("show");

                            scenario_dd_btn_click_count++;
                            if (scenario_dd_btn_click_count <= 1) {
                                scenario_dropdown_container_div.classList.add("show");
                            } else {
                                // scenario_dropdown_container_div.classList.remove("show");
                                scenario_dd_btn_click_count = 0;
                            }
                        });

                        scenario_dd_span.classList.add("sr-only");

                        scenario_dropdown_container_div.classList.add("dropdown-menu", "dropdown-menu-right", "container", "dropdown_menu", "scenario_dropdown_menu", "keep-open");
                        scenario_dropdown_container_div.id = scenarios[c]["name"] + "_container_div";

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
                                    let position_info = {
                                        "name": position.getAttribute("data-position-name"), "cartesian_coords": JSON.parse("[" + position.getAttribute("data-cartesian-coords") + "]"),
                                        "polar_params": {
                                            "coords": JSON.parse("[" + position.getAttribute("data-polar-coords") + "]"), "delays": JSON.parse("[" + position.getAttribute("data-polar-delays") + "]"),
                                            "divide_counts": JSON.parse("[" + position.getAttribute("data-polar-divide-counts") + "]")
                                        }
                                    };

                                    let existing_positions = scenarios[c]["positions"];
                                    existing_positions.push(position_info);

                                    let data = {"name": scenario_btn.innerHTML, "positions": existing_positions};

                                    request_asynchronous('/api/scenario?db=' + action_db_name + '&id=' + scenarios[c]["id"] + '&admin_id=' + admin_id + '&root=' + allow_root, 'PUT',
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

                            let position_context_menu = document.createElement('div');
                            let position_cm_remove_a = document.createElement('a');

                            position_div.classList.add("dropdown-item", "draggable_position", "drag-drop", "position_of_scenario");
                            position_div.setAttribute("data-position-name", scenarios[c]["positions"][i]["name"]);
                            position_div.setAttribute("data-cartesian-coords", scenarios[c]["positions"][i]["cartesian_coords"]);
                            position_div.setAttribute("data-polar-coords", scenarios[c]["positions"][i]["polar_params"]["coords"]);
                            position_div.setAttribute("data-polar-delays", scenarios[c]["positions"][i]["polar_params"]["delays"]);
                            position_div.setAttribute("data-polar-divide-counts", scenarios[c]["positions"][i]["polar_params"]["divide_counts"]);

                            position_span.classList.add("cut-text");
                            position_span.innerHTML = scenarios[c]["positions"][i]["name"];
                            position_span.title = scenarios[c]["positions"][i]["name"];
                            position_span.id = scenarios[c]["name"] + "_" + scenarios[c]["positions"][i]["name"] + "_span_" + i;

                            function hide_position_context_menu() {
                                $("#" + position_context_menu.id).removeClass("show").hide();
                                document.removeEventListener("click", hide_context_menu);
                            }

                            interact('#' + position_span.id)
                                .on('tap', function (event) {

                                    if (!position_context_menu.classList.contains("show")) {
                                        position_div.removeChild(position_span);

                                        let position_input = document.createElement('input');

                                        position_input.type = "text";
                                        position_input.placeholder = position_span.innerHTML;
                                        position_input.classList.add("action_name_input", "scenario_position_input");

                                        position_input.addEventListener("focusout", function () {
                                            if (position_input.value !== position_span.innerHTML && position_input.value !== "") {

                                                scenarios[c]["positions"][i]["name"] = position_input.value;
                                                let data = {"name": scenarios[c]["name"], "positions": scenarios[c]["positions"]};

                                                request_asynchronous('/api/scenario?db=' + action_db_name + '&id=' + scenarios[c]["id"] + '&admin_id=' + admin_id + '&root=' + allow_root, 'PUT',
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
                                        position_input.focus();
                                    }
                                })
                                .on('doubletap', function (event) {
                                })
                                .on('hold', function (event) {
                                    position_span.classList.add("disable_pointer");

                                    let target = event.target;
                                    let x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
                                    let y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

                                    position_context_menu.setAttribute('data-x', x);
                                    position_context_menu.setAttribute('data-y', y);

                                    $("#" + position_context_menu.id).css({
                                        display: "block",
                                        transform: 'translate(' + x + 'px, ' + y + 'px)',
                                    }).addClass("show");

                                    setTimeout(function () {
                                        position_span.classList.remove("disable_pointer");
                                        document.addEventListener("click", hide_position_context_menu);
                                    }, 500);

                                    return false; //blocks default WebBrowser right click menu
                                })
                                .on('down', function (event) {
                                })
                                .on('up', function (event) {
                                });

                            position_context_menu.classList.add("position-relative", "dropdown-menu", "dropdown-menu-sm");
                            position_context_menu.id = scenarios[c]["name"] + "_" + scenarios[c]["positions"][i]["name"] + "context-menu_" + i;

                            $("#" + position_context_menu.id + " a").on("click", function () {
                                $(this).parent().removeClass("show").hide();
                            });

                            position_cm_remove_a.classList.add("dropdown-item");
                            position_cm_remove_a.innerHTML = translate_text_item("remove");

                            position_cm_remove_a.addEventListener("click", function () {
                                JSalert(translate_text_item("Position Deleting!"),
                                    translate_text_item("You are about to delete this scenario's position: ") + "\n" + scenarios[c]["positions"][i]["name"],
                                    translate_text_item("OK"), translate_text_item("CANCEL"), function () {
                                        scenarios[c]["positions"].splice(i, 1);
                                        let data = {"name": scenarios[c]["name"], "positions": scenarios[c]["positions"]};
                                        request_asynchronous('/api/scenario?db=' + action_db_name + '&id=' + scenarios[c]["id"] + '&admin_id=' + admin_id + '&root=' + allow_root, 'PUT',
                                            'application/json; charset=UTF-8', data, function (req, err, response) {
                                                if (err === "success") {
                                                    let response_data = JSON.parse(response.responseText);
                                                }
                                            });
                                    });
                            });

                            position_context_menu.appendChild(position_cm_remove_a);

                            position_div.appendChild(position_span);
                            position_div.appendChild(position_context_menu);

                            scenario_dropdown_container_div.appendChild(position_div);
                        }

                        scenario_context_menu.appendChild(scenario_cm_remove_a);
                        scenario_context_menu.appendChild(scenario_cm_rename_a);
                        scenario_context_menu.appendChild(scenario_cm_advanced_a);

                        scenario_dd_btn.appendChild(scenario_dd_span);

                        scenario_dropdown_div.appendChild(scenario_btn);
                        scenario_dropdown_div.appendChild(scenario_dd_btn);
                        scenario_dropdown_div.appendChild(scenario_dropdown_container_div);
                        scenario_dropdown_div.appendChild(scenario_context_menu);

                        scenario_list_ul.appendChild(scenario_dropdown_div);
                    }
                }

            }
        });
});

controlling_template_sidebar_close_btn.addEventListener("click", function () {
    controlling_template_sidebar.classList.toggle("active");
    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    show_element(controlling_template_content);

    setSwiperSwiping(true);
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
                data = {
                    "name": position.getAttribute("data-position-name"), "cartesian_coords": JSON.parse("[" + position.getAttribute("data-cartesian-coords") + "]"),
                    "polar_params": {
                        "coords": JSON.parse("[" + position.getAttribute("data-polar-coords") + "]"), "delays": JSON.parse("[" + position.getAttribute("data-polar-delays") + "]"),
                        "divide_counts": JSON.parse("[" + position.getAttribute("data-polar-divide-counts") + "]")
                    }
                };

                request_asynchronous('/api/position?db=' + action_db_name + '&admin_id=' + admin_id + '&root=' + allow_root, 'POST',
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
        event.target.classList.remove('actions-drop-active');
        event.target.classList.remove('actions-drop-target');
        event.relatedTarget.classList.remove('action-can-drop');
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

            setSwiperSwiping(false);

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

            setSwiperSwiping(true);

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

// prismatic_menu_control_input.disabled = true;     // Todo: prismatic control is a broken point. Solve this.
prismatic_menu_control_input.addEventListener("change", function () {
    prismatic_control_div.classList.toggle("focused");
    rotational_control_div.classList.toggle("hidden_element");

    prismatic_menu_control_label.classList.toggle("fa-arrows-alt");
    prismatic_menu_control_label.classList.toggle("fa-times");

    if (prismatic_menu_control_input.checked) {
        setSwiperSwiping(false);
    } else {
        setSwiperSwiping(true);
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
        setSwiperSwiping(false);

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
                            arm_joint_right_btn.innerHTML = translate_text_item("j-") + joint_number + " ";

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
                            arm_joint_left_btn.innerHTML = translate_text_item("j-") + joint_number + " ";

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
    } else {
        setSwiperSwiping(true);
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

        setSwiperSwiping(false);

        record_pos_sce_btn.innerHTML = translate_text_item("cancel");

        current_arm_position = {};

        request_asynchronous('/api/move?admin_id=' + admin_id, 'GET',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
                if (err === "success") {
                    if (requested_data["status"] === "OK") {

                        current_arm_position = requested_data["data"];
                        console.log(requested_data["data"]);
                        console.log(typeof requested_data["data"]);
                    }
                }
            });

    } else {
        record_pos_sce_btn.innerHTML = translate_text_item("save");
        position_div_back_btn.click();
        scenario_div_back_btn.click();

        setSwiperSwiping(true);

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

    let delays = [];
    let divide_counts = [];

    for (let i = 0; i < current_arm_position["polar_coords"].length; i++) {
        delays.push(0);
        divide_counts.push(1);
    }

    data = {"name": position_name_input.value, "cartesian_coords": current_arm_position["cartesian_coords"], "polar_params": {"coords": current_arm_position["polar_coords"], "delays": delays, "divide_counts": divide_counts}};

    console.log(data);

    request_asynchronous('/api/position?db=' + action_db_name + '&admin_id=' + admin_id + '&root=' + allow_root, 'POST',
        'application/json; charset=UTF-8', data, function (req, err, response) {
            if (err === "success") {
                let response_data = JSON.parse(response.responseText);
                swal(translate_text_item("Position Created!"), "", "success");
            }
        });

    position_name_input.value = "";
    position_div_back_btn.click();
    record_pos_sce_btn.click();

});

record_in_sce_btn.addEventListener("click", function () {
    pos_sce_select_div.classList.add("inactive");
    create_sce_btn.disabled = true;

    setTimeout(function () {
        record_in_scenario_div.classList.add("focused");
    }, 175);

    clearElement(record_in_scenario_list_ul);

    request_asynchronous('/api/scenario?db=' + action_db_name + '&admin_id=' + admin_id + '&root=' + allow_root, 'GET',
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

                            request_asynchronous('/api/scenario?db=' + action_db_name + "&id=" + scenarios[i]["id"] + '&admin_id=' + admin_id + '&root=' + allow_root, 'PUT',
                                'application/json; charset=UTF-8', scenarios[i], function (req, err, response) {
                                    if (err === "success") {
                                        let response_data = JSON.parse(response.responseText);
                                        swal(translate_text_item("Position Added in Scenario: ") + scenarios[i]["name"], "", "success");
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

    let delays = [];
    let divide_counts = [];

    for (let i = 0; i < current_arm_position["polar_coords"].length; i++) {
        delays.push(0.2);
        divide_counts.push(1);
    }

    let position = {"name": "position_1", "cartesian_coords": current_arm_position["cartesian_coords"], "polar_params": {"coords": current_arm_position["polar_coords"], "delays": delays, "divide_counts": divide_counts}};

    let data = {"name": scenario_name_input.value, "positions": [position]};

    request_asynchronous('/api/scenario?db=' + action_db_name + '&admin_id=' + admin_id + '&root=' + allow_root, 'POST',
        'application/json; charset=UTF-8', data, function (req, err, response) {
            console.log(response.responseText);
            if (err === "success") {
                let response_data = JSON.parse(response.responseText);
                swal(translate_text_item("Position Added in New Scenario!"), "", "success");
            }
        });

    scenario_name_input.value = "";
    scenario_div_back_btn.click();
    record_pos_sce_btn.click();
});
