const job_template_container = document.getElementById("job_template_container");
const job_btn = document.getElementById("job_btn");
const job_btn_i = document.getElementById("job_btn_i");
const job_div = document.getElementById("job_div");

const ss_switch_checkbox = document.getElementById("ss_switch_checkbox");

const main_selected_div = document.getElementById("main_selected_div");

const selected_sce_div = document.getElementById("selected_sce_div");
const selected_sce_span = document.getElementById("selected_sce_span");
const selected_scenarios_div = document.getElementById("selected_scenarios_div");

const selected_param_div = document.getElementById("selected_param_div");
const selected_param_span = document.getElementById("selected_param_span");
const selected_params_div = document.getElementById("selected_params_div");

const selected_website_div = document.getElementById("selected_website_div");
const selected_website_span = document.getElementById("selected_website_span");
const selected_websites_div = document.getElementById("selected_websites_div");

const getting_lock_animation_div = document.getElementById("getting_lock_animation_div");
const getting_lock_animation = document.getElementById("getting_lock_animation");

const job_record_control_div = document.getElementById("job_record_control_div");
const job_record_btn = document.getElementById("job_record_btn");
const job_live_stream_control_div = document.getElementById("job_live_stream_control_div");
const job_live_stream_btn = document.getElementById("job_live_stream_btn");
const job_mission_control_div = document.getElementById("job_mission_control_div");
const job_mission_btn = document.getElementById("job_mission_btn");

const job_take_shots_btn = document.getElementById("job_take_shots_btn");
const job_ready_btn = document.getElementById("job_ready_btn");
const job_release_btn = document.getElementById("job_release_btn");

const mark_target_dd_div = document.getElementById("mark_target_dd_div");
const mark_target_dd_btn = document.getElementById("mark_target_dd_btn");
const no_mark_div = document.getElementById("no_mark_div");
const no_mark_checkbox = document.getElementById("no_mark_checkbox");
const mark_target_list_ul = document.getElementById("mark_target_list_ul");

const monitor_area_div = document.getElementById("monitor_area_div");

const monitor_area_counter_div = document.getElementById("monitor_area_counter_div");
const monitor_minutes_label = document.getElementById("monitor_minutes_label");
const monitor_seconds_label = document.getElementById("monitor_seconds_label");

const monitor_stream_area_img = document.getElementById("monitor_stream_area_img");

let monitor_total_seconds = 0;
let monitor_counter_interval;

function set_monitoring_time() {
    ++monitor_total_seconds;
    monitor_seconds_label.innerHTML = pad(monitor_total_seconds % 60);
    monitor_minutes_label.innerHTML = pad(parseInt(monitor_total_seconds / 60));
}

function reset_monitoring_time() {
    monitor_seconds_label.innerHTML = "00";
    monitor_minutes_label.innerHTML = "00";
}

function pad(val) {
    let valString = val + "";
    if (valString.length < 2) {
        return "0" + valString;
    } else {
        return valString;
    }
}

function toggle_job_control_btns(activate = false) {
    let job_control_btns = [job_record_btn, job_live_stream_btn, job_mission_btn];
    if (activate) {
        job_control_btns.forEach(function (btn) {
            if (btn.classList.contains("notRec")) {
                btn.click();
            }
        });
    } else {
        job_control_btns.forEach(function (btn) {
            if (btn.classList.contains("Rec")) {
                btn.click();
            }
        });
    }
}

function toggle_ss_switch_checkbox(activate = false) {
    ss_switch_checkbox.disabled = !activate;

    if (activate) {
        $('#ss_switch_checkbox').bootstrapToggle('destroy');

        ss_switch_checkbox.setAttribute("data-onstyle", "info");
        ss_switch_checkbox.setAttribute("data-offstyle", "success");

        $('#ss_switch_checkbox').bootstrapToggle();
    } else {
        $('#ss_switch_checkbox').bootstrapToggle('destroy');

        ss_switch_checkbox.setAttribute("data-onstyle", "default");
        ss_switch_checkbox.setAttribute("data-offstyle", "default");

        $('#ss_switch_checkbox').bootstrapToggle();
    }
}

function terminate_monitoring_stream() {
    if (monitor_area_div.classList.contains("active")) {
        monitor_area_div.click();
    }
}

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
                    if (labels[a].innerHTML === translate_text_item("Don't Use")) {
                        data["scenario"] = null;
                    }
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

