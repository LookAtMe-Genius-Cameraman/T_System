const options_player_div = document.getElementById("options_player_div");
const options_video = document.getElementById("options_video");
const close_options_player_btn = document.getElementById("close_options_player_btn");
const options_player_source = document.getElementById("options_player_source");

const options_image_viewer_div = document.getElementById("options_image_viewer_div");
const close_options_image_viewer_btn = document.getElementById("close_options_image_viewer_btn");
const options_image_viewer_img = document.getElementById("options_image_viewer_img");

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
const f_enc_photo_input = document.getElementById("f_enc_photo_input");
const f_enc_photo_label = document.getElementById("f_enc_photo_label");
const encoded_face_list_ul = document.getElementById("encoded_face_list_ul");

const record_control_div = document.getElementById("record_control_div");
const record_control_btn = document.getElementById("record_control_btn");
const record_control_io_div = document.getElementById("record_control_io_div");
const record_list_ul = document.getElementById("record_list_ul");

const lang_select_div = document.getElementById("lang_select_div");
const lang_select_btn = document.getElementById("lang_select_btn");
const language_dropdown_div = document.getElementById("language_dropdown_div");


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
 * Method of getting specified network information with its ssid or the all existing network information.
 * It is triggered via a click on settings_btn or clicked specified network on network list.
 */
function get_face_recognition_data(id = null) {

    if (id) {
        jquery_manager.get_data("/api/face_encoding?id=" + id + "&admin_id=" + admin_id);
    } else {
        jquery_manager.get_data("/api/face_encoding?admin_id=" + admin_id);
    }
}

/**
 * Method of getting records, record lists and specified record information with their id, date or none.
 * It is triggered via a click on record_control_btn, specified date of the records or specified record.
 */
function get_record_data(date = null, id = null) {

    if (date && id) {
        jquery_manager.get_data("/api/record?date=" + date + "&id=" + id + "&admin_id=" + admin_id);
    } else if (!date && !id) {
        jquery_manager.get_data("/api/record?admin_id=" + admin_id);
    } else if (date) {
        jquery_manager.get_data("/api/record?date=" + date + "&admin_id=" + admin_id);
    } else if (id) {
        jquery_manager.get_data("/api/record?id=" + id + "&admin_id=" + admin_id);
    }
}


