// -*- coding: utf-8 -*-

/**
 * @module main
 * @fileoverview the top-level module of T_System that contains the communication methods with python flask of T_System.
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 */

/** @type {!Element} */
const body = document.getElementsByTagName("BODY")[0];

/** @type {!Object} */
const jquery_manager = JQueryManager;


const initial_loading_div = document.getElementById("initial_loading_div");
const loading_animation_div = document.getElementById("loading_animation_div");

const swiper_wrapper = document.getElementById("swiper_wrapper");

const title_footer = document.getElementById("title_footer");

/** @type {!Element} */
const page_control_div = document.getElementById("page_control_div");
const control_btn = document.getElementById("control_btn");
const options_btn = document.getElementById("options_btn");
const prepare_btn = document.getElementById("prepare_btn");


/** @type {!Element} */
// const swiper = document.querySelector(".swiper-container");
const controlling_template_container = document.getElementById("controlling_template_container");
const options_template_container = document.getElementById("options_template_container");
const prepare_template_container = document.getElementById("prepare_template_container");


/**
 * Method to create drop-down language selection menu.
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
 * Method to change visibility and opacity for making usable of given element.
 * @param {Object} element: the route address of the flask
 */
function show_element(element) {
    element.style.opacity = "1";
    element.style.visibility = "visible";
}


/**
 * Method to change visibility and opacity for making unusable of given element.
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

function dragMoveListener(event) {
    let target = event.target;
    // keep the dragged position in the data-x/data-y attributes
    let x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
    let y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

    // translate the element
    target.style.webkitTransform =
        target.style.transform =
            'translate(' + x + 'px, ' + y + 'px)';

    // update the posiion attributes
    target.setAttribute('data-x', x);
    target.setAttribute('data-y', y);
}

// this is used later in the resizing and gesture demos
window.dragMoveListener = dragMoveListener;


function resize_image(src, max_width, max_height, dest_element) {
    let img = new Image();
    img.src = src;

    let canvas = document.createElement("canvas");
    img.onload = function () {

        let width = img.width;
        let height = img.height;

        if (width > height) {
            if (width > max_width) {
                height *= max_width / width;
                width = max_width;
            }
        } else {
            if (height > max_height) {
                width *= max_height / height;
                height = max_height;
            }
        }

        canvas.width = width;
        canvas.height = height;
        let ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);
        dest_element.src = canvas.toDataURL(img.type);
    };
}


let swiper;
$(document).ready(function () {
    initial_loading_div.classList.add("inactive");
    loading_animation_div.classList.remove("lds-dual-ring");

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

    control_btn.click();

    document.addEventListener("contextmenu", function (e) {
        e.preventDefault();
    }, false);

});

title_footer.addEventListener("click", function (e) {
   // window.open('https://github.com/connected-life/T_System', '_system');

   e.preventDefault();
  $('#title_footer_url_modal').modal('show').find('.modal-body').load('https://github.com/connected-life/T_System');
});


options_btn.addEventListener("click", function () {
    swiper.slideTo(0)
});


control_btn.addEventListener("click", function () {
    swiper.slideTo(1)
});


prepare_btn.addEventListener("click", function () {
    swiper.slideTo(2)
});
