// -*- coding: utf-8 -*-

/**
 * @module main
 * @fileoverview the top-level module of T_System that contains the communication methods with python flask of T_System.
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 */

/** @type {!Element} */
const body = document.getElementsByTagName("BODY")[0];

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

const dark_deep_background_div = document.getElementById("dark_deep_background_div");


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

function activateAdminAuthorityBy(admin_id) {
    if (admin_id !== false) {
        administration_template_container.classList.add("active");
        toggle_controlling_modal(true);
    } else {
        administration_template_container.classList.remove("active");
        toggle_controlling_modal(false);
    }
}

/**
 * Method to remove all children elements of given element.
 * @param {Object} element: the route address of the flask
 */
function clearElement(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

/**
 * Method to change swipeablity of swiper element.
 * @param {boolean} is_active: swipeablity flag
 */
function setSwiperSwiping(is_active) {
    swiper.allowSlideNext = is_active;
    swiper.allowSlidePrev = is_active;
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


function set_language_processes() {
    let value = get_localdata('language');
    if (String(value).length === 0 || String(value) === "null") value = "en";
    build_language_menu();
    translate_text(value, lang_select_dd_btn);
}

let swiper;

function init_swiper() {
    swiper = new Swiper('.swiper-container', {
        effect: 'coverflow',
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
}

function toggle_controlling_modal(activate = false) {
    swiper.destroy(true, true);

    if (activate) {
        page_control_div.removeChild(prepare_btn);
        page_control_div.appendChild(control_btn);
        page_control_div.appendChild(prepare_btn);

        swiper_wrapper.removeChild(prepare_template_container);
        swiper_wrapper.appendChild(controlling_template_container);
        swiper_wrapper.appendChild(prepare_template_container);

    } else {
        page_control_div.removeChild(control_btn);
        swiper_wrapper.removeChild(controlling_template_container);
    }

    init_swiper();
}



$(document).ready(function () {
    initial_loading_div.classList.add("inactive");
    loading_animation_div.classList.remove("lds-dual-ring");

    set_language_processes();

    init_swiper();

    control_btn.click();

    document.addEventListener("contextmenu", function (e) {
        e.preventDefault();
    }, false);

    no_mark_checkbox.click();
    toggle_controlling_modal(false);

    if (!ss_switch_checkbox.checked) {
        console.log("something_wrong");
        ss_switch_checkbox.click();
    }
});

title_footer.addEventListener("click", function (e) {
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
