const job_template_container = document.getElementById("job_template_container");
const job_btn = document.getElementById("job_btn");
const job_btn_i = document.getElementById("job_btn_i");
const job_div = document.getElementById("job_div");

const selected_sce_span = document.getElementById("selected_sce_span");
const selected_scenarios_div = document.getElementById("selected_scenarios_div");

const selected_param_span = document.getElementById("selected_param_span");
const selected_params_div = document.getElementById("selected_params_div");

const job_simulate_btn = document.getElementById("job_simulate_btn");
const job_ready_btn = document.getElementById("job_ready_btn");
const job_cancel_btn = document.getElementById("job_cancel_btn");

const mark_target_dd_btn = document.getElementById("mark_target_dd_btn");
const no_mark_div = document.getElementById("no_mark_div");
const no_mark_checkbox = document.getElementById("no_mark_checkbox");
const mark_target_list_ul = document.getElementById("mark_target_list_ul");

const mark_target_dd_div = document.getElementById("mark_target_dd_div");
const monitor_area_div = document.getElementById("monitor_area_div");
const monitor_stream_area_img = document.getElementById("monitor_stream_area_img");

function post_job_data() {
    let data = {
        "job_type": "track",
        "scenario": "scenario_1",
        "predicted_mission": false,  // Todo: With the administration authenticate, predicted missions will be editable and this key true.
        "recognized_persons": [],
        "non_moving_target": null,
        "arm_expansion": false,
        "ai": null
    };

    if (security_mode_checkbox.checked) {
        data["job_type"] = "secure"
    } else if (learn_mode_checkbox.checked) {
        data["job_type"] = "learn"
    }

    if (recognize_all_select_checkbox.checked) {
        data["recognized_persons"] = ["all"]
    } else {
        for (let i = 0; i < recognize_checkboxes.length; i++) {
            if (recognize_checkboxes[i].checked) {
                data["recognized_persons"].push(recognize_checkboxes[i].id)
            }
        }
    }

    if (non_moving_target_checkbox.checked) {
        data["non_moving_target"] = true;
    }

    if (ai_checkbox.checked) {
        data["ai"] = "official_ai"

    }

    let labels = document.getElementsByTagName('label');

    for (let i = 0; i < scenario_checkboxes.length; i++) {
        if (scenario_checkboxes[i].checked) {
            for (let a = 0; a < labels.length; a++) {
                if (labels[a].htmlFor === scenario_checkboxes[i].id) {
                    data["scenario"] = labels[a].innerHTML;
                    console.log(labels[a].innerHTML);
                }
            }
        }
    }

    request_asynchronous('/api/job?admin_id=' + admin_id, 'POST',
        'application/json; charset=UTF-8', data, function (req, err, response) {
            if (err === "success") {
                let response_data = JSON.parse(response.responseText);
                console.log(response_data)
            }
        });

}

let selected_spans = [];

function show_checked_boxes(elements, dest) {
    while (dest.firstChild) {
        dest.removeChild(dest.firstChild);
    }

    let labels = document.getElementsByTagName('label');

    for (let i = 0; i < elements.length; i++) {
        if (elements[i].checked) {
            for (let a = 0; a < labels.length; a++) {
                if (labels[a].htmlFor === elements[i].id) {

                    let selected_div = document.createElement('div');
                    let selected_span = document.createElement('span');

                    selected_div.classList.add("position-relative");

                    selected_span.innerHTML = labels[a].innerHTML;
                    selected_span.classList.toggle("shine_in_dark");

                    selected_div.appendChild(selected_span);
                    dest.appendChild(selected_div);

                    selected_spans.push(selected_span);
                }
            }
        }
    }
}