function get_selected_recognize_checkboxes() {
    let labels = document.getElementsByTagName('label');

    for (let i = 0; i < recognize_checkboxes.length; i++) {
        for (let a = 0; a < labels.length; a++) {
            if (labels[a].htmlFor === recognize_checkboxes[i].id && labels[a].innerHTML === translate_text_item("Them all")) {
                return recognize_checkboxes[i];
            }
        }
    }
    return recognize_checkboxes;
}

let selected_spans = [];

function show_checked_boxes(elements, dest) {

    clearElement(dest);

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
        show_checked_boxes([security_mode_checkbox, learn_mode_checkbox, non_moving_target_checkbox, time_laps_checkbox].concat(get_selected_recognize_checkboxes()).concat(ai_checkboxes), selected_params_div);
        show_checked_boxes([].concat(scenario_checkboxes), selected_scenarios_div);
        show_checked_boxes([].concat(website_checkboxes), selected_websites_div);

        if (ss_switch_checkbox.checked) {
            monitor_area_counter_div.classList.add("focused");
        } else {
            monitor_area_div.click();
        }

        job_div.addEventListener("click", toggle_job_modal_by);
        dark_deep_background_div.addEventListener("click", toggle_job_modal_by);

    } else {  // 2. click
        if (dark_overlay_active === false) {
            dark_overlay_active = true

        } else {
            dark_deep_background_div.classList.toggle("focused");
            dark_overlay_active = false
        }
        job_btn_i.innerHTML = "";

        terminate_monitoring_stream();

        job_div.removeEventListener("click", toggle_job_modal_by);
        dark_deep_background_div.removeEventListener("click", toggle_job_modal_by);
    }

    options_template_container.classList.toggle("hidden_element");
    controlling_template_container.classList.toggle("hidden_element");
    prepare_template_container.classList.toggle("hidden_element");
    system_info_template_container.classList.toggle("hidden_element");

}

function toggle_job_modal_by(event) {
    if (event.target === event.currentTarget) {
        toggle_job_modal()
    } else {
    }
}

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

$('#ss_switch_checkbox').change(function () {
    if (ss_switch_checkbox.checked) {  // shooting
        if (job_div.contains(motion_control_div)) {
            job_div.removeChild(motion_control_div);
            motion_control_div.classList.remove("take_shots_job");
            rotational_control_div.classList.remove("take_shots_job");

            monitor_area_div.classList.remove("focused_shots_taking");
            terminate_monitoring_stream();

            selected_sce_div.classList.remove("hidden_element");
            selected_param_div.classList.remove("hidden_element");
            selected_website_div.classList.remove("hidden_element");

            job_ready_btn.classList.remove("hidden_element");

            job_take_shots_btn.classList.remove("active");

            monitor_area_counter_div.classList.add("focused");
        }

    } else {  // take shots
        if (!job_div.contains(motion_control_div)) {
            job_div.appendChild(motion_control_div);
            motion_control_div.classList.add("take_shots_job");
            rotational_control_div.classList.add("take_shots_job");

            monitor_area_div.classList.add("focused_shots_taking");
            monitor_area_div.click();

            selected_sce_div.classList.add("hidden_element");
            selected_param_div.classList.add("hidden_element");
            selected_website_div.classList.add("hidden_element");

            job_ready_btn.classList.add("hidden_element");

            job_take_shots_btn.classList.add("active");

            monitor_area_counter_div.classList.remove("focused");
        }
    }
});

job_record_btn.addEventListener("click", function () {
    if (job_record_btn.classList.contains("notRec")) {  // Start Recording
        job_record_btn.classList.remove("notRec");
        job_record_btn.classList.add("Rec");

        request_asynchronous('/api/job?cause=record&admin_id=' + admin_id, 'PUT',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                    monitor_minutes_label.classList.add("active");
                    monitor_seconds_label.classList.add("active");
                    monitor_counter_interval = setInterval(set_monitoring_time, 1000);
                }
            });

    } else {  // Stop Recording
        job_record_btn.classList.remove("Rec");
        job_record_btn.classList.add("notRec");

        clearInterval(monitor_counter_interval);

        request_asynchronous('/api/job?cause=record&admin_id=' + admin_id, 'DELETE',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                    reset_monitoring_time();
                    monitor_minutes_label.classList.remove("active");
                    monitor_seconds_label.classList.remove("active");
                }

            });
    }
});


