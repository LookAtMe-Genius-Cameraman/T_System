

const wifi_control_div = document.getElementById("wifi_control_div");
const wifi_connections_btn = document.getElementById("wifi_connections_btn");
const wifi_control_io_div = document.getElementById("wifi_control_io_div");
const network_ssid_input = document.getElementById("network_ssid_input");
const network_password_input = document.getElementById("network_password_input");
const create_new_network_btn = document.getElementById("create_new_network_btn");


// a_i_checkbox.addEventListener("change", function () {  // Checkbox onchange sample
//
//     if (a_i_checkbox.checked){
//     }
//     else {
//     }
//
// });

let wifi_connections_btn_click_count = 0;
wifi_connections_btn.addEventListener("click", function () {
    wifi_connections_btn_click_count++;

    if (wifi_connections_btn_click_count <= 1) {
            // get_network_data();
    //
    // let timer_settings_cont = setInterval(function() {
    //
    //     if (requested_data !== undefined) {
    //
    //         for (let c = 0; c < requested_data.length; c++) {
    //             // console.log(event_db[c]["name"]);
    //             let li = document.createElement('li');
    //             let section = document.createElement('section');
    //
    //             let ssid_output = document.createElement('output');
    //             let password_output = document.createElement('output');
    //
    //             ssid_output.value = requested_data[c]["ssid"];
    //             password_output.value = requested_data[c]["password"];
    //
    //             li.appendChild(section);
    //             section.appendChild(ssid_output);
    //             section.appendChild(password_output);
    //         }
    //
    //         wifi_control_div.style.top = "-5.5rem";
    //         show_element(wifi_control_io_div);
    //
    //             requested_data = undefined;
    //             clearInterval(timer_settings_cont)
    //     }
    //
    //         }, 500);

        wifi_control_div.style.top = "-40%";
        wifi_control_div.style.height = "70%";
        hide_element(system_info_div);
        show_element(wifi_control_io_div);

        jquery_manager.post_data("/try", {"bla": "bla"})

    } else {
        wifi_control_div.style.top = "-20%";
        wifi_control_div.style.height = "40px";
        hide_element(wifi_control_io_div);
        show_element(system_info_div);
        wifi_connections_btn_click_count = 0;
    }

});

function show_create_new_wifi_button() {
    if(network_ssid_input.value !== "" && network_password_input.value !== ""){
        network_ssid_input.classList.add("new_network_input_transition");
        network_password_input.classList.add("new_network_input_transition");
        show_element(create_new_network_btn);
    }
    else {
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

    admin_id = response_data["admin_id"]
});

// new Chart(disk_usage_chart, {
//     "type": "doughnut",
//     "data": {
//         "labels": ["Used", "Free"],
//         "datasets": [{
//             "label": "Disk Usage",
//             "data": [disk_usage_percentage, 100 - disk_usage_percentage],
//             "backgroundColor": [
//                 "rgb(210, 26, 11)",
//                 "rgb(238, 237, 233)"
//             ]
//         }]
//     }
// });


/**
 * The high-level method of getting specified network information with its ssid or the all existing network information.
 * It is triggered via a click on settings_btn or clicked specified network on network list.
 */
function get_network_data(ssid=null) {

    if (ssid){
        timer = setInterval(function() {
                // console.log("bla");
                // console.log(response);

                jquery_manager.get_data("/api/network?ssid=" + ssid + "&admin_id=" + admin_id);

            }, 500);
    }
    else {
        timer = setInterval(function() {
                // console.log("bla");
                // console.log(response);

                jquery_manager.get_data("/api/network?admin_id=" + admin_id);

            }, 500);
    }
}