function toggle_job_modal() {
    job_template_container.classList.toggle("focused");
    job_div.classList.toggle("focused");
    job_btn.classList.toggle("clicked");


    if (job_div.classList.contains("focused")) {  // 1. click
        job_btn.classList.remove("heart");

        if (dark_overlay_active) {
            dark_overlay_active = false
        } else {
            dark_deep_background_div.classList.toggle("focused");
            dark_overlay_active = true
        }

        job_btn_i.innerHTML = translate_text_item(" job");
        post_job_data();

        selected_spans = [];
        show_checked_boxes([security_mode_checkbox, learn_mode_checkbox, non_moving_target_checkbox, time_laps_checkbox].concat(recognize_checkboxes).concat(ai_checkboxes), selected_params_div);
        show_checked_boxes([].concat(scenario_checkboxes), selected_scenarios_div);

    } else {  // 2. click
        if (dark_overlay_active === false) {
            dark_overlay_active = true

        } else {
            dark_deep_background_div.classList.toggle("focused");
            dark_overlay_active = false
        }
        job_btn_i.innerHTML = "";
    }

    options_template_container.classList.toggle("hidden_element");
    controlling_template_container.classList.toggle("hidden_element");
    prepare_template_container.classList.toggle("hidden_element");
    system_info_template_container.classList.toggle("hidden_element");

}

job_div.addEventListener("click", function (event) {
    if (event.target === event.currentTarget) {
        toggle_job_modal()

    } else {
    }
});

setInterval(function () {
    if (!job_btn.classList.contains("clicked")) {
        job_btn.classList.add("heart");
    }

    setTimeout(function () {
        job_btn.classList.remove("heart");
    }, 1000)

}, 30000);

job_btn.addEventListener("click", toggle_job_modal);

interact('#job_btn')
    .draggable({
        // enable inertial throwing
        inertia: true,
        // keep the element within the area of it's parent
        modifiers: [
            interact.modifiers.restrictRect({
                restriction: 'parent',
                endOnly: true
            })
        ],
        // enable autoScroll
        autoScroll: false,

        // call this function on every dragmove event
        onmove: function (event) {
            setTimeout(function () {
                job_btn.removeEventListener("click", toggle_job_modal)
            }, 100);
            dragMoveListener(event);
        },
        // call this function on every dragend event
        onend: function (event) {
            setTimeout(function () {
                job_btn.addEventListener("click", toggle_job_modal)
            }, 100);
        }
    })
    .on('tap', function (event) {

    });

job_ready_btn.addEventListener("click", function () {
    if (job_ready_btn.innerHTML === translate_text_item("READY")) {
        job_ready_btn.innerHTML = translate_text_item("START");
        job_ready_btn.classList.add("ready");
        job_ready_btn.classList.remove("btn-warning");
        job_ready_btn.classList.add("btn-danger");

        job_cancel_btn.classList.add("active");

        job_simulate_btn.classList.add("inactive");

        selected_sce_span.classList.add("hidden_element");
        selected_param_span.classList.add("hidden_element");

        for (let i = 0; i < selected_spans.length; i++) {
            selected_spans[i].classList.remove("shine_in_dark");
            selected_spans[i].classList.add("shine_as_red_in_dark");
        }

    } else if (job_ready_btn.innerHTML === translate_text_item("START")) {
        job_ready_btn.innerHTML = translate_text_item("FINISH");
        job_ready_btn.classList.remove("ready");
        job_ready_btn.classList.add("start");
        job_ready_btn.classList.remove("btn-danger");
        job_ready_btn.classList.add("btn-dark");

        job_cancel_btn.classList.add("pause_job");
        job_cancel_btn.classList.remove("btn-warning");
        job_cancel_btn.classList.add("btn-dark");
        job_cancel_btn.innerHTML = translate_text_item("PAUSE");

        mark_target_dd_div.classList.add("focused");
        monitor_area_div.classList.add("focused");

        for (let i = 0; i < selected_spans.length; i++) {
            selected_spans[i].classList.remove("shine_as_red_in_dark");
            selected_spans[i].classList.add("hidden_element");
        }

        request_asynchronous('/api/job?type=real&admin_id=' + admin_id, 'PUT',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });

    } else if (job_ready_btn.innerHTML === translate_text_item("FINISH")) {
        job_ready_btn.innerHTML = translate_text_item("READY");
        job_ready_btn.classList.remove("start");
        job_ready_btn.classList.remove("btn-dark");
        job_ready_btn.classList.add("btn-warning");

        job_cancel_btn.classList.remove("active");
        job_cancel_btn.classList.remove("pause_job");
        job_cancel_btn.classList.remove("btn-dark");
        job_cancel_btn.classList.remove("btn-light");
        job_cancel_btn.classList.add("btn-warning");
        job_cancel_btn.innerHTML = translate_text_item("CANCEL");

        job_simulate_btn.classList.remove("inactive");

        mark_target_dd_div.classList.remove("focused");

        monitor_area_div.classList.remove("focused");
        monitor_area_div.classList.remove("active");

        monitor_stream_area_img.classList.remove("focused");

        selected_sce_span.classList.remove("hidden_element");
        selected_param_span.classList.remove("hidden_element");

        for (let i = 0; i < selected_spans.length; i++) {
            selected_spans[i].classList.add("shine_in_dark");
            selected_spans[i].classList.remove("hidden_element");
        }
        console.log("finish clicked");
        request_asynchronous('/api/job?admin_id=' + admin_id, 'DELETE',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });
    }
});


