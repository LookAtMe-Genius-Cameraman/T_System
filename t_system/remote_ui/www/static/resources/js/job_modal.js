const job_template_container = document.getElementById("job_template_container");
const job_btn = document.getElementById("job_btn");
const job_btn_i = document.getElementById("job_btn_i");
const job_div = document.getElementById("job_div");

const job_simulate_btn = document.getElementById("job_simulate_btn");
const job_ready_btn = document.getElementById("job_ready_btn");
const job_cancel_btn = document.getElementById("job_cancel_btn");

const monitor_area_div = document.getElementById("monitor_area_div");

function toggle_job_modal() {
    job_template_container.classList.toggle("focused");
    job_div.classList.toggle("focused");
    job_btn.classList.toggle("clicked");

    if (dark_overlay_active) {

    } else {
        dark_deep_background_div.classList.toggle("focused");
        dark_overlay_active = false
    }

    if (job_div.classList.contains("focused")) {
        job_btn_i.innerHTML = translate_text_item(" job");
    } else {
        job_btn_i.innerHTML = "";
    }

    options_template_container.classList.toggle("hidden_element");
    controlling_template_container.classList.toggle("hidden_element");
    prepare_template_container.classList.toggle("hidden_element");
    system_info_template_container.classList.toggle("hidden_element");

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
  });

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