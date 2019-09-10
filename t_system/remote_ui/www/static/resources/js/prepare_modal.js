const main_specify_div = document.getElementById("main_specify_div");

const specify_sce_div = document.getElementById("specify_sce_div");
const specify_param_div = document.getElementById("specify_param_div");

const specify_sce_span = document.getElementById("specify_sce_span");
const specify_param_span = document.getElementById("specify_param_span");

const available_sce_div = document.getElementById("available_sce_div");
const select_param_cb_div = document.getElementById("select_param_cb_div");

const ai_select_dd_div = document.getElementById("ai_select_dd_div");
const ai_select_dd_btn = document.getElementById("ai_select_dd_btn");


const ai_select_checkbox = document.getElementById("ai_select_checkbox");
const ai_select_cb_label = document.getElementById("ai_select_cb_label");
const security_mode_checkbox = document.getElementById("security_mode_checkbox");
const security_mode_cb_label = document.getElementById("security_mode_cb_label");
const non_moving_target_checkbox = document.getElementById("non_moving_target_checkbox");
const non_moving_target_cb_label = document.getElementById("non_moving_target_cb_label");
const time_laps_checkbox = document.getElementById("time_laps_checkbox");
const time_laps_cb_label = document.getElementById("time_laps_cb_label");

function shine_checked_boxes(elements) {

    let labels = document.getElementsByTagName('label');

    for (let i = 0; i < elements.length; i++) {
        if (elements[i].checked) {
            for (let a = 0; a < labels.length; a++) {
                if (labels[a].htmlFor === elements[i].id) {
                    labels[a].classList.toggle("shine_in_dark");
                }
            }
        }
    }
}

specify_sce_div.addEventListener("click", function (e) {

    if(e.target !== e.currentTarget) return;

    if (specify_sce_span.innerHTML === "") {
        specify_sce_span.innerHTML = "Specify Scenarios";
        specify_param_span.innerHTML = "";

        main_specify_div.classList.remove("center");
        main_specify_div.classList.remove("left");
        main_specify_div.classList.add("right");

        specify_sce_div.classList.add("focused");
        specify_param_div.classList.remove("focused");

        available_sce_div.classList.add("focused");
        select_param_cb_div.classList.remove("focused");
    }
    else {
        specify_sce_span.innerHTML = "";

        specify_sce_div.classList.remove("focused");

        main_specify_div.classList.remove("right");
        main_specify_div.classList.remove("left");
        main_specify_div.classList.add("center");

        available_sce_div.classList.remove("focused");
        select_param_cb_div.classList.remove("focused");
    }

});

specify_param_div.addEventListener("click", function (e) {

    if(e.target !== e.currentTarget) return;

    if (specify_param_span.innerHTML === "") {
        specify_param_span.innerHTML = "Specify Parameters";
        specify_sce_span.innerHTML = "";

        main_specify_div.classList.remove("center");
        main_specify_div.classList.remove("right");
        main_specify_div.classList.add("left");

        specify_param_div.classList.add("focused");
        specify_sce_div.classList.remove("focused");

        select_param_cb_div.classList.add("focused");
        available_sce_div.classList.remove("focused");
    }
    else {
        specify_param_span.innerHTML = "";
        specify_param_div.classList.remove("focused");

        main_specify_div.classList.remove("left");
        main_specify_div.classList.remove("right");
        main_specify_div.classList.add("center");

        select_param_cb_div.classList.remove("focused");
        available_sce_div.classList.remove("focused");
    }
});

specify_param_div.addEventListener("click", function (e) {
});