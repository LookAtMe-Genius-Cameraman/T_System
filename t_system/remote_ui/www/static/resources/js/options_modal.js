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
const create_wifi_checkbox = document.getElementById("create_wifi_checkbox");
const wifi_control_io_div = document.getElementById("wifi_control_io_div");
const create_new_network = document.getElementById("create_new_network");
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
const lang_select_io_div = document.getElementById("lang_select_io_div");
const lang_select_dd_btn = document.getElementById("lang_select_dd_btn");
const lang_list_ul = document.getElementById("lang_list_ul");

const help_control_div = document.getElementById("help_control_div");
const help_control_btn = document.getElementById("help_control_btn");
const help_control_io_div = document.getElementById("help_control_io_div");

const identity_control_div = document.getElementById("identity_control_div");
const identity_control_btn = document.getElementById("identity_control_btn");
const identity_control_io_div = document.getElementById("identity_control_io_div");
const identity_public_id_div = document.getElementById("identity_public_id_div");
const identity_public_id_span = document.getElementById("identity_public_id_span");
const identity_name_div = document.getElementById("identity_name_div");
const identity_name_span = document.getElementById("identity_name_span");
const identity_private_id_div = document.getElementById("identity_private_id_div");
const identity_private_id_span = document.getElementById("identity_private_id_span");

/**
 * Method to create drop-down language selection menu.
 */
function build_language_menu() {

    let lang_dropdown_row_div;
    for (let i = 0; i < language_list.length; i++) {

        if (i % 2 === 0) {
            lang_dropdown_row_div = document.createElement('div');
            lang_dropdown_row_div.classList.add("position-relative", "row", "lang_row");

            lang_list_ul.appendChild(lang_dropdown_row_div);
        }

        let lang_dropdown_col_div = document.createElement('div');
        lang_dropdown_col_div.classList.add("position-relative", "col-*", "lang_col", "ml-2");


        let lang_div = document.createElement('div');
        let lang_btn = document.createElement('button');

        lang_btn.classList.add("btn", "btn-light", "lang_btn", "cut-text", "mb-2");
        lang_btn.innerHTML = language_list[i][1];

        lang_btn.addEventListener("click", function () {
            translate_text(language_list[i][0].toString(), lang_select_dd_btn);
        });

        lang_div.appendChild(lang_btn);
        lang_dropdown_col_div.appendChild(lang_div);
        lang_dropdown_row_div.appendChild(lang_dropdown_col_div);

        if (language_list[i][0] === language) {
            lang_select_dd_btn.innerHTML = language_list[i][1];
        }
    }
}

function close_opened_option(option_btn) {
    if (event.target === event.currentTarget) {
        option_btn.click();
    } else {
    }
}


let update_control_btn_click_count = 0;
let update_control_btn_lis_bind = close_opened_option.bind(null, update_control_btn);

update_control_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([wifi_control_div, audio_control_div, face_encoding_div, record_control_div, identity_control_div, lang_select_div, help_control_div]);
    update_control_div.classList.toggle("col");
    update_control_div.classList.toggle("focused");
    update_control_div.classList.toggle("higher");
    update_control_io_div.classList.toggle("focused");

    update_control_btn_click_count++;
    if (update_control_btn_click_count <= 1) {

        dark_deep_background_div.addEventListener("click", update_control_btn_lis_bind);
        options_template_container.addEventListener("click", update_control_btn_lis_bind);

        setSwiperSwiping(false);

        request_asynchronous('/api/network?key=auto_update&admin_id=' + admin_id, 'GET',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
                if (err === "success") {
                    if (requested_data["status"] === "OK") {
                        auto_update_checkbox.checked = requested_data["data"] === true;
                    }
                }
            });

    } else {
        dark_deep_background_div.removeEventListener("click", update_control_btn_lis_bind);
        options_template_container.removeEventListener("click", update_control_btn_lis_bind);

        $('#swiper_wrapper').removeClass("disabled");

        update_control_btn_click_count = 0;
    }
});

