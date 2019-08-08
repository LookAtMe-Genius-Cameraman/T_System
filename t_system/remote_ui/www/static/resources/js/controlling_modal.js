// -*- coding: utf-8 -*-

/**
 * @module controlling_modal
 * @fileoverview the top-level module of T_System that contains controlling methods of data that is coming from T_System.
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 * @version 0.0.1
 */

// /**
//  *Add one or more listeners to an element
//  * @param {Element} element - DOM element to add listeners to
//  * @param {string} eventNames - space separated list of event names, e.g. 'click change'
//  * @param {Function} listener - function to attach for each event as a listener
//  */
// function add_multiple_listener(element, eventNames, listener) {
//   var events = eventNames.split(' ');
//   for (var i=0, iLen=events.length; i<iLen; i++) {
//     element.addEventListener(events[i], listener, false);
//   }
// }

// add_multiple_listener(window, 'mousemove touchmove', function(){…});


const main_container = document.getElementById("main_container");
const dark_deep_background_div = document.getElementById("dark_deep_background_div");

const video_area_div = document.getElementById("video_area_div");
const get_preview_span = document.getElementById("get_preview_span");
const stream_area_video = document.getElementById("stream_area_video");
const stream_area_video_source = document.getElementById("stream_area_video_source");

const motion_control_div = document.getElementById("motion_control_div");

const prismatic_control_div = document.getElementById("prismatic_control_div");
const prismatic_motion_control_btn = document.getElementById("prismatic_motion_control_btn");
const joint_1_cw_btn = document.getElementById("joint_1_cw_btn");
const joint_2_cw_btn = document.getElementById("joint_2_cw_btn");
const joint_3_cw_btn = document.getElementById("joint_3_cw_btn");
const joint_1_ccw_btn = document.getElementById("joint_1_ccw_btn");
const joint_2_ccw_btn = document.getElementById("joint_2_ccw_btn");
const joint_3_ccw_btn = document.getElementById("joint_3_ccw_btn");

const rotational_control_div = document.getElementById("rotational_control_div");
const x_up_btn = document.getElementById("x_up_btn");
const y_up_btn = document.getElementById("y_up_btn");
const z_up_btn = document.getElementById("z_up_btn");
const x_down_btn = document.getElementById("x_down_btn");
const y_down_btn = document.getElementById("y_down_btn");
const z_down_btn = document.getElementById("z_down_btn");

const rotational_motion_control_btn = document.getElementById("rotational_motion_control_btn");

const body = document.getElementsByTagName("BODY")[0];



// video_area_div.addEventListener("mouseover", function () {
//
//     get_preview_span.style.color = "#008CBA";
//
// });

stream_area_video.addEventListener("mouseover", function () {

    get_preview_span.style.color = "#008CBA";

});

stream_area_video.addEventListener("mouseout", function () {

    get_preview_span.style.color = "#000000";

});


function focus_video_area() {
    stream_area_video.removeEventListener("click", focus_video_area);
    stream_area_video.addEventListener("click", unfocus_video_area);

    start_stream("preview");

    let timer_settings_cont = setInterval(function () {

        if (requested_data !== undefined) {
            if (requested_data["status"] === "OK") {

                console.log(requested_data["data"] + "gşlrdmöfv");
                stream_area_video_source.src = requested_data["data"];

                dark_deep_background_div.style.opacity = "1";
                stream_area_video.classList.add("focused_video_area");
                video_area_div.style.margin = "-18% auto 0";
                show_element(motion_control_div);

                requested_data = undefined;
                clearInterval(timer_settings_cont)
            }
        }
    }, 300);


    // dark_deep_background_div.style.opacity = "1";
    // stream_area_video.classList.add("focused_video_area");
    // video_area_div.style.margin = "-30% auto";
    // show_element(motion_control_div);


}

function unfocus_video_area() {
    stream_area_video.removeEventListener("click", unfocus_video_area);
    stream_area_video.addEventListener("click", focus_video_area);

    stop_stream("preview");
    dark_deep_background_div.style.opacity = "0";
    stream_area_video.classList.remove("focused_video_area");
    video_area_div.style.margin = "30%  auto";
    hide_element(motion_control_div);
    hide_element(prismatic_control_div);
    hide_element(rotational_control_div);

}

function toggleFullScreen(){
	if(stream_area_video.requestFullScreen){
		stream_area_video.requestFullScreen();
	} else if(stream_area_video.webkitRequestFullScreen){
		stream_area_video.webkitRequestFullScreen();
	} else if(stream_area_video.mozRequestFullScreen){
		stream_area_video.mozRequestFullScreen();
	}
}

stream_area_video.addEventListener("click", focus_video_area);
stream_area_video.addEventListener("dblclick", toggleFullScreen);

prismatic_motion_control_btn.addEventListener("click", function () {
    hide_element(prismatic_motion_control_btn);
    show_element(rotational_motion_control_btn);

    show_element(rotational_control_div);
    rotational_control_div.style.top = "-280px";
    hide_element(prismatic_control_div);
    prismatic_control_div.style.top = "75%";


});

rotational_motion_control_btn.addEventListener("click", function () {
    hide_element(rotational_motion_control_btn);
    show_element(prismatic_motion_control_btn);

    hide_element(rotational_control_div); // when prismatic button clicked rotational modal showing because rotational modal's button become visible via prismatic's hover.
    rotational_control_div.style.top = "-20%";
    show_element(prismatic_control_div);
    prismatic_control_div.style.top = "-45%";

});

/**
 * The high-level method of getting specified network information with its ssid or the all existing network information.
 * It is triggered via a click on settings_btn or clicked specified network on network list.
 */
function start_stream(type) {

        // console.log("bla");
        // console.log(response);
        jquery_manager.get_data("/api/stream?type=" + type + "&admin_id=" + admin_id);

}

function stop_stream(type) {
            jquery_manager.delete_data("/api/stream?type=" + type + "&admin_id=" + admin_id);

}



