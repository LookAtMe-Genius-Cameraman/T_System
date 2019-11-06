const administration_template_container = document.getElementById("administration_template_container");
const administration_header_div = document.getElementById("administration_header_div");
const administration_btn = document.getElementById("administration_btn");
const administration_btn_i = document.getElementById("administration_btn_i");
const administration_selected_task_div = document.getElementById("administration_selected_task_div");
const administration_div = document.getElementById("administration_div");

const create_emotion_checkbox = document.getElementById("create_emotion_checkbox");
const create_emotion_cb_label = document.getElementById("create_emotion_cb_label");

const predict_mission_checkbox = document.getElementById("predict_mission_checkbox");
const predict_mission_cb_label = document.getElementById("predict_mission_cb_label");

function show_selected_tasks(elements, dest) {
    selected_spans = [];


    let labels = document.getElementsByTagName('label');

    for (let i = 0; i < elements.length; i++) {
        if (elements[i].checked) {
            for (let a = 0; a < labels.length; a++) {
                if (labels[a].htmlFor === elements[i].id) {

                    let selected_div = document.createElement('div');
                    let selected_span = document.createElement('span');

                    selected_div.classList.add("position-relative", "mb-1");

                    selected_span.innerHTML = labels[a].innerHTML;
                    selected_span.classList.toggle("administrator_selected_shine");

                    selected_div.appendChild(selected_span);
                    dest.appendChild(selected_div);

                    selected_spans.push(selected_span);
                }
            }
        }
    }
}

function toggle_administration_modal() {
    administration_template_container.classList.toggle("focused");
    administration_header_div.classList.toggle("clicked");
    administration_selected_task_div.classList.toggle("mr-2");
    administration_btn.classList.toggle("clicked");
    administration_btn.classList.toggle("ml-2");
    administration_div.classList.toggle("focused");

    if (administration_div.classList.contains("focused")) {  // 1. click
        if (dark_overlay_active) {
            dark_overlay_active = false
        } else {
            dark_deep_background_div.classList.toggle("focused");
            dark_overlay_active = true
        }

        administration_btn_i.innerHTML = translate_text_item(" administration");
        clearElement(administration_selected_task_div);

    } else {  // 2. click
        if (dark_overlay_active === false) {
            dark_overlay_active = true

        } else {
            dark_deep_background_div.classList.toggle("focused");
            dark_overlay_active = false
        }

        administration_btn_i.innerHTML = "";
        show_selected_tasks([create_emotion_checkbox, predict_mission_checkbox], administration_selected_task_div);
    }

    options_template_container.classList.toggle("hidden_element");
    controlling_template_container.classList.toggle("hidden_element");
    prepare_template_container.classList.toggle("hidden_element");
    system_info_template_container.classList.toggle("hidden_element");
    job_template_container.classList.toggle("hidden_element");
    page_control_div.classList.toggle("hidden_element");

}

administration_btn.addEventListener("click", toggle_administration_modal);

administration_div.addEventListener("click", function (event) {
    if (event.target === event.currentTarget) {
        toggle_administration_modal()
    } else {
    }
});


create_emotion_checkbox.addEventListener("change", function () {
    predict_mission_cb_label.disabled = predict_mission_checkbox.disabled = create_emotion_checkbox.checked;
    predict_mission_checkbox.checked = false;

    if (create_emotion_checkbox.checked) {
        request_asynchronous('/api/move?expand=true' + '&admin_id=' + admin_id, 'POST',
        'application/x-www-form-urlencoded; charset=UTF-8', {}, function (req, err, response) {
            if (err === "success") {
                let response_data = JSON.parse(response.responseText);
            }
        });

        action_db_name = "emotions";
        allow_root = true;
        console.log("checked");
    } else {
        request_asynchronous('/api/move?expand=false' + '&admin_id=' + admin_id, 'POST',
        'application/x-www-form-urlencoded; charset=UTF-8', {}, function (req, err, response) {
            if (err === "success") {
                let response_data = JSON.parse(response.responseText);
            }
        });

        action_db_name = "missions";
        allow_root = false;
    }
});


predict_mission_checkbox.addEventListener("change", function () {
    create_emotion_cb_label.disabled = create_emotion_checkbox.disabled = predict_mission_checkbox.checked;
    create_emotion_checkbox.checked = false;

    if (predict_mission_checkbox.checked) {
        action_db_name = "predicted_missions";
        allow_root = true;
    } else {
        action_db_name = "missions";
        allow_root = false;
    }
});