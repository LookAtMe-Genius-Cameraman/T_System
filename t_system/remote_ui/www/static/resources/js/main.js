// -*- coding: utf-8 -*-

/**
 * @module main
 * @fileoverview the top-level module of T_System that contains the communication methods with python flask of T_System.
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 */

/** @type {!Object} */
const jquery_manager = JQueryManager;


/** @type {!Element} */
const control_btn = document.getElementById("control_btn");
const settings_btn = document.getElementById("settings_btn");
const on_work_btn = document.getElementById("on_work_btn");


/** @type {!Element} */
// const swiper = document.querySelector(".swiper-container");
const controlling_template_container = document.getElementById("controlling_template_container");
const settings_template_container = document.getElementById("settings_template_container");
const on_work_template_container = document.getElementById("on_work_template_container");


/**
 * The low-level method to create drop-down language selection menu.
 */
function build_language_menu() {
    let content = "";
    for (let lang_i = 0; lang_i < language_list.length; lang_i++) {
        content += "<a href='#' onclick=\"translate_text('";
        content += language_list[lang_i][0];
        content += "'); update_ui_text();\"><span >";
        content += language_list[lang_i][1];
        content += "</span><span class=\"clearfix\"></span></a>";
        if (language_list[lang_i][0] === language) {
            document.getElementById("translate_menu").innerHTML = language_list[lang_i][1];
        }
    }
    document.getElementById("lang_menu").innerHTML = content;
}


function update_ui_text() {
    build_HTML_setting_list(current_setting_filter);
}

function toggle_elements(elements) {
    for (let i = 0; i < elements.length; i++) {
        elements[i].classList.toggle("hidden_element")
    }
}

/**
 * The low-level method to change visibility and opacity for making usable of given element.
 * @param {Object} element: the route address of the flask
 */
function show_element(element) {
    element.style.opacity = "1";
    element.style.visibility = "visible";
}


/**
 * The low-level method to change visibility and opacity for making unusable of given element.
 * @param {Object} element: the route address of the flask
 */
function hide_element(element) {
    element.style.opacity = "0";
    element.style.visibility = "hidden";
}


/**
 * The method to reload the page.
 */
function refresh_page() {
    window.location.reload();
}


// window.onload = function () {
//
// };

let swiper;
$(document).ready(function () {
    //to check if javascript is disabled like in anroid preview
    // document.getElementById('warningmsg').style.display = 'none';
    connectdlg();

    swiper = new Swiper('.swiper-container', {
        effect: 'cube',
        grabCursor: true,
        cubeEffect: {
            shadow: true,
            slideShadows: true,
            shadowOffset: 20,
            shadowScale: 0.94,
        },
        pagination: {
            el: '.swiper-pagination',
        },
    });

    on_work_btn.click()

});


settings_btn.addEventListener("click", function () {
    swiper.slideTo(0)
});


control_btn.addEventListener("click", function () {
    swiper.slideTo(1)
});


on_work_btn.addEventListener("click", function () {
    swiper.slideTo(2)
});
