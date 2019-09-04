const update_control_div = document.getElementById("update_control_div");
const update_control_btn = document.getElementById("update_control_btn");
const update_control_io_div = document.getElementById("update_control_io_div");
const auto_update_checkbox = document.getElementById("auto_update_checkbox");

const wifi_control_div = document.getElementById("wifi_control_div");
const wifi_connections_btn = document.getElementById("wifi_connections_btn");
const wifi_control_io_div = document.getElementById("wifi_control_io_div");
const network_ssid_input = document.getElementById("network_ssid_input");
const network_password_input = document.getElementById("network_password_input");
const create_new_network_btn = document.getElementById("create_new_network_btn");
const network_list_ul = document.getElementById("network_list_ul");

const audio_control_div = document.getElementById("audio_control_div");
const audio_control_btn = document.getElementById("audio_control_btn");
const audio_control_io_div = document.getElementById("audio_control_io_div");

const face_encoding_div = document.getElementById("face_encoding_div");
const face_encoding_btn = document.getElementById("face_encoding_btn");
const face_encoding_io_div = document.getElementById("face_encoding_io_div");

const record_control_div = document.getElementById("record_control_div");
const record_control_btn = document.getElementById("record_control_btn");
const record_control_io_div = document.getElementById("record_control_io_div");
const record_list_ul = document.getElementById("record_list_ul");

const lang_select_div = document.getElementById("lang_select_div");
const lang_select_btn = document.getElementById("lang_select_btn");
const language_dropdown_div = document.getElementById("language_dropdown_div");


// a_i_checkbox.addEventListener("change", function () {  // Checkbox onchange sample
//
//     if (a_i_checkbox.checked){
//     }
//     else {
//     }
//
// });

/**
 * Method to updating `auto_update` status of UpdateManager of t_system.
 */
function put_update_data(data) {
    jquery_manager.post_data("/api/update&admin_id=" + admin_id, data);
}

/**
 * Method of getting specified network information with its ssid or the all existing network information.
 * It is triggered via a click on settings_btn or clicked specified network on network list.
 */
function get_update_data(key) {
    jquery_manager.get_data("/api/network?key=" + key + "&admin_id=" + admin_id);
}

/**
 * Method of getting specified network information with its ssid or the all existing network information.
 * It is triggered via a click on settings_btn or clicked specified network on network list.
 */
function get_network_data(ssid = null) {

    if (ssid) {
        jquery_manager.get_data("/api/network?ssid=" + ssid + "&admin_id=" + admin_id);
    } else {
        jquery_manager.get_data("/api/network?admin_id=" + admin_id);
    }
}

/**
 * Method of getting records, record lists and specified record information with their id, date or none.
 * It is triggered via a click on record_control_btn, specified date of the records or specified record.
 */
function get_record_data(date = null, id = null) {

    if (date && id) {
        return false
    }

    if (!date && !id) {
        jquery_manager.get_data("/api/record?admin_id=" + admin_id);
    } else if (date) {
        jquery_manager.get_data("/api/record?date=" + date + "&admin_id=" + admin_id);
    } else if (id) {
        jquery_manager.get_data("/api/record?id=" + id + "&admin_id=" + admin_id);
    }
}

let update_control_btn_click_count = 0;
update_control_btn.addEventListener("click", function () {
    update_control_btn_click_count++;

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([wifi_control_div, audio_control_div, face_encoding_div, record_control_div, lang_select_div]);
    update_control_div.classList.toggle("col");
    update_control_div.classList.toggle("focused");
    update_control_div.classList.toggle("higher");
    update_control_io_div.classList.toggle("focused");

    if (update_control_btn_click_count <= 1) {
        get_update_data("auto_update");

        let timer_settings_cont = setInterval(function () {
            if (requested_data !== null) {
                if (requested_data["status"] === "OK") {
                    auto_update_checkbox.checked = requested_data["data"] === true;
                }
                requested_data = null;
                clearInterval(timer_settings_cont)
            }
        });

    } else {
        update_control_btn_click_count = 0;
    }
});

auto_update_checkbox.addEventListener("change", function () {
    if (auto_update_checkbox.checked) {
        let data = {"auto_update": true};
        put_update_data(data);
    } else {
        let data = {"auto_update": false};
        put_update_data(data);
    }
});

let wifi_connections_btn_click_count = 0;
wifi_connections_btn.addEventListener("click", function () {
    wifi_connections_btn_click_count++;

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    toggle_elements([update_control_div, audio_control_div, face_encoding_div, record_control_div, lang_select_div]);
    wifi_control_div.classList.toggle("col");
    wifi_control_div.classList.toggle("focused");
    wifi_control_div.classList.toggle("higher");
    wifi_control_io_div.classList.toggle("focused");

    if (wifi_connections_btn_click_count <= 1) {
        get_network_data();

        let timer_settings_cont = setInterval(function () {

            if (requested_data !== null) {

                if (requested_data["status"] === "OK") {

                    while (network_list_ul.firstChild) {
                        network_list_ul.removeChild(network_list_ul.firstChild);
                    }

                    for (let c = 0; c < requested_data["data"].length; c++) {
                        // console.log(event_db[c]["name"]);
                        let li = document.createElement('li');
                        let section = document.createElement('section');

                        let ssid_output = document.createElement('output');
                        let password_output = document.createElement('output');

                        ssid_output.value = requested_data["data"][c]["ssid"];
                        password_output.value = requested_data["data"][c]["password"];

                        li.appendChild(section);
                        section.appendChild(ssid_output);
                        section.appendChild(password_output);

                        network_list_ul.appendChild(li);
                    }
                }
                requested_data = null;
                clearInterval(timer_settings_cont)
            }
        }, 500);
        // jquery_manager.post_data("/try", {"bla": "bla"})
    } else {
        wifi_connections_btn_click_count = 0;
    }
});

