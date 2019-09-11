const main_specify_div = document.getElementById("main_specify_div");

const specify_sce_div = document.getElementById("specify_sce_div");
const specify_sce_span = document.getElementById("specify_sce_span");
const available_sce_div = document.getElementById("available_sce_div");

const specify_param_div = document.getElementById("specify_param_div");
const specify_param_span = document.getElementById("specify_param_span");
const select_param_cb_div = document.getElementById("select_param_cb_div");

const recognize_checkbox = document.getElementById("recognize_checkbox");
const recognize_select_dd_div = document.getElementById("recognize_select_dd_div");
const recognize_select_dd_btn = document.getElementById("recognize_select_dd_btn");
const recognize_all_select_checkbox = document.getElementById("recognize-all_select_checkbox");
const recognize_person_list_ul = document.getElementById("recognize_person_list_ul");

const ai_checkbox = document.getElementById("ai_checkbox");
const ai_select_dd_div = document.getElementById("ai_select_dd_div");
const ai_select_dd_btn = document.getElementById("ai_select_dd_btn");
const official_ai_checkbox = document.getElementById("official_ai_checkbox");

const learn_mode_check_div = document.getElementById("learn_mode_check_div");

const security_mode_checkbox = document.getElementById("security_mode_checkbox");
const security_mode_cb_label = document.getElementById("security_mode_cb_label");
const learn_mode_checkbox = document.getElementById("learn_mode_checkbox");
const learn_mode_cb_label = document.getElementById("learn_mode_cb_label");
const non_moving_target_checkbox = document.getElementById("non_moving_target_checkbox");
const non_moving_target_cb_label = document.getElementById("non_moving_target_cb_label");
const time_laps_checkbox = document.getElementById("time_laps_checkbox");
const time_laps_cb_label = document.getElementById("time_laps_cb_label");


specify_sce_div.addEventListener("click", function (e) {

    if (e.target !== e.currentTarget) return;

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
    } else {
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

    if (e.target !== e.currentTarget) return;

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

        recognize_checkbox.click();
        ai_checkbox.click();
    } else {
        specify_param_span.innerHTML = "";
        specify_param_div.classList.remove("focused");

        main_specify_div.classList.remove("left");
        main_specify_div.classList.remove("right");
        main_specify_div.classList.add("center");

        select_param_cb_div.classList.remove("focused");
        available_sce_div.classList.remove("focused");
    }
});

let recognize_checkboxes = [];

recognize_checkboxes.push(recognize_all_select_checkbox);


function is_recognition_be_used() {
    for (let i = 0; i < recognize_checkboxes.length; i++) {
        if (recognize_checkboxes[i].checked) {
            return true;
        }
    }
    return false;
}

recognize_checkbox.addEventListener("change", function () {
    console.log("main recognize changed");
    if (is_recognition_be_used()) {
        time_laps_cb_label.disabled = time_laps_checkbox.disabled =
            non_moving_target_cb_label.disabled = non_moving_target_checkbox.disabled = true;

        time_laps_checkbox.checked =
            non_moving_target_checkbox.checked = false;

        recognize_checkbox.checked = true;

    } else {
        time_laps_cb_label.disabled = time_laps_checkbox.disabled =
            non_moving_target_cb_label.disabled = non_moving_target_checkbox.disabled = false;

        security_mode_checkbox.click();
        security_mode_checkbox.click();
        ai_checkbox.click();

        recognize_checkbox.checked = false;
    }
});

recognize_all_select_checkbox.addEventListener("change", function () {
        for (let c = 0; c < recognize_checkboxes.length; c++) {
            recognize_checkboxes[c].checked = recognize_all_select_checkbox.checked;
        }
        recognize_checkbox.click();
});