job_live_stream_btn.addEventListener("click", function () {
    if (job_live_stream_btn.classList.contains("notRec")) {  // Start Mission
        job_live_stream_btn.classList.remove("notRec");
        job_live_stream_btn.classList.add("Rec");

        request_asynchronous('/api/job?cause=live_stream&admin_id=' + admin_id, 'PUT',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                    monitor_minutes_label.classList.add("active");
                    monitor_seconds_label.classList.add("active");
                    monitor_counter_interval = setInterval(set_monitoring_time, 1000);
                }
            });

    } else {  // Stop Mission
        job_live_stream_btn.classList.remove("Rec");
        job_live_stream_btn.classList.add("notRec");

        clearInterval(monitor_counter_interval);

        request_asynchronous('/api/job?cause=live_stream&admin_id=' + admin_id, 'DELETE',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                    reset_monitoring_time();
                    monitor_minutes_label.classList.remove("active");
                    monitor_seconds_label.classList.remove("active");
                }
            });
    }
});

job_mission_btn.addEventListener("click", function () {
    if (job_mission_btn.classList.contains("notRec")) {  // Start Mission
        job_mission_btn.classList.remove("notRec");
        job_mission_btn.classList.add("Rec");

        request_asynchronous('/api/job?cause=mission&admin_id=' + admin_id, 'PUT',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });

    } else {  // Stop Mission
        job_mission_btn.classList.remove("Rec");
        job_mission_btn.classList.add("notRec");

        request_asynchronous('/api/job?cause=mission&admin_id=' + admin_id, 'DELETE',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }

            });
    }
});

job_ready_btn.addEventListener("click", function () {
    if (job_ready_btn.innerHTML === translate_text_item("GET LOCK")) {
        job_ready_btn.innerHTML = translate_text_item("START");
        job_ready_btn.classList.add("ready");
        job_ready_btn.classList.remove("btn-warning");
        job_ready_btn.classList.add("btn-danger");

        job_release_btn.classList.add("active");

        getting_lock_animation.classList.add("lds-hourglass");
        getting_lock_animation_div.classList.add("focused");

        job_record_control_div.classList.add("enable");
        job_live_stream_control_div.classList.add("enable");
        job_mission_control_div.classList.add("enable");

        job_record_btn.classList.add("inactive");
        job_record_btn.disabled = true;

        job_live_stream_btn.classList.add("inactive");
        job_live_stream_btn.disabled = true;

        job_mission_btn.classList.add("inactive");
        job_mission_btn.disabled = true;

        monitor_area_div.classList.add("focused");

        main_selected_div.classList.add("locked");
        selected_sce_span.classList.add("hidden_element");
        selected_param_span.classList.add("hidden_element");
        selected_website_span.classList.add("hidden_element");

        for (let i = 0; i < selected_spans.length; i++) {
            selected_spans[i].classList.remove("shine_in_dark");
            selected_spans[i].classList.add("shine_as_red_in_dark");
        }

        toggle_ss_switch_checkbox(false);

        request_asynchronous('/api/job?cause=track&admin_id=' + admin_id, 'PUT',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);

                    getting_lock_animation.classList.remove("lds-hourglass");
                    getting_lock_animation_div.classList.remove("focused");

                    request_asynchronous('/api/live_stream?cause=availability&admin_id=' + admin_id, 'GET',
                        'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
                            if (err === "success") {
                                if (requested_data["status"] === "OK") {
                                    if (requested_data["data"]) {
                                        job_live_stream_btn.classList.add("notRec");
                                        job_live_stream_btn.classList.remove("inactive");
                                        job_live_stream_btn.disabled = false;
                                    } else {
                                        swal(translate_text_item("The Live Broadcast feature is not available because there is no internet access."), "", "warning");
                                    }
                                }
                            }
                        });

                    job_record_btn.classList.add("notRec");
                    job_record_btn.classList.remove("inactive");
                    job_record_btn.disabled = false;

                    job_mission_btn.classList.add("notRec");
                    job_mission_btn.classList.remove("inactive");
                    job_mission_btn.disabled = false;
                }
            });


        job_div.removeEventListener("click", toggle_job_modal_by);
        dark_deep_background_div.removeEventListener("click", toggle_job_modal_by);
    }
});