let update_control_btn_click_count = 0;
update_control_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    toggle_elements([wifi_control_div, audio_control_div, face_encoding_div, record_control_div, lang_select_div]);
    update_control_div.classList.toggle("col");
    update_control_div.classList.toggle("focused");
    update_control_div.classList.toggle("higher");
    update_control_io_div.classList.toggle("focused");

    update_control_btn_click_count++;
    if (update_control_btn_click_count <= 1) {
        get_update_data("auto_update");

        let timer_settings_cont = setInterval(function () {
            if (requested_data !== {}) {
                if (requested_data["status"] === "OK") {
                    auto_update_checkbox.checked = requested_data["data"] === true;
                }
                requested_data = {};
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

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    toggle_elements([update_control_div, audio_control_div, face_encoding_div, record_control_div, lang_select_div]);
    wifi_control_div.classList.toggle("col");
    wifi_control_div.classList.toggle("focused");
    wifi_control_div.classList.toggle("higher");
    wifi_control_io_div.classList.toggle("focused");

    wifi_connections_btn_click_count++;
    if (wifi_connections_btn_click_count <= 1) {
        get_network_data();

        let timer_settings_cont = setInterval(function () {

            if (requested_data !== {}) {

                if (requested_data["status"] === "OK") {

                    while (network_list_ul.firstChild) {
                        network_list_ul.removeChild(network_list_ul.firstChild);
                    }

                    for (let c = 0; c < requested_data["data"].length; c++) {

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
                requested_data = {};
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

let face_encoding_btn_click_count = 0;

face_encoding_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    toggle_elements([update_control_div, wifi_control_div, audio_control_div, record_control_div, lang_select_div]);
    face_encoding_div.classList.toggle("col");
    face_encoding_div.classList.toggle("focused");
    face_encoding_div.classList.toggle("higher");
    face_encoding_io_div.classList.toggle("focused");

    face_encoding_btn_click_count++;
    if (face_encoding_btn_click_count <= 1) {
        get_face_recognition_data();
        // requested_data = {"status": "OK", "data": [{"id": "z970136a-aegb-15e9-b130-cy2f756671ed", "name": "face_name", "image_names": ["image_name1", "image_name2"]}]};

        let face_encoding_interval = setInterval(function () {

            if (requested_data !== {}) {

                if (requested_data["status"] === "OK") {

                    for (let c = 0; c < requested_data["data"].length; c++) {

                        let face_dropdown_div = document.createElement('div');
                        let face_pp_img = document.createElement('img');
                        let face_a = document.createElement('a');
                        let face_dropdown_container_div = document.createElement('div');

                        face_dropdown_div.classList.add("dropdown", "show");

                        let src = "/api/face_encoding?id=" + requested_data["data"][c]["id"] + "&image=" + requested_data["data"][c]["image_names"][0] + "&admin_id=" + admin_id;   // this url assigning creates a GET request.
                        // let src = "static/resources/images/favicon.png" + "# " + new Date().getTime();

                        resize_image(src, 25, 40, face_pp_img);

                        face_a.classList.add("btn", "btn-secondary", "dropdown-toggle");
                        face_a.href = "#";
                        face_a.role = "button";
                        face_a.id = requested_data["data"][c]["name"] + "_a";
                        face_a.setAttribute("data-toggle", "dropdown");
                        face_a.setAttribute("aria-haspopup", "true");
                        face_a.setAttribute("aria-expanded", "false");
                        face_a.innerHTML = requested_data["data"][c]["name"];

                        face_dropdown_container_div.classList.add("dropdown-menu", "dropdown-menu-right");
                        face_dropdown_container_div.classList.add("container");
                        face_dropdown_container_div.setAttribute("aria-labelledby", face_a.id);

                        let face_dropdown_row_div;
                        for (let i = 0; i < requested_data["data"][c]["image_names"].length; i++) {
                            if (i % 3 === 0) {
                                face_dropdown_row_div = document.createElement('div');
                                face_dropdown_row_div.classList.add("row");
                                face_dropdown_container_div.appendChild(face_dropdown_row_div);

                            }
                            let face_dropdown_col_div = document.createElement('div');
                            face_dropdown_col_div.classList.add("col");

                            let face_img = document.createElement('img');
                            // Todo: make bigger when clicked and download when hold on.

                            let src = "/api/face_encoding?id=" + requested_data["data"][c]["id"] + "&image=" + requested_data["data"][c]["image_names"][i] + "&admin_id=" + admin_id;   // this url assigning creates a GET request.
                            resize_image(src, 25, 40, face_img);

                            face_img.addEventListener("click", function () {

                            });

                            face_dropdown_col_div.appendChild(face_img);
                            face_dropdown_row_div.appendChild(face_dropdown_col_div);
                        }
                        face_dropdown_div.appendChild(face_pp_img);
                        face_dropdown_div.appendChild(face_a);
                        face_dropdown_div.appendChild(face_dropdown_container_div);

                        encoded_face_list_ul.appendChild(face_dropdown_div);
                    }
                }

                requested_data = {};
                clearInterval(face_encoding_interval)
            }

        });
    } else {
        while (encoded_face_list_ul.firstChild) {
            encoded_face_list_ul.removeChild(encoded_face_list_ul.firstChild);
        }
        face_encoding_btn_click_count = 0;
    }


});

// $('#f_enc_photo_input').on('change',function(){
//                 //get the file name
//                 let fileName = $(this).val();
//                 //replace the "Choose a file" label
//                 $(this).next('.custom-file-label').html(fileName);
//             });

f_enc_photo_input.addEventListener("change", function (event) {
    if (event.target.files.length > 1) {
        f_enc_photo_label.innerHTML = event.target.files.length + " images uploaded";
    } else {
        f_enc_photo_label.innerHTML = event.target.files[0].name;
    }
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
        // requested_data = {"status": "OK", "data": ["22_05_2019", "23_05_2019", "27_05_2019", "27_05_2019", "27_05_2019", "27_05_2019", "27_05_2019", "27_05_2019", "27_05_2019"]};

        let record_dates;
        let record_dates_interval = setInterval(function () {

            if (requested_data !== {}) {
                if (requested_data["status"] === "OK") {
                    record_dates = requested_data["data"];
                    for (let c = 0; c < record_dates.length; c++) {

                        let date_dropdown_div = document.createElement('div');
                        let date_btn = document.createElement('button');
                        let date_dropdown_container_div = document.createElement('div');

                        date_dropdown_div.classList.add("dropdown", "btn-group", "mt-1");

                        date_btn.classList.add("btn", "btn-secondary", "dropdown-toggle");
                        date_btn.type = "button";
                        date_btn.id = record_dates[c] + "_btn";
                        date_btn.setAttribute("data-toggle", "dropdown");
                        date_btn.setAttribute("aria-haspopup", "true");
                        date_btn.setAttribute("aria-expanded", "false");
                        date_btn.innerHTML = record_dates[c].replace(/_/gi, "/"); // to replace all necessary characters.

                        date_dropdown_container_div.classList.add("dropdown-menu", "dropdown-menu-right", "dropdown-menu-center");
                        date_dropdown_container_div.setAttribute("aria-labelledby", date_btn.id);

                        let date_btn_click_count = 0;
                        date_btn.addEventListener("click", function () {

                            date_btn_click_count++;

                                while (date_dropdown_container_div.firstChild) {
                                    date_dropdown_container_div.removeChild(date_dropdown_container_div.firstChild);
                                }
                                get_record_data(record_dates[c], null);
                                // requested_data = {"status": "OK", "data": [{"id": "b970138a-argb-11e9-b145-cc2f844671ed", "name": "record_name", "time": "12_27_54", "length": 180, "extension": "mp4"}]};

                                let records;
                                let records_interval = setInterval(function () {
                                    if (requested_data !== {}) {

                                        if (requested_data["status"] === "OK") {
                                            records = requested_data["data"];

                                            for (let i = 0; i < records.length; i++) {
                                                let record_div = document.createElement('div');
                                                let record_a = document.createElement('a');
                                                let record_time_span = document.createElement('span');
                                                let record_length_span = document.createElement('span');

                                                record_div.classList.add("dropdown-item");
                                                record_div.id = records[i]["id"];

                                                record_a.role = "button";
                                                record_a.innerHTML = records[i]["name"];
                                                record_a.classList.add("record_a");

                                                record_time_span.innerHTML = records[i]["time"].replace(/_/gi, ":");
                                                record_time_span.classList.add("record_time_span");

                                                record_length_span.innerHTML = records[i]["length"] + " min.";
                                                record_length_span.classList.add("record_length_span");

                                                record_a.addEventListener("click", function () {

                                                    record_control_div.classList.toggle("hidden_element");
                                                    options_player_div.classList.toggle("focused");

                                                    options_player_source.type = "video/" + records[i]["extension"];
                                                    options_player_source.src = "/api/record?id=" + records[i]["id"] + "&admin_id=" + admin_id;

                                                    // options_player_source.src = "static/resources/images/mov_bbb.mp4"+ "# " + new Date().getTime();
                                                    options_video.load()
                                                });

                                                record_div.appendChild(record_a);
                                                record_div.appendChild(record_time_span);
                                                record_div.appendChild(record_length_span);

                                                date_dropdown_container_div.appendChild(record_div);
                                            }
                                        }
                                        requested_data = {};
                                        clearInterval(records_interval)
                                    }
                                }, 300);
                        });
                        date_dropdown_div.appendChild(date_btn);
                        date_dropdown_div.appendChild(date_dropdown_container_div);

                        record_list_ul.appendChild(date_dropdown_div);
                    }
                }
                requested_data = {};
                clearInterval(record_dates_interval)
            }
        }, 300);

    } else {
        while (record_list_ul.firstChild) {
            record_list_ul.removeChild(record_list_ul.firstChild);
        }
        record_control_btn_click_count = 0;
    }
});

close_options_player_btn.addEventListener("click", function () {
    options_player_div.classList.toggle("focused");
    options_player_source.src = "";
    record_control_div.classList.toggle("hidden_element");
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
