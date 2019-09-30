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

const monitor_area_div = document.getElementById("monitor_area_div");
const monitor_stream_area_img = document.getElementById("monitor_stream_area_img");

function post_job_data() {
    let data = {
        "job_type": "track",
        "scenario": "scenario_1",
        "predicted_mission": false,  // Todo: With the administration authenticate, predicted missions will be editable and this key true.
        "recognized_person": [],
        "non_moving_target": null,
        "ai": null
    };

    if (security_mode_checkbox.checked) {
        data["job_type"] = "secure"
    } else if (learn_mode_checkbox.checked) {
        data["job_type"] = "learn"
    }

    if (recognize_all_select_checkbox.checked) {
        data["recognized_person"] = ["all"]
    } else {
        for (let i = 0; i < recognize_checkboxes.length; i++) {
            if (recognize_checkboxes[i].checked) {
                data["recognized_person"].push(recognize_checkboxes[i].id)
            }
        }
    }

    if (non_moving_target_checkbox.checked) {
        data["non_moving_target"] = true;
    }

    if (ai_checkbox.checked) {
        data["ai"] = "official_ai"

    }

    jquery_manager.post_data("/api/job&admin_id=" + admin_id, data);

}

let selected_spans = [];

function show_checked_boxes(elements, dest) {
    selected_spans = [];
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
        if (dark_overlay_active) {
            dark_overlay_active = false
        } else {
            dark_deep_background_div.classList.toggle("focused");
            dark_overlay_active = true
        }

        job_btn_i.innerHTML = translate_text_item(" job");
        post_job_data();
        show_checked_boxes([security_mode_checkbox, learn_mode_checkbox, non_moving_target_checkbox, time_laps_checkbox].concat(recognize_checkboxes).concat(ai_checkboxes), selected_params_div)
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

        monitor_area_div.classList.add("focused");

        for (let i = 0; i < selected_spans.length; i++) {
            selected_spans[i].classList.remove("shine_as_red_in_dark");
            selected_spans[i].classList.add("hidden_element");
        }

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

        monitor_area_div.classList.remove("focused");
        monitor_area_div.classList.remove("active");

        monitor_stream_area_img.classList.remove("focused");

        selected_sce_span.classList.remove("hidden_element");
        selected_param_span.classList.remove("hidden_element");

        for (let i = 0; i < selected_spans.length; i++) {
            selected_spans[i].classList.add("shine_in_dark");
        }
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
    } else if (job_cancel_btn.innerHTML === translate_text_item("RESUME")) {
        job_cancel_btn.innerHTML = translate_text_item("PAUSE");
        job_cancel_btn.classList.remove("btn-light");
        job_cancel_btn.classList.add("btn-dark");
    }
});

job_simulate_btn.addEventListener("click", function () {

    if (job_simulate_btn.innerText === translate_text_item("SIMULATE")) {

        job_simulate_btn.innerHTML = translate_text_item("HOLD TO PAUSE");
        job_simulate_btn.classList.add("active");

        job_cancel_btn.classList.add("hidden_element");

        job_ready_btn.classList.add("hidden_element");

        monitor_area_div.classList.add("focused");

        selected_sce_span.classList.add("hidden_element");
        selected_param_span.classList.add("hidden_element");

        for (let i = 0; i < selected_spans.length; i++) {
            selected_spans[i].classList.remove("shine_in_dark");
            selected_spans[i].classList.add("shine_as_red_in_dark");
        }

    } else if (job_simulate_btn.innerText === translate_text_item("HOLD TO PAUSE")) {
        job_simulate_btn.innerHTML = translate_text_item("SIMULATE");
        job_simulate_btn.classList.remove("active");

        job_cancel_btn.classList.remove("hidden_element");

        job_ready_btn.classList.remove("hidden_element");

        monitor_area_div.classList.remove("focused");
        monitor_area_div.classList.remove("active");

        monitor_stream_area_img.classList.remove("focused");

        selected_sce_span.classList.remove("hidden_element");
        selected_param_span.classList.remove("hidden_element");

        for (let i = 0; i < selected_spans.length; i++) {
            selected_spans[i].classList.remove("shine_as_red_in_dark");
            selected_spans[i].classList.add("shine_in_dark");
        }
    }
});

let monitor_area_div_click_count = 0;

monitor_area_div.addEventListener("click", function () {
    monitor_area_div_click_count++;
    if (monitor_area_div_click_count <= 1) {
            monitor_stream_area_img.src = "/api/stream?type=preview&admin_id=" + admin_id;   // this url assigning creates a GET request.
            monitor_stream_area_img.classList.add("focused");

            monitor_area_div.classList.add("active");

        } else {
            stop_stream("monitoring");
            monitor_stream_area_img.src = "";
            monitor_stream_area_img.classList.remove("focused");

            monitor_area_div.classList.remove("active");

            monitor_area_div_click_count = 0;
        }
});