let date_btn_click_count = 0;
recognize_select_dd_btn.addEventListener("click", function () {

    date_btn_click_count++;

    while (recognize_person_list_ul.firstChild) {
        recognize_person_list_ul.removeChild(recognize_person_list_ul.firstChild);
    }

    requested_data = {"status": "OK", "data": [{"id": "z970136a-aegb-15e9-b130-cy2f756671ed", "name": "Face 1", "image_names": ["im-n1"]}, {"id": "z970163v-ayhb-17r9-b132-cy2f857471ed", "name": "Face 2", "image_names": ["im-n1"]}]};

    let recognize_select_interval = setInterval(function () {

            if (requested_data !== {}) {

                if (requested_data["status"] === "OK") {

                    for (let c = 0; c < requested_data["data"].length; c++) {

                        let recognize_select_div = document.createElement('div');
                        let recognize_select_checkbox = document.createElement('input');
                        let recognize_select_label = document.createElement('label');

                        recognize_select_div.classList.add("dropdown-item", "form-check", "mb-1");
                        // class="dropdown-item"

                        recognize_select_checkbox.classList.add("form-check-input");
                        recognize_select_checkbox.id = requested_data["data"][c]["id"];
                        recognize_select_checkbox.type = "checkbox";

                        let face_exist = false;

                        for(let i= 0; i < recognize_checkboxes.length; i++) {
                            if (recognize_checkboxes[i].id === recognize_select_checkbox.id) {
                                recognize_select_checkbox = recognize_checkboxes[i];
                                face_exist = true;
                                break;
                            }
                        }

                        if (!face_exist) {
                            recognize_checkboxes.push(recognize_select_checkbox);
                        }

                        recognize_select_checkbox.addEventListener("change", function () {
                            recognize_checkbox.click();
                        });

                        recognize_select_label.classList.add("form-check-label");
                        recognize_select_label.setAttribute("for", recognize_select_checkbox.id);
                        recognize_select_label.innerHTML = requested_data["data"][c]["name"];

                        recognize_select_div.appendChild(recognize_select_checkbox);
                        recognize_select_div.appendChild(recognize_select_label);

                        recognize_person_list_ul.appendChild(recognize_select_div);
                    }
                }
                requested_data = {};
                clearInterval(recognize_select_interval)
            }
        }
    );
});


let ai_checkboxes = [];

ai_checkboxes.push(official_ai_checkbox);

function is_ai_be_used() {
    for (let i = 0; i < ai_checkboxes.length; i++) {
        if (ai_checkboxes[i].checked) {
            return true;
        }
    }
    return false;
}

ai_checkbox.addEventListener("change", function () {
    console.log("main AI changed");
    if (is_ai_be_used()) {
        time_laps_cb_label.disabled = time_laps_checkbox.disabled =
            non_moving_target_cb_label.disabled = non_moving_target_checkbox.disabled =
                security_mode_cb_label.disabled = security_mode_checkbox.disabled = true;

        learn_mode_cb_label.disabled = learn_mode_checkbox.disabled = false;

        time_laps_checkbox.checked =
            non_moving_target_checkbox.checked =
                security_mode_checkbox.checked = false;

        ai_checkbox.checked = true;

    } else {
        time_laps_cb_label.disabled = time_laps_checkbox.disabled =
            non_moving_target_cb_label.disabled = non_moving_target_checkbox.disabled =
                    security_mode_cb_label.disabled = security_mode_checkbox.disabled = false;

        learn_mode_cb_label.disabled = learn_mode_checkbox.disabled = true;

        learn_mode_checkbox.checked =
            ai_checkbox.checked = false;
    }
});

official_ai_checkbox.addEventListener("change", function () {
        ai_checkbox.click();
});


security_mode_checkbox.addEventListener("change", function () {

    time_laps_cb_label.disabled = time_laps_checkbox.disabled =
        non_moving_target_cb_label.disabled = non_moving_target_checkbox.disabled =
            learn_mode_cb_label.disabled = learn_mode_checkbox.disabled =
                ai_select_dd_btn.disabled = ai_checkbox.disabled = security_mode_checkbox.checked;

    time_laps_checkbox.checked =
        non_moving_target_checkbox.checked =
            learn_mode_checkbox.checked =
                ai_checkbox.checked = false;

    ai_checkbox.click();
});

learn_mode_checkbox.addEventListener("change", function () {

    time_laps_checkbox.checked =
        non_moving_target_checkbox.checked =
            security_mode_checkbox.checked = false;
});

non_moving_target_checkbox.addEventListener("change", function () {

    time_laps_cb_label.disabled = time_laps_checkbox.disabled =
        learn_mode_cb_label.disabled = learn_mode_checkbox.disabled =
                security_mode_cb_label.disabled = security_mode_checkbox.disabled =
                    ai_select_dd_btn.disabled = ai_checkbox.disabled =
                        recognize_select_dd_btn.disabled = recognize_checkbox.disabled = non_moving_target_checkbox.checked;

    time_laps_checkbox.checked =
        learn_mode_checkbox.checked =
            security_mode_checkbox.checked =
                ai_select_dd_btn.checked =
                    recognize_select_dd_btn.checked = false;

    recognize_checkbox.click();
    ai_checkbox.click();
});