job_cancel_btn.addEventListener("click", function () {
    if (job_cancel_btn.innerText === translate_text_item("CANCEL")) {

        job_simulate_btn.classList.remove("inactive");

        job_cancel_btn.classList.remove("active");

        job_ready_btn.innerHTML = translate_text_item("READY");
        job_ready_btn.classList.remove("ready");
        job_ready_btn.classList.remove("btn-danger");
        job_ready_btn.classList.add("btn-warning");

        selected_sce_span.classList.remove("hidden_element");
        selected_param_span.classList.remove("hidden_element");

        for (let i = 0; i < selected_spans.length; i++) {
            selected_spans[i].classList.remove("shine_as_red_in_dark");
            selected_spans[i].classList.add("shine_in_dark");
        }

    } else if (job_cancel_btn.innerText === translate_text_item("PAUSE")) {
        job_cancel_btn.innerHTML = translate_text_item("RESUME");
        job_cancel_btn.classList.remove("btn-dark");
        job_cancel_btn.classList.add("btn-light");

        request_asynchronous('/api/job?pause=' + true + 'admin_id=' + admin_id, 'DELETE',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });

    } else if (job_cancel_btn.innerHTML === translate_text_item("RESUME")) {
        job_cancel_btn.innerHTML = translate_text_item("PAUSE");
        job_cancel_btn.classList.remove("btn-light");
        job_cancel_btn.classList.add("btn-dark");

        request_asynchronous('/api/job?admin_id=' + admin_id, 'PATCH',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });
    }
});

job_simulate_btn.addEventListener("click", function () {

    if (job_simulate_btn.innerText === translate_text_item("SIMULATE")) {

        job_simulate_btn.innerHTML = translate_text_item("HOLD TO PAUSE");
        job_simulate_btn.classList.add("active");

        job_cancel_btn.classList.add("hidden_element");

        job_ready_btn.classList.add("hidden_element");

        mark_target_dd_div.classList.add("focused");

        monitor_area_div.classList.add("focused");

        selected_sce_span.classList.add("hidden_element");
        selected_param_span.classList.add("hidden_element");

        for (let i = 0; i < selected_spans.length; i++) {
            selected_spans[i].classList.remove("shine_in_dark");
            selected_spans[i].classList.add("shine_as_red_in_dark");
        }

        request_asynchronous('/api/job?type=simulation&admin_id=' + admin_id, 'PUT',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });

    } else if (job_simulate_btn.innerText === translate_text_item("HOLD TO PAUSE")) {
        job_simulate_btn.innerHTML = translate_text_item("SIMULATE");
        job_simulate_btn.classList.remove("active");

        job_cancel_btn.classList.remove("hidden_element");

        job_ready_btn.classList.remove("hidden_element");

        mark_target_dd_div.classList.remove("focused");

        monitor_area_div.classList.remove("focused");
        monitor_area_div.classList.remove("active");

        monitor_stream_area_img.classList.remove("focused");

        selected_sce_span.classList.remove("hidden_element");
        selected_param_span.classList.remove("hidden_element");

        for (let i = 0; i < selected_spans.length; i++) {
            selected_spans[i].classList.remove("shine_as_red_in_dark");
            selected_spans[i].classList.add("shine_in_dark");
        }

        request_asynchronous('/api/job?admin_id=' + admin_id, 'DELETE',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });
    }
});