auto_update_checkbox.addEventListener("change", function () {
    if (auto_update_checkbox.checked) {
        let data = {"auto_update": true};

        request_asynchronous('/api/update?admin_id=' + admin_id, 'PUT',
            'application/x-www-form-urlencoded; charset=UTF-8', data, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });
    } else {
        let data = {"auto_update": false};

        request_asynchronous('/api/update?admin_id=' + admin_id, 'PUT',
            'application/x-www-form-urlencoded; charset=UTF-8', data, function (req, err, response) {
                if (err === "success") {
                    let response_data = JSON.parse(response.responseText);
                }
            });
    }
});

update_btn.addEventListener("click", function () {
    // Todo: Response will handled. for response arrive, button will be disabled. and maybe for update completed, Remote UI will sleep, shutdown or locked. decide that.

    request_asynchronous('/api/update?admin_id=' + admin_id, 'POST',
        'application/x-www-form-urlencoded; charset=UTF-8', {}, function (req, err, response) {
            if (err === "success") {
                let response_data = JSON.parse(response.responseText);
            }
        });
});

let wifi_connections_btn_click_count = 0;
let wifi_connections_btn_lis_bind = close_opened_option.bind(null, wifi_connections_btn);

wifi_connections_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, audio_control_div, face_encoding_div, record_control_div, identity_control_div, lang_select_div, help_control_div]);
    wifi_control_div.classList.toggle("col");
    wifi_control_div.classList.toggle("focused");
    wifi_control_div.classList.toggle("higher");
    wifi_control_io_div.classList.toggle("focused");

    wifi_connections_btn_click_count++;
    if (wifi_connections_btn_click_count <= 1) {

        dark_deep_background_div.addEventListener("click", wifi_connections_btn_lis_bind);
        options_template_container.addEventListener("click", wifi_connections_btn_lis_bind);

        setSwiperSwiping(false);

        request_asynchronous('/api/network?admin_id=' + admin_id, 'GET',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
                // err = "success";
                // requested_data = {"status": "OK", "data": [{"ssid": "Beyaz", "password": "arge"}, {"ssid": "new_wifi", "password": "1234"}, {"ssid": "demo", "password": "bla"}]};
                if (err === "success") {
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

                                request_asynchronous('/api/network?ssid=' + network_connections[c]["ssid"] + '&admin_id=' + admin_id, 'PUT',
                                    'application/x-www-form-urlencoded; charset=UTF-8', data, function (req, err, response) {
                                        if (err === "success") {
                                            let response_data = JSON.parse(response.responseText);
                                        }
                                    });

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
                }
            });

        request_asynchronous('/api/network?activity=' + true + '&admin_id=' + admin_id, 'GET',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
                // err = "success";
                // requested_data = {"status": "OK", "data": true};
                if (err === "success") {
                    if (requested_data["status"] === "OK") {
                        let activity = requested_data["data"];

                        if (activity) {
                            create_wifi_checkbox.checked = false
                        } else {
                            create_wifi_checkbox.checked = true;
                            create_new_network.classList.add("disabled");
                            network_list_ul.classList.add("disabled");
                        }
                    }
                }
            });

    } else {
        dark_deep_background_div.removeEventListener("click", wifi_connections_btn_lis_bind);
        options_template_container.removeEventListener("click", wifi_connections_btn_lis_bind);

        clearElement(network_list_ul);

        setSwiperSwiping(true);

        wifi_connections_btn_click_count = 0;
    }
});

create_wifi_checkbox.setAttribute("data-on", translate_text_item(" "));
create_wifi_checkbox.setAttribute("data-off", translate_text_item(" "));

$('#create_wifi_checkbox').change(function () {
    let data = {};

    request_asynchronous('/api/network?activity=' + create_wifi_checkbox.checked, 'POST',
        'application/x-www-form-urlencoded; charset=UTF-8', data, function (req, err, response) {
            if (err === "success") {
                let response_data = JSON.parse(response.responseText);
            }
        });

    if (create_wifi_checkbox.checked) {
        create_new_network.classList.add("disabled");
        network_list_ul.classList.add("disabled");
    } else {
        create_new_network.classList.remove("disabled");
        network_list_ul.classList.remove("disabled");
    }
    swal(translate_text_item("This process will be the effect after reboot!"), "", "info");
});

