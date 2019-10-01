const options_player_div = document.getElementById("options_player_div");
const options_video = document.getElementById("options_video");
const close_options_player_btn = document.getElementById("close_options_player_btn");
const options_player_source = document.getElementById("options_player_source");

const options_image_viewer_div = document.getElementById("options_image_viewer_div");
const options_image_viewer_img = document.getElementById("options_image_viewer_img");

const update_control_div = document.getElementById("update_control_div");
const update_control_btn = document.getElementById("update_control_btn");
const update_control_io_div = document.getElementById("update_control_io_div");
const auto_update_checkbox = document.getElementById("auto_update_checkbox");
const update_btn = document.getElementById("update_btn");

const wifi_control_div = document.getElementById("wifi_control_div");
const wifi_connections_btn = document.getElementById("wifi_connections_btn");
const wifi_control_io_div = document.getElementById("wifi_control_io_div");
const network_ssid_input = document.getElementById("network_ssid_input");
const network_password_input = document.getElementById("network_password_input");
const network_pass_eye_span = document.getElementById("network_pass_eye_span");
const create_new_network_btn = document.getElementById("create_new_network_btn");
const network_list_ul = document.getElementById("network_list_ul");

const audio_control_div = document.getElementById("audio_control_div");
const audio_control_btn = document.getElementById("audio_control_btn");
const audio_control_io_div = document.getElementById("audio_control_io_div");

const face_encoding_div = document.getElementById("face_encoding_div");
const face_encoding_btn = document.getElementById("face_encoding_btn");
const face_encoding_io_div = document.getElementById("face_encoding_io_div");
const face_encoding_form = document.getElementById("face_encoding_form");
const face_name_input = document.getElementById("face_name_input");
const f_enc_photo_input = document.getElementById("f_enc_photo_input");
const f_enc_photo_label = document.getElementById("f_enc_photo_label");
const encode_new_face_btn = document.getElementById("encode_new_face_btn");
const encoded_face_list_ul = document.getElementById("encoded_face_list_ul");
const processing_animation_div = document.getElementById("processing_animation_div");
const processing_animation = document.getElementById("processing_animation");

const record_control_div = document.getElementById("record_control_div");
const record_control_btn = document.getElementById("record_control_btn");
const record_control_io_div = document.getElementById("record_control_io_div");
const record_list_ul = document.getElementById("record_list_ul");

const lang_select_div = document.getElementById("lang_select_div");
const lang_select_btn = document.getElementById("lang_select_btn");
const language_dropdown_div = document.getElementById("language_dropdown_div");

const help_control_div = document.getElementById("help_control_div");
const help_control_btn = document.getElementById("help_control_btn");
const help_control_io_div = document.getElementById("help_control_io_div");

const empty_option_div = document.getElementById("empty_option_div");
const empty_option_btn = document.getElementById("empty_option_btn");
const empty_option_io_div = document.getElementById("empty_option_io_div");



/**
 * Method to updating `auto_update` status of UpdateManager of t_system.
 */
function put_update_data(data) {
    jquery_manager.put_data("/api/update&admin_id=" + admin_id, data);
}

/**
 * Method of getting specified network information with its ssid or the all existing network information.
 * It is triggered via a click on options_btn or clicked specified network on network list.
 */
function get_update_data(key) {
    jquery_manager.get_data("/api/network?key=" + key + "&admin_id=" + admin_id);
}