no_mark_checkbox.click();

no_mark_checkbox.addEventListener("change", function () {
    if (no_mark_checkbox.checked) {
        request_asynchronous('/api/job?mark=' + false + '&admin_id=' + admin_id, 'POST',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });
    }
});

mark_target_dd_btn.addEventListener("click", function () {
    while (mark_target_list_ul.firstChild) {
        mark_target_list_ul.removeChild(mark_target_list_ul.firstChild);
    }
    request_asynchronous('/api/job?cause=mark&admin_id=' + admin_id, 'GET',
        'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
            // err = "success";
            // requested_data = {"status": "OK", "data": {"drawings": ["single_rect", "partial_rect", "rotating_arcs"], "animations": ["animation_1"]}};

            if (err === "success") {
                if (requested_data["status"] === "OK") {


                    let target_mark_types = requested_data["data"];

                    function create_items(items) {
                        for (let c = 0; c < items.length; c++) {

                            let mark_select_div = document.createElement('div');
                            let mark_select_checkbox = document.createElement('input');
                            let mark_select_label = document.createElement('label');

                            mark_select_div.classList.add("dropdown-item", "form-check", "mb-1");

                            mark_select_checkbox.classList.add("form-check-input");
                            mark_select_checkbox.id = items[c] + "_checkbox_" + c;
                            mark_select_checkbox.type = "radio";
                            mark_select_checkbox.name = "mark_select";

                            mark_select_checkbox.addEventListener("change", function () {
                                if (mark_select_checkbox.checked) {
                                    request_asynchronous('/api/job?mark=' + items[c] + '&admin_id=' + admin_id, 'POST',
                                        'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                                            if (err === "success") {
                                                let response_data = JSON.parse(response.responseText);
                                            }
                                        });
                                }
                            });

                            mark_select_label.classList.add("form-check-label");
                            mark_select_label.setAttribute("for", mark_select_checkbox.id);
                            mark_select_label.innerHTML = items[c];

                            mark_select_div.appendChild(mark_select_checkbox);
                            mark_select_div.appendChild(mark_select_label);

                            mark_target_list_ul.appendChild(mark_select_div);
                        }
                    }

                    create_items(target_mark_types["drawings"]);
                    let divider_div = document.createElement('div');
                    divider_div.classList.add("dropdown-divider");
                    mark_target_list_ul.appendChild(divider_div);
                    create_items(target_mark_types["animations"]);
                }
            }
        });
});

let monitor_area_div_click_count = 0;

monitor_area_div.addEventListener("click", function () {
    monitor_area_div_click_count++;
    if (monitor_area_div_click_count <= 1) {
        monitor_stream_area_img.src = "/api/stream?type=monitoring&admin_id=" + admin_id;   // this url assigning creates a GET request.
        monitor_stream_area_img.classList.add("focused");

        mark_target_dd_div.classList.remove("focused");

        monitor_area_div.classList.add("active");

    } else {

        request_asynchronous('/api/stream?type=monitoring&admin_id=' + admin_id, 'DELETE',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });

        monitor_stream_area_img.src = "";
        monitor_stream_area_img.classList.remove("focused");

        mark_target_dd_div.classList.add("focused");

        monitor_area_div.classList.remove("active");

        monitor_area_div_click_count = 0;
    }
});