network_pass_eye_span.addEventListener("click", function () {
    network_pass_eye_span.classList.toggle("fa-eye fa-eye-slash");
    if (network_password_input.type === 'password') {
        network_password_input.setAttribute('type', 'text');
    } else {
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

    let data = {"ssid": network_ssid_input.value, "password": network_password_input.value};

    request_asynchronous('/api/network', 'POST',
        'application/x-www-form-urlencoded; charset=UTF-8', data, function (req, err, response) {
            if (err === "success") {
                let response_data = JSON.parse(response.responseText);
                if (response_data["status"] === "OK") {
                    wifi_connections_btn.click();
                    wifi_connections_btn.click();

                    admin_id = response_data["admin_id"];
                    activateAdminAuthorityBy(admin_id);
                }
            }
        });

    network_ssid_input.value = "";
    network_password_input.value = "";
});

let audio_control_btn_click_count = 0;
let audio_control_btn_lis_bind = close_opened_option.bind(null, audio_control_btn);

audio_control_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    toggle_elements([update_control_div, wifi_control_div, face_encoding_div, record_control_div, identity_control_div, lang_select_div, help_control_div]);
    audio_control_div.classList.toggle("col");
    audio_control_div.classList.toggle("focused");
    audio_control_div.classList.toggle("higher");
    audio_control_io_div.classList.toggle("focused");

    audio_control_btn_click_count++;
    if (audio_control_btn_click_count <= 1) {
        dark_deep_background_div.addEventListener("click", audio_control_btn_lis_bind);
        options_template_container.addEventListener("click", audio_control_btn_lis_bind);

        setSwiperSwiping(false);

    } else {
        dark_deep_background_div.removeEventListener("click", audio_control_btn_lis_bind);
        options_template_container.removeEventListener("click", audio_control_btn_lis_bind);

        setSwiperSwiping(true);

        audio_control_btn_click_count = 0;
    }
});

let face_encoding_btn_click_count = 0;
let face_encoding_btn_lis_bind = close_opened_option.bind(null, face_encoding_btn);

face_encoding_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    toggle_elements([update_control_div, wifi_control_div, audio_control_div, record_control_div, identity_control_div, lang_select_div, help_control_div]);
    face_encoding_div.classList.toggle("col");
    face_encoding_div.classList.toggle("focused");
    face_encoding_div.classList.toggle("higher");
    face_encoding_io_div.classList.toggle("focused");

    face_encoding_btn_click_count++;
    if (face_encoding_btn_click_count <= 1) {

        dark_deep_background_div.addEventListener("click", face_encoding_btn_lis_bind);
        options_template_container.addEventListener("click", face_encoding_btn_lis_bind);

        setSwiperSwiping(false);

        request_asynchronous('/api/face_encoding?admin_id=' + admin_id, 'GET',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
                // err = "success";
                // requested_data = {"status": "OK", "data": [{"id": "z970136a-aegb-15e9-b130-cy2f756671ed", "name": "face_name", "image_names": ["im-n1", "im-n2", "im-n3", "im-n4", "im-n5"]}]};

                if (err === "success") {
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

                            face_dropdown_container_div.classList.add("dropdown-menu", "dropdown-menu-right", "dropdown_menu", "face_encoding_dropdown_menu", "container");
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

                                        request_asynchronous(route, 'GET',
                                            'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
                                                if (err === "success") {
                                                }
                                            });
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
                }
            });

    } else {

        dark_deep_background_div.removeEventListener("click", face_encoding_btn_lis_bind);
        options_template_container.removeEventListener("click", face_encoding_btn_lis_bind);

        clearElement(encoded_face_list_ul);

        setSwiperSwiping(true);

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

    request_asynchronous('/api/face_encoding?admin_id=' + admin_id, 'POST',
        'application/x-www-form-urlencoded; charset=UTF-8', $("#face_encoding_form").serialize(), function (req, err, response) {  // .serialize returns the dictionary form data.
            if (err === "success") {
                let response_data = JSON.parse(response.responseText);

                if (response_data["status"] === "OK") {
                    body.classList.remove("disable_pointer");
                    swiper_wrapper.classList.remove("disabled");
                    processing_animation_div.classList.remove("focused");
                    processing_animation.classList.remove("lds-hourglass");

                    face_encoding_btn.click();
                    face_encoding_btn.click();
                }
            }
        });

    face_name_input.value = "";

});


