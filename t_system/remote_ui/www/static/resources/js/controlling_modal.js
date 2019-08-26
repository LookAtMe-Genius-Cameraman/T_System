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
const motion_control_btn = document.getElementById("motion_control_btn");

/** @type {!Element} */
const prismatic_control_div = document.getElementById("prismatic_control_div");
const joint_1_cw_btn = document.getElementById("joint_1_cw_btn");
const joint_2_cw_btn = document.getElementById("joint_2_cw_btn");
const joint_3_cw_btn = document.getElementById("joint_3_cw_btn");
const joint_1_ccw_btn = document.getElementById("joint_1_ccw_btn");
const joint_2_ccw_btn = document.getElementById("joint_2_ccw_btn");
const joint_3_ccw_btn = document.getElementById("joint_3_ccw_btn");

/** @type {!Element} */
const rotational_control_div = document.getElementById("rotational_control_div");
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

/** @type {!Element} */
const body = document.getElementsByTagName("BODY")[0];


function stop_stream(type) {
    jquery_manager.delete_data("/api/stream?type=" + type + "&admin_id=" + admin_id);

}

function get_current_position() {
    jquery_manager.get_data("/api/move?admin_id=" + admin_id);
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

        if (requested_data !== null) {
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
            requested_data = null;
            clearInterval(timer_settings_cont)
        }
    }, 300);

    get_scenario_s();

    timer_settings_cont = setInterval(function () {

        if (requested_data !== null) {
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
            requested_data = null;
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

video_area_div.addEventListener("click", function () {
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
});

video_area_div.addEventListener("dblclick", function () {
    	if(stream_area_img.requestFullScreen){
		stream_area_img.requestFullScreen();
	} else if(stream_area_img.webkitRequestFullScreen){
		stream_area_img.webkitRequestFullScreen();
	} else if(stream_area_img.mozRequestFullScreen){
		stream_area_img.mozRequestFullScreen();
	}
});

let motion_control_btn_click_count = 0;


motion_control_btn.addEventListener("click", function () {
    motion_control_btn_click_count++;
    if (motion_control_btn_click_count <= 1) {

        motion_control_btn.classList.toggle("first_clicked");

        show_element(rotational_control_div);
        rotational_control_div.style.top = "-225px";
        hide_element(prismatic_control_div);
        prismatic_control_div.style.top = "75%";

    } else if (motion_control_btn_click_count <= 2) {

        motion_control_btn.classList.toggle("first_clicked");
        motion_control_btn.classList.toggle("second_clicked");

        hide_element(rotational_control_div); // when prismatic button clicked rotational modal showing because rotational modal's button become visible via prismatic's hover.
        rotational_control_div.style.top = "-20%";
        show_element(prismatic_control_div);
        prismatic_control_div.style.top = "-20%";

    } else {

        motion_control_btn.classList.toggle("second_clicked");

        hide_element(rotational_control_div); // when prismatic button clicked rotational modal showing because rotational modal's button become visible via prismatic's hover.
        hide_element(prismatic_control_div);
        prismatic_control_div.style.top = "75%";

        motion_control_btn_click_count = 0;
    }
});

let record_pos_sce_btn_click_count = 0;

record_pos_sce_btn.addEventListener("click", function () {
    record_pos_sce_btn_click_count++;
    if (record_pos_sce_btn_click_count <= 1) {

        get_current_position();
        let timer_settings_cont = setInterval(function () {

            if (requested_data !== null) {
                if (requested_data["status"] === "OK") {

                    current_arm_position = requested_data["data"];
                    // console.log(requested_data["data"]);
                    record_pos_sce_btn.innerHTML = "cancel";

                    hide_element(motion_control_div);
                    hide_element(video_area_div);
                    hide_element(controlling_template_sidebar);
                    hide_element(sidebar_toggle_btn);
                }
                requested_data = null;
                clearInterval(timer_settings_cont)
            }
        }, 300);

    } else {
        record_pos_sce_btn.innerHTML = "save";

        show_element(motion_control_div);
        show_element(video_area_div);
        show_element(controlling_template_sidebar);
        show_element(sidebar_toggle_btn);
        record_pos_sce_btn_click_count = 0
    }
    dark_deep_background_div.classList.toggle("focused");
    record_pos_sce_div.classList.toggle("focused");
});


record_as_pos_btn.addEventListener("click", function () {
    pos_sce_select_div.classList.toggle("inactive");
    create_pos_btn.disabled = true;

    setTimeout(function () {
        record_as_position_div.classList.toggle("focused");
        }, 175)
});


position_div_back_btn.addEventListener("click", function () {
    record_as_position_div.classList.toggle("focused");
    setTimeout(function () {
        pos_sce_select_div.classList.toggle("inactive");
        }, 175)
});


position_name_input.addEventListener("mousemove", function () {
    create_pos_btn.disabled = position_name_input.value === "";
});


create_pos_btn.addEventListener("click", function () {

    let name_dict = {"name": position_name_input.value};
    let data = Object.assign({}, name_dict, current_arm_position);

    jquery_manager.post_data("/api/position&admin_id=" + admin_id, data);

    position_name_input.value = "";
    position_div_back_btn.click();
    record_pos_sce_btn.click();

    swal(translate_text_item("Position Created!"), "", "success");
});

record_in_sce_btn.addEventListener("click", function () {
    pos_sce_select_div.classList.toggle("inactive");

    setTimeout(function () {
        record_in_scenario_div.classList.toggle("focused");
        }, 175)
});

scenario_div_back_btn.addEventListener("click", function () {
    record_in_scenario_div.classList.toggle("focused");
    setTimeout(function () {
        pos_sce_select_div.classList.toggle("inactive");
        }, 175)
});