function show_create_new_wifi_button() {
    if (network_ssid_input.value !== "" && network_password_input.value !== "") {
        network_ssid_input.classList.add("new_network_input_transition");
        network_password_input.classList.add("new_network_input_transition");
        show_element(create_new_network_btn);
    } else {
        network_ssid_input.classList.remove("new_network_input_transition");
        network_password_input.classList.remove("new_network_input_transition");
        hide_element(create_new_network_btn);
    }
}

network_ssid_input.addEventListener("mousemove", show_create_new_wifi_button);
network_password_input.addEventListener("mousemove", show_create_new_wifi_button);

create_new_network_btn.addEventListener("click", function () {

    let data = {"ssid": network_ssid_input.value, "password": network_password_input.value};
    jquery_manager.post_data("/api/network", data);

    network_ssid_input.value = "";
    network_password_input.value = "";
    wifi_connections_btn.click();
    wifi_connections_btn.click();

    admin_id = response_data["admin_id"];
    console.log(admin_id)
});

audio_control_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    toggle_elements([update_control_div, wifi_control_div, face_encoding_div, record_control_div, lang_select_div]);
    audio_control_div.classList.toggle("col");
    audio_control_div.classList.toggle("focused");
    audio_control_div.classList.toggle("higher");
    audio_control_io_div.classList.toggle("focused");
});

face_encoding_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    toggle_elements([update_control_div, wifi_control_div, audio_control_div, record_control_div, lang_select_div]);
    face_encoding_div.classList.toggle("col");
    face_encoding_div.classList.toggle("focused");
    face_encoding_div.classList.toggle("higher");
    face_encoding_io_div.classList.toggle("focused");
});


let record_control_btn_click_count = 0;

record_control_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, wifi_control_div, audio_control_div, face_encoding_div, lang_select_div]);
    record_control_div.classList.toggle("col");
    record_control_div.classList.toggle("focused");
    record_control_div.classList.toggle("higher");
    record_control_io_div.classList.toggle("focused");

    record_control_btn_click_count++;

    if (record_control_btn_click_count <= 1) {
        get_record_data();

        let timer_settings_cont = setInterval(function () {

            if (requested_data !== null) {

                if (requested_data["status"] === "OK") {

                    while (record_list_ul.firstChild) {
                        record_list_ul.removeChild(record_list_ul.firstChild);
                    }

                    for (let c = 0; c < requested_data["data"].length; c++) {
                        let li = document.createElement('li');
                        let section = document.createElement('section');

                        let date_dropdown_div = document.createElement('div');
                        let date_a = document.createElement('a');
                        let date_dropdown_container_div = document.createElement('div');

                        date_dropdown_div.classList.add("dropdown show");

                        date_a.classList.add("btn btn-secondary dropdown-toggle");
                        date_a.href = "#";
                        date_a.role = "button";
                        date_a.id = requested_data["data"][c] + "_a";
                        date_a.attr("data-toggle", "dropdown");
                        date_a.attr("aria-haspopup", "true");
                        date_a.attr("aria-expanded", "false");
                        date_a.innerHTML = requested_data["data"][c];


                        date_dropdown_container_div.classList.add("dropdown-menu");
                        date_dropdown_container_div.attr("aria-labelledby", date_a.id);

                        requested_data = null;

                        get_record_data(date_a.innerHTML, null);

                        let timer_settings_cont = setInterval(function () {

                            if (requested_data !== null) {

                                if (requested_data["status"] === "OK") {
                                    for (let c = 0; c < requested_data["data"].length; c++) {
                                        let record_div = document.createElement('div');
                                        let record_a = document.createElement('a');
                                        let record_time_span = document.createElement('span');
                                        let record_length_span = document.createElement('span');

                                        record_div.classList.add("dropdown-item");
                                        record_div.id = requested_data["data"][c]["id"];

                                        record_a.role = "button";
                                        record_a.innerHTML = requested_data["data"][c]["name"];
                                        record_time_span.innerHTML = requested_data["data"][c]["time"];
                                        record_length_span.innerHTML = requested_data["data"][c]["length"];

                                        record_a.addEventListener("click", function () {
                                            // Todo: Video getting, playing processes will be here.
                                            get_record_data(null, record_div.id);
                                        });

                                        record_div.appendChild(record_a);
                                        record_div.appendChild(record_time_span);
                                        record_div.appendChild(record_length_span);

                                        date_dropdown_container_div.appendChild(record_div);
                                    }
                                }
                                requested_data = null;
                                clearInterval(timer_settings_cont)
                            }
                        }, 500);

                        li.appendChild(section);
                        section.appendChild(date_dropdown_div);
                        date_dropdown_div.appendChild(date_a);
                        date_dropdown_div.appendChild(date_dropdown_container_div);

                        network_list_ul.appendChild(li);
                    }
                }
                requested_data = null;
                clearInterval(timer_settings_cont);
            }
        }, 500);
    } else {
        record_control_btn_click_count = 0;
    }
});

lang_select_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, wifi_control_div, audio_control_div, face_encoding_div, record_control_div]);
    lang_select_div.classList.toggle("col");
    lang_select_div.classList.toggle("focused");
    lang_select_div.classList.toggle("higher");
    language_dropdown_div.classList.toggle("focused");
});