job_release_btn.addEventListener("click", function () {
    if (job_release_btn.innerText === translate_text_item("RELEASE")) {

        request_asynchronous('/api/job?cause=track&admin_id=' + admin_id, 'DELETE',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                    job_release_btn.classList.remove("active");

                    job_ready_btn.innerHTML = translate_text_item("GET LOCK");
                    job_ready_btn.classList.remove("ready");
                    job_ready_btn.classList.remove("btn-danger");
                    job_ready_btn.classList.add("btn-warning");

                    getting_lock_animation.classList.remove("lds-hourglass");
                    getting_lock_animation_div.classList.remove("focused");

                    job_record_control_div.classList.remove("enable");
                    job_live_stream_control_div.classList.remove("enable");
                    job_mission_control_div.classList.remove("enable");

                    terminate_monitoring_stream();
                    monitor_area_div.classList.remove("focused");
                    monitor_area_div.classList.remove("active");

                    main_selected_div.classList.remove("locked");

                    selected_sce_span.classList.remove("hidden_element");
                    selected_param_span.classList.remove("hidden_element");
                    selected_website_span.classList.remove("hidden_element");

                    for (let i = 0; i < selected_spans.length; i++) {
                        selected_spans[i].classList.remove("shine_as_red_in_dark");
                        selected_spans[i].classList.add("shine_in_dark");
                    }

                    toggle_ss_switch_checkbox(true);
                    toggle_job_control_btns(false);

                    job_div.addEventListener("click", toggle_job_modal_by);
                    dark_deep_background_div.addEventListener("click", toggle_job_modal_by);
                }
            });

    } else if (job_release_btn.innerText === translate_text_item("PAUSE")) {
        job_release_btn.innerHTML = translate_text_item("RESUME");
        job_release_btn.classList.remove("btn-dark");
        job_release_btn.classList.add("btn-light");

        request_asynchronous('/api/job?pause=' + true + 'admin_id=' + admin_id, 'DELETE',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });

    } else if (job_release_btn.innerHTML === translate_text_item("RESUME")) {
        job_release_btn.innerHTML = translate_text_item("PAUSE");
        job_release_btn.classList.remove("btn-light");
        job_release_btn.classList.add("btn-dark");

        request_asynchronous('/api/job?admin_id=' + admin_id, 'PATCH',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });
    }
});

job_take_shots_btn.addEventListener("click", function () {

    if (job_take_shots_btn.innerText === translate_text_item("TAKE PHOTO")) {
        monitor_area_div.classList.add("flashit");
        request_asynchronous('/api/job?cause=take_shots&admin_id=' + admin_id, 'PUT',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });

        setTimeout(function () {
            monitor_area_div.classList.remove("flashit");
        }, 1000);
    }
});


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

let mark_select_checkboxes = [];
mark_select_checkboxes.push(no_mark_checkbox);

no_mark_checkbox.click();

mark_target_dd_btn.addEventListener("click", function () {
    clearElement(mark_target_list_ul);
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

                            let mark_exist = false;

                            for (let i = 0; i < mark_select_checkboxes.length; i++) {
                                if (mark_select_checkboxes[i].id === mark_select_checkbox.id) {
                                    mark_select_checkbox = mark_select_checkboxes[i];
                                    mark_exist = true;
                                    break;
                                }
                            }

                            if (!mark_exist) {
                                mark_select_checkboxes.push(mark_select_checkbox);

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
                            }

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

        selected_params_div.classList.add("hidden_element");
        selected_scenarios_div.classList.add("hidden_element");
        selected_websites_div.classList.add("hidden_element");

        monitor_stream_area_img.src = "/api/stream?type=monitoring&admin_id=" + admin_id;   // this url assigning creates a GET request.
        monitor_stream_area_img.classList.add("focused");

        if (ss_switch_checkbox.checked) {
            mark_target_dd_div.classList.add("focused");

            job_record_control_div.classList.add("on_monitoring");
            job_live_stream_control_div.classList.add("on_monitoring");
            job_mission_control_div.classList.add("on_monitoring");
        }

        monitor_area_div.classList.add("active");

    } else {

        selected_params_div.classList.remove("hidden_element");
        selected_scenarios_div.classList.remove("hidden_element");
        selected_websites_div.classList.remove("hidden_element");

        request_asynchronous('/api/stream?type=monitoring&admin_id=' + admin_id, 'DELETE',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });

        monitor_stream_area_img.src = "";
        monitor_stream_area_img.classList.remove("focused");

        if (ss_switch_checkbox.checked) {
            mark_target_dd_div.classList.remove("focused");

            job_record_control_div.classList.remove("on_monitoring");
            job_live_stream_control_div.classList.remove("on_monitoring");
            job_mission_control_div.classList.remove("on_monitoring");
        }

        monitor_area_div.classList.remove("active");

        monitor_area_div_click_count = 0;
    }
});