let record_control_btn_click_count = 0;
let record_control_btn_lis_bind = close_opened_option.bind(null, record_control_btn);

record_control_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, wifi_control_div, audio_control_div, face_encoding_div, identity_control_div, lang_select_div, help_control_div]);
    record_control_div.classList.toggle("col");
    record_control_div.classList.toggle("focused");
    record_control_div.classList.toggle("higher");
    record_control_io_div.classList.toggle("focused");

    record_control_btn_click_count++;
    if (record_control_btn_click_count <= 1) {

        dark_deep_background_div.addEventListener("click", record_control_btn_lis_bind);
        options_template_container.addEventListener("click", record_control_btn_lis_bind);

        setSwiperSwiping(false);

        request_asynchronous('/api/record?admin_id=' + admin_id, 'GET',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
                // err = "success"
                // requested_data = {"status": "OK", "data": ["22_05_2019", "23_05_2019", "27_05_2019", "27_05_2019", "27_05_2019", "27_05_2019", "27_05_2019", "27_05_2019", "27_05_2019"]};
                if (err === "success") {
                    if (requested_data["status"] === "OK") {
                        let record_dates = requested_data["data"];

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

                                clearElement(date_dropdown_container_div);

                                request_asynchronous('/api/record?date=' + record_dates[c] + '&admin_id=' + admin_id, 'GET',
                                    'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
                                        // err = "success"
                                        // requested_data = {"status": "OK", "data": [{"id": "b970138a-argb-11e9-b145-cc2f844671ed", "name": "record_name", "time": "12_27_54", "length": 180, "extension": "mp4"}]};
                                        if (err === "success") {
                                            if (requested_data["status"] === "OK") {
                                                let records = requested_data["data"];

                                                for (let i = 0; i < records.length; i++) {
                                                    let record_div = document.createElement('div');
                                                    let record_a = document.createElement('a');
                                                    let record_time_span = document.createElement('span');
                                                    let record_length_span = document.createElement('span');

                                                    record_div.classList.add("dropdown-item", "position-relative");
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
                                        }
                                    });
                            });
                            date_dropdown_div.appendChild(date_btn);
                            date_dropdown_div.appendChild(date_dropdown_container_div);

                            record_list_ul.appendChild(date_dropdown_div);
                        }
                    }
                }
            });

    } else {

        if (options_player_div.classList.contains("focused")) {
            close_options_player_btn.click();
        }

        dark_deep_background_div.removeEventListener("click", record_control_btn_lis_bind);
        options_template_container.removeEventListener("click", record_control_btn_lis_bind);

        clearElement(record_list_ul);

        setSwiperSwiping(true);

        record_control_btn_click_count = 0;
    }
});

close_options_player_btn.addEventListener("click", function () {
    options_player_div.classList.toggle("focused");
    options_player_source.src = "";
    record_control_div.classList.toggle("hidden_element");
});

let identity_control_btn_click_count = 0;
let identity_control_btn_lis_bind = close_opened_option.bind(null, identity_control_btn);