/**
 * Method of getting specified network information with its ssid or the all existing network information.
 * It is triggered via a click on options_btn or clicked specified network on network list.
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
 * It is triggered via a click on options_btn or clicked specified network on network list.
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

    toggle_elements([wifi_control_div, audio_control_div, face_encoding_div, record_control_div, empty_option_div, lang_select_div, help_control_div]);
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
        }, 300);
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

update_btn.addEventListener("click", function () {
    // Todo: Response will handled. for response arrive, button will be disabled. and maybe for update completed, Remote UI will sleep, shutdown or locked. decide that.
    jquery_manager.post_data("/api/update?admin_id=" + admin_id, {})
});

let wifi_connections_btn_click_count = 0;
wifi_connections_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, audio_control_div, face_encoding_div, record_control_div, empty_option_div, lang_select_div, help_control_div]);
    wifi_control_div.classList.toggle("col");
    wifi_control_div.classList.toggle("focused");
    wifi_control_div.classList.toggle("higher");
    wifi_control_io_div.classList.toggle("focused");

    wifi_connections_btn_click_count++;
    if (wifi_connections_btn_click_count <= 1) {
        get_network_data();
        // requested_data = {"status": "OK", "data": [{"ssid": "Beyaz", "password": "arge"}, {"ssid": "new_wifi", "password": "1234"}, {"ssid": "demo", "password": "bla"}]};

        let timer_settings_cont = setInterval(function () {

            if (requested_data !== {}) {

                if (requested_data["status"] === "OK") {
                    let network_connections = requested_data["data"];

                    for (let c = 0; c < network_connections.length; c++) {

                        let wifi_dropdown_div = document.createElement('div');
                        let wifi_btn = document.createElement('button');
                        let wifi_dropdown_container_div = document.createElement('div');

                        wifi_dropdown_div.classList.add("dropdown", "btn-group", "mt-1");

                        wifi_btn.classList.add("btn", "btn-secondary", "dropdown-toggle", "cut-text");
                        wifi_btn.type = "button";
                        wifi_btn.id = network_connections[c]["ssid"] + "_btn";
                        wifi_btn.setAttribute("data-toggle", "dropdown");
                        wifi_btn.setAttribute("aria-haspopup", "true");
                        wifi_btn.setAttribute("aria-expanded", "false");
                        wifi_btn.innerHTML = network_connections[c]["ssid"];

                        wifi_dropdown_container_div.classList.add("dropdown-menu", "dropdown-menu-right", "dropdown-menu-center", "body_background", "no-border");
                        wifi_dropdown_container_div.setAttribute("aria-labelledby", wifi_btn.id);

                        // let ssid_output = document.createElement('output');
                        let password_div = document.createElement('div');
                        let password_input = document.createElement('input');
                        let password_update_btn = document.createElement('button');

                        password_div.classList.add("dropdown-item");

                        password_input.type = "password";
                        password_input.classList.add("modal_input", "existing_network_password");
                        password_input.value = network_connections[c]["password"];

                        let password_last_value = password_input.value;

                        password_input.addEventListener("focus", function () {
                            password_input.classList.add("focused");
                        });

                        password_input.addEventListener("blur", function () {
                            password_input.classList.remove("focused");
                        });

                        password_input.addEventListener("mousemove", function () {
                            if (password_input.value !== "" && password_input.value !== password_last_value) {
                                password_input.classList.add("changed");
                                show_element(password_update_btn);
                            } else {
                                password_input.classList.remove("changed");
                                hide_element(password_update_btn);
                            }
                        });


                        password_update_btn.classList.add("send_network_data_btn");
                        password_update_btn.innerHTML = "&#187;";

                        password_update_btn.addEventListener("click", function () {
                            let data = {"ssid": network_connections[c]["ssid"], "password": password_input.value};
                            jquery_manager.put_data("/api/network?ssid=" + network_connections[c]["ssid"] + "&admin_id=" + admin_id, data);

                            wifi_connections_btn.click();
                            wifi_connections_btn.click();
                        });

                        password_div.appendChild(password_input);
                        password_div.appendChild(password_update_btn);

                        wifi_dropdown_container_div.appendChild(password_div);

                        wifi_dropdown_div.appendChild(wifi_btn);
                        wifi_dropdown_div.appendChild(wifi_dropdown_container_div);

                        network_list_ul.appendChild(wifi_dropdown_div);
                    }
                }
                requested_data = {};
                clearInterval(timer_settings_cont)
            }
        }, 300);
    } else {
        while (network_list_ul.firstChild) {
            network_list_ul.removeChild(network_list_ul.firstChild);
        }
        wifi_connections_btn_click_count = 0;
    }
});

network_pass_eye_span.addEventListener("click", function () {
    network_pass_eye_span.classList.toggle("fa-eye fa-eye-slash");
    if (network_password_input.type === 'password') {
        network_password_input.setAttribute('type', 'text');
  }
  else {
        network_password_input.setAttribute('type', 'password');
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

    let data = {};
    data = {"ssid": network_ssid_input.value, "password": network_password_input.value};
    jquery_manager.post_data("/api/network", data);

    network_ssid_input.value = "";
    network_password_input.value = "";

    let new_network_interval = setInterval(function () {

        if (response_data !== {}) {
            if (response_data["status"] === "OK") {
                wifi_connections_btn.click();
                wifi_connections_btn.click();

                admin_id = response_data["admin_id"];
                console.log(admin_id)
            }
            response_data = {};
            clearInterval(new_network_interval);
        }
    }, 300);


});

audio_control_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    toggle_elements([update_control_div, wifi_control_div, face_encoding_div, record_control_div, empty_option_div, lang_select_div, help_control_div]);
    audio_control_div.classList.toggle("col");
    audio_control_div.classList.toggle("focused");
    audio_control_div.classList.toggle("higher");
    audio_control_io_div.classList.toggle("focused");
});

let face_encoding_btn_click_count = 0;

face_encoding_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    toggle_elements([update_control_div, wifi_control_div, audio_control_div, record_control_div, empty_option_div, lang_select_div, help_control_div]);
    face_encoding_div.classList.toggle("col");
    face_encoding_div.classList.toggle("focused");
    face_encoding_div.classList.toggle("higher");
    face_encoding_io_div.classList.toggle("focused");

    face_encoding_btn_click_count++;
    if (face_encoding_btn_click_count <= 1) {
        get_face_recognition_data();
        // requested_data = {"status": "OK", "data": [{"id": "z970136a-aegb-15e9-b130-cy2f756671ed", "name": "face_name", "image_names": ["im-n1", "im-n2", "im-n3", "im-n4", "im-n5"]}]};

        let face_encoding_interval = setInterval(function () {

            if (requested_data !== {}) {
                if (requested_data["status"] === "OK") {
                    for (let c = 0; c < requested_data["data"].length; c++) {

                        let face_dropdown_div = document.createElement('div');
                        let face_pp_img = document.createElement('img');
                        let face_a = document.createElement('a');
                        let face_dropdown_container_div = document.createElement('div');

                        face_dropdown_div.classList.add("dropdown", "show", "mb-1");

                        let src = "/api/face_encoding?id=" + requested_data["data"][c]["id"] + "&image=" + requested_data["data"][c]["image_names"][0] + "&admin_id=" + admin_id;   // this url assigning creates a GET request.
                        // let src = "static/resources/images/favicon.png" + "# " + new Date().getTime();

                        resize_image(src, 30, 40, face_pp_img);

                        face_a.classList.add("btn", "btn-secondary", "dropdown-toggle", "cut-text", "face_a", "ml-1");
                        face_a.href = "#";
                        face_a.role = "button";
                        face_a.id = requested_data["data"][c]["name"] + "_a";
                        face_a.setAttribute("data-toggle", "dropdown");
                        face_a.setAttribute("aria-haspopup", "true");
                        face_a.setAttribute("aria-expanded", "false");
                        face_a.innerHTML = requested_data["data"][c]["name"].replace(/_/gi, " ");
                        face_a.title = face_a.innerHTML;

                        face_dropdown_container_div.classList.add("dropdown-menu", "dropdown-menu-right", "dropdown_menu", "face_encoding_dropdown_menu");
                        face_dropdown_container_div.classList.add("container");
                        face_dropdown_container_div.setAttribute("aria-labelledby", face_a.id);

                        let face_dropdown_row_div;
                        for (let i = 0; i < requested_data["data"][c]["image_names"].length; i++) {

                            if (i % 3 === 0) {
                                face_dropdown_row_div = document.createElement('div');
                                face_dropdown_row_div.classList.add("row", "mb-1", "face_row");
                            }

                            let face_dropdown_col_div = document.createElement('div');
                            face_dropdown_col_div.classList.add("col-*", "ml-2");

                            let face_div = document.createElement('div');
                            let face_img = document.createElement('img');

                            face_div.id = requested_data["data"][c]["image_names"][i];
                            face_div.classList.add("face_div");

                            let src = "/api/face_encoding?id=" + requested_data["data"][c]["id"] + "&image=" + requested_data["data"][c]["image_names"][i] + "&admin_id=" + admin_id;   // this url assigning creates a GET request.
                            resize_image(src, 25, 40, face_img);

                            interact('#' + face_div.id)
                                .on('tap', function (event) {
                                })
                                .on('doubletap', function (event) {
                                    let route = "/api/face_encoding?id=" + requested_data["data"][c]["id"] + "&image=" + requested_data["data"][c]["image_names"][0] + "&download=" + true + "&admin_id=" + admin_id;
                                    jquery_manager.get_data(route);
                                })
                                .on('hold', function (event) {
                                    console.log("triggered haaa?");
                                    face_encoding_div.classList.add("hidden_element");
                                    options_image_viewer_div.classList.add("focused");
                                    options_image_viewer_img.src = src;

                                })
                                .on('up', function (event) {
                                    options_image_viewer_div.classList.remove("focused");
                                    options_image_viewer_img.src = "";
                                    face_encoding_div.classList.remove("hidden_element");
                                });

                            face_div.appendChild(face_img);
                            face_dropdown_col_div.appendChild(face_div);
                            face_dropdown_row_div.appendChild(face_dropdown_col_div);
                            face_dropdown_container_div.appendChild(face_dropdown_row_div);

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
        }, 300);
    } else {
        while (encoded_face_list_ul.firstChild) {
            encoded_face_list_ul.removeChild(encoded_face_list_ul.firstChild);
        }
        face_encoding_btn_click_count = 0;
    }


});

f_enc_photo_input.addEventListener("change", function (event) {
    if (event.target.files.length > 1) {
        f_enc_photo_label.innerHTML = event.target.files.length + " images uploaded";
    } else {
        f_enc_photo_label.innerHTML = event.target.files[0].name;
    }
});

encode_new_face_btn.addEventListener("click", function () {

    body.classList.add("disable_pointer");
    swiper_wrapper.classList.add("disabled");
    processing_animation.classList.add("lds-hourglass");
    processing_animation_div.classList.add("focused");

    face_name_input.value = face_name_input.value.replace(/ /gi, "_");

    // face_encoding_form.submit(function () {});

    response_data = null;
    jquery_manager.post_data("/api/face_encoding", $("#face_encoding_form").serialize());  // .serialize returns the dictionary form data.

    face_name_input.value = "";

    let encode_face_interval = setInterval(function () {
                            console.log(typeof response_data);

        if (response_data !== null) {
            if (response_data["status"] === "OK") {
                console.log(response_data);
                body.classList.remove("disable_pointer");
                swiper_wrapper.classList.remove("disabled");
                processing_animation_div.classList.remove("focused");
                processing_animation.classList.remove("lds-hourglass");

                face_encoding_btn.click();
                face_encoding_btn.click();
            }
            response_data = {};
            clearInterval(encode_face_interval);
        }
    }, 300);
});


let record_control_btn_click_count = 0;

record_control_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, wifi_control_div, audio_control_div, face_encoding_div, empty_option_div, lang_select_div, help_control_div]);
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
                                    console.log(requested_data);

                if (requested_data["status"] === "OK") {
                    record_dates = requested_data["data"];
                    for (let c = 0; c < record_dates.length; c++) {

                        let date_dropdown_div = document.createElement('div');
                        let date_btn = document.createElement('button');
                        let date_dropdown_container_div = document.createElement('div');

                        date_dropdown_div.classList.add("dropdown", "mt-1");

                        date_btn.classList.add("btn", "btn-secondary", "dropdown-toggle");
                        date_btn.type = "button";
                        date_btn.id = record_dates[c] + "_btn";
                        date_btn.setAttribute("data-toggle", "dropdown");
                        date_btn.setAttribute("aria-haspopup", "true");
                        date_btn.setAttribute("aria-expanded", "false");
                        date_btn.innerHTML = record_dates[c].replace(/_/gi, "/"); // to replace all necessary characters.

                        date_dropdown_container_div.classList.add("dropdown-menu", "dropdown-menu-right", "dropdown_menu", "record_dropdown_menu");
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

empty_option_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, wifi_control_div, audio_control_div, face_encoding_div, record_control_div, lang_select_div, help_control_div]);
    empty_option_div.classList.toggle("col");
    empty_option_div.classList.toggle("focused");
    empty_option_div.classList.toggle("higher");
    empty_option_io_div.classList.toggle("focused");
});

lang_select_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, wifi_control_div, audio_control_div, face_encoding_div, record_control_div, empty_option_div, help_control_div]);
    lang_select_div.classList.toggle("col");
    lang_select_div.classList.toggle("focused");
    lang_select_div.classList.toggle("higher");
    language_dropdown_div.classList.toggle("focused");
});

help_control_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, wifi_control_div, audio_control_div, face_encoding_div, record_control_div, empty_option_div, lang_select_div]);
    help_control_div.classList.toggle("col");
    help_control_div.classList.toggle("focused");
    help_control_div.classList.toggle("higher");
    help_control_io_div.classList.toggle("focused");
});
