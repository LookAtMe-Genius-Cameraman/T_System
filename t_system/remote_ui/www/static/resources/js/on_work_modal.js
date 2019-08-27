const on_work_job_btn = document.getElementById("on_work_job_btn");
const on_work_cancel_btn = document.getElementById("on_work_cancel_btn");

const monitor_area_div = document.getElementById("monitor_area_div");

const main_specify_div = document.getElementById("main_specify_div");

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


let on_work_job_btn_click_count = 0;


on_work_job_btn.addEventListener("click", function () {
    on_work_job_btn_click_count++;
    if (on_work_job_btn_click_count <= 1) {
        on_work_job_btn.innerHTML = "START";
        on_work_job_btn.classList.toggle("ready");
        on_work_job_btn.classList.toggle("btn-warning");
        on_work_job_btn.classList.toggle("btn-danger");

        on_work_cancel_btn.classList.toggle("active");

        main_specify_div.classList.toggle("hidden_element_without_child");
        // main_specify_div.style.visibility = "hidden";
        dark_deep_background_div.classList.toggle("focused");

        shine_checked_boxes([ai_select_checkbox, security_mode_checkbox, non_moving_target_checkbox, time_laps_checkbox])

    } else if (on_work_job_btn_click_count <= 2) {
        on_work_job_btn.innerHTML = "STOP";
        on_work_job_btn.classList.toggle("ready");
        on_work_job_btn.classList.toggle("btn-danger");
        on_work_job_btn.classList.toggle("btn-dark");

        on_work_cancel_btn.classList.toggle("active");

        monitor_area_div.classList.toggle("focused");

        shine_checked_boxes([ai_select_checkbox, security_mode_checkbox, non_moving_target_checkbox, time_laps_checkbox])

    } else {
        on_work_job_btn.innerHTML = "READY";
        on_work_job_btn.classList.toggle("btn-dark");
        on_work_job_btn.classList.toggle("btn-warning");
        dark_deep_background_div.classList.toggle("focused");

        main_specify_div.classList.toggle("hidden_element_without_child");
        monitor_area_div.classList.toggle("focused");

        on_work_job_btn_click_count = 0;
    }
});


on_work_cancel_btn.addEventListener("click", function () {
    on_work_cancel_btn.classList.toggle("active");

    on_work_job_btn.innerHTML = "READY";
    on_work_job_btn.classList.toggle("ready");
    on_work_job_btn.classList.toggle("btn-danger");
    on_work_job_btn.classList.toggle("btn-warning");
    dark_deep_background_div.classList.toggle("focused");

    main_specify_div.classList.toggle("hidden_element_without_child");

    shine_checked_boxes([ai_select_checkbox, security_mode_checkbox, non_moving_target_checkbox, time_laps_checkbox]);


    on_work_job_btn_click_count = 0
});