identity_control_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, wifi_control_div, audio_control_div, face_encoding_div, record_control_div, lang_select_div, help_control_div]);
    identity_control_div.classList.toggle("col");
    identity_control_div.classList.toggle("focused");
    identity_control_div.classList.toggle("higher");
    identity_control_io_div.classList.toggle("focused");

    identity_public_id_div.classList.toggle("identity_div");
    identity_private_id_div.classList.toggle("identity_div");
    identity_name_div.classList.toggle("identity_div");

    identity_control_btn_click_count++;
    if (identity_control_btn_click_count <= 1) {
        dark_deep_background_div.addEventListener("click", identity_control_btn_lis_bind);
        options_template_container.addEventListener("click", identity_control_btn_lis_bind);

        setSwiperSwiping(false);

        request_asynchronous('/api/identity?admin_id=' + admin_id, 'GET',
            'application/x-www-form-urlencoded; charset=UTF-8', null, function (requested_data, err) {
                if (err === "success") {
                    if (requested_data["status"] === "OK") {
                        let identity_info = requested_data["data"];

                        identity_public_id_span.classList.add("pale");
                        identity_public_id_span.innerHTML = identity_info["public_id"];
                        identity_public_id_span.title = identity_info["public_id"];

                        identity_name_span.innerHTML = identity_info["name"];
                        identity_name_span.title = identity_info["name"];

                        identity_name_span.addEventListener("click", function () {

                            identity_name_div.removeChild(identity_name_span);

                            let identity_name_input = document.createElement('input');

                            identity_name_input.type = "text";
                            identity_name_input.placeholder = identity_name_span.innerHTML;
                            identity_name_input.classList.add("identity_update_input");

                            identity_name_input.addEventListener("focusout", function () {
                                if (identity_name_input.value !== identity_name_span.innerHTML && identity_name_input.value !== "") {

                                    let data = {"public_id": null, "private_id": null, "name": identity_name_input.value};

                                    request_asynchronous('/api/identity?cause=name&admin_id=' + admin_id, 'PUT',
                                        'application/json; charset=UTF-8', data, function (req, err, response) {
                                            if (err === "success") {
                                                let response_data = JSON.parse(response.responseText);
                                                if (response_data["status"] === "OK") {
                                                    swal(translate_text_item("Device Name is now:") + "\n" + translate_text_item(identity_name_input.value), "", "success");
                                                    identity_name_span.innerHTML = identity_name_input.value
                                                } else if (response_data["status"] === "ERROR") {
                                                    swal(translate_text_item("Device Name changing failed!"), "", "error");
                                                }
                                            }
                                        });
                                }
                                identity_name_div.removeChild(identity_name_input);
                                identity_name_div.appendChild(identity_name_span);
                            });
                            identity_name_div.appendChild(identity_name_input);
                            identity_name_input.focus();
                        });

                        if (identity_info["private_id"] != null) {

                            identity_public_id_span.classList.remove("pale");

                            identity_public_id_span.addEventListener("click", function () {

                                identity_public_id_div.removeChild(identity_public_id_span);

                                let identity_public_id_input = document.createElement('input');

                                identity_public_id_input.type = "text";
                                identity_public_id_input.placeholder = identity_public_id_span.innerHTML;
                                identity_public_id_input.classList.add("identity_update_input");

                                identity_public_id_input.addEventListener("focusout", function () {
                                    if (identity_public_id_input.value !== identity_public_id_span.innerHTML && identity_public_id_input.value !== "") {

                                        let data = {"public_id": identity_public_id_input.value, "private_id": null, "name": null};

                                        request_asynchronous('/api/identity?cause=public_id&admin_id=' + admin_id, 'PUT',
                                            'application/json; charset=UTF-8', data, function (req, err, response) {
                                                if (err === "success") {
                                                    let response_data = JSON.parse(response.responseText);
                                                    if (response_data["status"] === "OK") {
                                                        swal(translate_text_item("Device Public ID is now:") + "\n" + translate_text_item(identity_public_id_input.value), "", "success");
                                                        identity_public_id_span.innerHTML = identity_public_id_input.value
                                                    } else if (response_data["status"] === "ERROR") {
                                                        swal(translate_text_item("Device Public ID changing failed!"), "", "error");
                                                    }
                                                }
                                            });
                                    }
                                    identity_public_id_div.removeChild(identity_public_id_input);
                                    identity_public_id_div.appendChild(identity_public_id_span);
                                });
                                identity_public_id_div.appendChild(identity_public_id_input);
                                identity_public_id_input.focus();
                            });

                            identity_private_id_div.classList.add("active");
                            identity_private_id_span.innerHTML = identity_info["private_id"];
                            identity_private_id_span.title = identity_info["private_id"];

                            identity_private_id_span.addEventListener("click", function () {

                                identity_private_id_div.removeChild(identity_private_id_span);

                                let identity_private_id_input = document.createElement('input');

                                identity_private_id_input.type = "text";
                                identity_private_id_input.placeholder = identity_private_id_span.innerHTML;
                                identity_private_id_input.classList.add("identity_update_input");

                                identity_private_id_input.addEventListener("focusout", function () {
                                    if (identity_private_id_input.value !== identity_private_id_span.innerHTML && identity_private_id_input.value !== "") {

                                        let data = {"public_id": null, "private_id": identity_private_id_input.value, "name": null};

                                        request_asynchronous('/api/identity?cause=private_id&admin_id=' + admin_id, 'PUT',
                                            'application/json; charset=UTF-8', data, function (req, err, response) {
                                                if (err === "success") {
                                                    let response_data = JSON.parse(response.responseText);
                                                    if (response_data["status"] === "OK") {
                                                        swal(translate_text_item("Device Private ID is now:") + "\n" + translate_text_item(identity_private_id_input.value), "", "success");
                                                        identity_private_id_span.innerHTML = identity_private_id_input.value;
                                                    } else if (response_data["status"] === "ERROR") {
                                                        swal(translate_text_item("Device Private ID changing failed!"), "", "error");
                                                    }
                                                }
                                            });
                                    }
                                    identity_private_id_div.removeChild(identity_private_id_input);
                                    identity_private_id_div.appendChild(identity_private_id_span);
                                });
                                identity_private_id_div.appendChild(identity_private_id_input);
                                identity_private_id_input.focus();
                            });
                        }
                    }
                }
            });
    } else {
        identity_public_id_span.innerHTML = "";
        identity_name_span.innerHTML = "";
        identity_private_id_span.innerHTML = "";

        dark_deep_background_div.removeEventListener("click", identity_control_btn_lis_bind);
        options_template_container.removeEventListener("click", identity_control_btn_lis_bind);

        setSwiperSwiping(true);

        identity_control_btn_click_count = 0;
    }
});

