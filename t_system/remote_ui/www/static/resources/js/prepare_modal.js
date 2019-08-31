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