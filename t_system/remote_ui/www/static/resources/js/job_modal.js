const job_template_container = document.getElementById("job_template_container");
const job_btn = document.getElementById("job_btn");
const job_div = document.getElementById("job_div");

const job_simulate_btn = document.getElementById("job_simulate_btn");
const job_ready_btn = document.getElementById("job_ready_btn");
const job_cancel_btn = document.getElementById("job_cancel_btn");

const monitor_area_div = document.getElementById("monitor_area_div");

function dragElement(drag_element, header_element = null) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (header_element !== null) {
        // if present, the header is where you move the DIV from:
        header_element.onmousedown = drag_mouse_down;
        drag_element.ontouchstart = drag_touch_start;

    } else {
        // otherwise, move the DIV from anywhere inside the DIV:
        drag_element.onmousedown = drag_mouse_down;
        drag_element.ontouchstart = drag_touch_start;
    }

    let add_timeout;

    function drag_mouse_down(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = close_drag_element;
        // call a function whenever the cursor moves:
        document.onmousemove = mouse_element_drag;

        add_timeout = setTimeout(function () {
            job_btn.removeEventListener("click", toggle_job_modal)
        }, 100);
    }

    function drag_touch_start(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.ontouchend = close_drag_element;
        // call a function whenever the cursor moves:
        document.ontouchmove = touch_element_drag;

        add_timeout = setTimeout(function () {
            job_btn.removeEventListener("click", toggle_job_modal)
        }, 100);
    }

    function mouse_element_drag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        drag_element.style.top = (drag_element.offsetTop - pos2) + "px";
        drag_element.style.left = (drag_element.offsetLeft - pos1) + "px";
    }

    function touch_element_drag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:

        drag_element.style.top = (e.targetTouches[0].pageX - pos2) + "px";
        drag_element.style.left = (e.targetTouches[0].pageY - pos1) + "px";
    }

    function close_drag_element() {
        clearTimeout(add_timeout);

        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;

        document.ontouchend = null;
        document.ontouchmove = null;

        let timeout = setTimeout(function () {
            job_btn.addEventListener("click", toggle_job_modal)
        }, 100);
    }
}

function toggle_job_modal() {
    job_template_container.classList.toggle("focused");
    job_div.classList.toggle("focused");
    job_btn.classList.toggle("clicked");

    if (dark_overlay_active) {

    } else {
        dark_deep_background_div.classList.toggle("focused");
        dark_overlay_active = false
    }

    settings_template_container.classList.toggle("hidden_element");
    controlling_template_container.classList.toggle("hidden_element");
    prepare_template_container.classList.toggle("hidden_element");
    system_info_template_container.classList.toggle("hidden_element");

}

// Make the DIV element draggable:
dragElement(job_template_container, job_btn);

job_div.addEventListener("click", function (event) {
    if (event.target === event.currentTarget) {
        toggle_job_modal()

    } else {
        // alert('Child element clicked!');
    }

});

job_btn.addEventListener("click", toggle_job_modal);

job_ready_btn.addEventListener("click", function () {
    if (job_ready_btn.innerHTML === translate_text_item("READY")) {
        job_ready_btn.innerHTML = translate_text_item("START");
        job_ready_btn.classList.toggle("ready");
        job_ready_btn.classList.toggle("btn-warning");
        job_ready_btn.classList.toggle("btn-danger");

        job_cancel_btn.classList.toggle("active");

        job_simulate_btn.classList.toggle("inactive")

    } else if (job_ready_btn.innerHTML === translate_text_item("START")) {
        job_ready_btn.innerHTML = translate_text_item("FINISH");
        job_ready_btn.classList.toggle("ready");
        job_ready_btn.classList.toggle("start");
        job_ready_btn.classList.toggle("btn-danger");
        job_ready_btn.classList.toggle("btn-dark");

        job_cancel_btn.classList.toggle("pause_job");
        job_cancel_btn.classList.toggle("btn-warning");
        job_cancel_btn.classList.toggle("btn-dark");
        job_cancel_btn.innerHTML = translate_text_item("PAUSE");

        monitor_area_div.classList.toggle("focused");

        // shine_checked_boxes([ai_select_checkbox, security_mode_checkbox, non_moving_target_checkbox, time_laps_checkbox])

    } else if (job_ready_btn.innerHTML === translate_text_item("FINISH")) {
        job_ready_btn.innerHTML = translate_text_item("READY");
        job_ready_btn.classList.toggle("start");
        job_ready_btn.classList.toggle("btn-dark");
        job_ready_btn.classList.toggle("btn-warning");
        // dark_deep_background_div.classList.toggle("focused");

        job_cancel_btn.classList.toggle("active");
        job_cancel_btn.classList.toggle("pause_job");
        job_cancel_btn.classList.toggle("btn-dark");
        job_cancel_btn.classList.toggle("btn-warning");
        job_cancel_btn.innerHTML = translate_text_item("CANCEL");

        job_simulate_btn.classList.toggle("inactive");

        monitor_area_div.classList.toggle("focused");
    }
});


job_cancel_btn.addEventListener("click", function () {
    if (job_cancel_btn.innerText === translate_text_item("CANCEL")) {

        job_simulate_btn.classList.toggle("inactive");

        job_cancel_btn.classList.toggle("active");

        job_ready_btn.innerHTML = translate_text_item("READY");
        job_ready_btn.classList.toggle("ready");
        job_ready_btn.classList.toggle("btn-danger");
        job_ready_btn.classList.toggle("btn-warning");

    } else if (job_cancel_btn.innerText === translate_text_item("PAUSE")) {
        job_cancel_btn.innerHTML = translate_text_item("RESUME");
        job_cancel_btn.classList.toggle("btn-dark");
        job_cancel_btn.classList.toggle("btn-light");
    } else if (job_cancel_btn.innerHTML === translate_text_item("RESUME")) {
        job_cancel_btn.innerHTML = translate_text_item("PAUSE");
        job_cancel_btn.classList.toggle("btn-light");
        job_cancel_btn.classList.toggle("btn-dark");
    }
});

job_simulate_btn.addEventListener("click", function () {

    if (job_simulate_btn.innerText === translate_text_item("SIMULATE")) {

        job_simulate_btn.innerHTML = translate_text_item("HOLD TO PAUSE");
        job_simulate_btn.classList.toggle("active");
        job_ready_btn.classList.toggle("btn-dark");

        job_cancel_btn.classList.toggle("hidden_element");

        job_ready_btn.classList.toggle("hidden_element");

        monitor_area_div.classList.toggle("focused");

    } else if (job_simulate_btn.innerText === translate_text_item("HOLD TO PAUSE")) {
        job_simulate_btn.innerHTML = translate_text_item("SIMULATE");
        job_simulate_btn.classList.toggle("active");
        job_ready_btn.classList.toggle("btn-dark");

        job_cancel_btn.classList.toggle("hidden_element");

        job_ready_btn.classList.toggle("hidden_element");

        monitor_area_div.classList.toggle("focused");
    }


});