let lang_select_btn_click_count = 0;
let lang_select_btn_lis_bind = close_opened_option.bind(null, lang_select_btn);

lang_select_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, wifi_control_div, audio_control_div, face_encoding_div, record_control_div, identity_control_div, help_control_div]);
    lang_select_div.classList.toggle("col");
    lang_select_div.classList.toggle("focused");
    lang_select_div.classList.toggle("higher");
    lang_select_io_div.classList.toggle("focused");

    lang_select_btn_click_count++;
    if (lang_select_btn_click_count <= 1) {
        dark_deep_background_div.addEventListener("click", lang_select_btn_lis_bind);
        options_template_container.addEventListener("click", lang_select_btn_lis_bind);

        setSwiperSwiping(false);

    } else {
        dark_deep_background_div.removeEventListener("click", lang_select_btn_lis_bind);
        options_template_container.removeEventListener("click", lang_select_btn_lis_bind);

        setSwiperSwiping(true);

        lang_select_btn_click_count = 0;
    }
});

let help_control_btn_click_count = 0;
let help_control_btn_lis_bind = close_opened_option.bind(null, help_control_btn);

help_control_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, wifi_control_div, audio_control_div, face_encoding_div, record_control_div, identity_control_div, lang_select_div]);
    help_control_div.classList.toggle("col");
    help_control_div.classList.toggle("focused");
    help_control_div.classList.toggle("higher");
    help_control_io_div.classList.toggle("focused");

    help_control_btn_click_count++;
    if (help_control_btn_click_count <= 1) {
        dark_deep_background_div.addEventListener("click", help_control_btn_lis_bind);
        options_template_container.addEventListener("click", help_control_btn_lis_bind);

        setSwiperSwiping(false);
    } else {
        dark_deep_background_div.removeEventListener("click", help_control_btn_lis_bind);
        options_template_container.removeEventListener("click", help_control_btn_lis_bind);

        setSwiperSwiping(true);

        help_control_btn_click_count = 0;
    }
});
