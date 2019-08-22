// -*- coding: utf-8 -*-

/**
 * @module system_info
 * @fileoverview the top-level module of T_System that contains the communication methods with python flask of T_System system_info API.
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 */


/** @type {!Element} */
const system_info_template_container = document.getElementById("system_info_template_container");
const system_info_btn = document.getElementById("system_info_btn");
const system_info_chart_div = document.getElementById("system_info_chart_div");
const system_info_chart = document.getElementById('system_info_chart').getContext('2d');
const versions_div = document.getElementById('versions_div');
const stand_version_p = document.getElementById('stand_version_p');
const remote_ui_version_p = document.getElementById('remote_ui_version_p');
const t_system_version_p = document.getElementById('t_system_version_p');


let system_info_btn_click_count = 0;
system_info_btn.addEventListener("click", function () {
    system_info_btn_click_count++;

    if (system_info_btn_click_count <= 1) {
        set_system_info();

        system_info_template_container.classList.toggle("focused");
        dark_deep_background_div.classList.toggle("focused");

        settings_template_container.classList.toggle("hidden_element");
        controlling_template_container.classList.toggle("hidden_element");
        on_work_template_container.classList.toggle("hidden_element");


        show_element(system_info_chart_div);
        show_element(versions_div)

    } else {
        system_info_template_container.classList.toggle("focused");
        dark_deep_background_div.classList.toggle("focused");

        hide_element(system_info_chart_div);
        hide_element(versions_div);

        settings_template_container.classList.toggle("hidden_element");
        controlling_template_container.classList.toggle("hidden_element");
        on_work_template_container.classList.toggle("hidden_element");

        system_info_btn_click_count = 0;
    }
});


/**
 * The low-level method to make specific request for system_info of T_System.
 */
function get_system_info() {
    jquery_manager.get_data("/api/system_info?admin_id=" + admin_id);
}


/**
 * The high-level method to set system info chart/table by administration or normal entry.
 */
function set_system_info() {
    get_system_info();
    // requested_data = {"status": "OK", "data": {"cpu_usage_percent": 15, "cpu_temperature": 37, "ram_usage_percent": 20, "disk_usage_percent": 55, "free_disk_space": 18, "versions": {"t_system": "0.9-alpha1.99", "stand": "0.3", "remote_ui": "1.8.7"}}};
    let timer_settings_cont = setInterval(function () {

        if (requested_data !== null) {
            if (requested_data["status"] === "OK") {

                let disk_usage_percentage = requested_data["data"]["disk_usage_percent"];
                let cpu_usage_percentage = requested_data["data"]["cpu_usage_percent"];
                let ram_usage_percentage = requested_data["data"]["ram_usage_percent"];
                let cpu_temperature = requested_data["data"]["cpu_temperature"];
                let t_system_version = requested_data["data"]["versions"]["t_system"];
                let stand_version = requested_data["data"]["versions"]["stand"];
                let remote_ui_version = requested_data["data"]["versions"]["remote_ui"];

                if (ram_usage_percentage === null) {
                    new Chart(system_info_chart, {
                        "type": "doughnut",
                        "data": {
                            "labels": ["Disk Usage(%)", "Free(%)"],
                            "datasets": [{
                                "label": "Disk Usage",
                                "data": [disk_usage_percentage, 100 - disk_usage_percentage],
                                "backgroundColor": [
                                    "rgb(210, 26, 11)",
                                    "rgb(238, 237, 233)"
                                ],
                                "borderWidth": 5,
                                "borderColor": "rgba(0, 0, 0, 0.5)",
                            }],
                        },
                        "options": {
                            "legend": {
                                "labels": {
                                    "fontColor": "white",
                                    "fontSize": 12
                                }
                            },
                            "segmentShowStroke": true,
                            "segmentStrokeColor": "#fff",
                            "segmentStrokeWidth": 50,
                            "cutoutPercentage": 80,  // thin of the donut as inverse between 50-100.
                            "animation:": {
                                "animationSteps": 100,
                                "animationEasing": "easeOutBounce",
                                "animateRotate": true,
                                "animateScale": true
                            },
                            "responsive": true,
                            "maintainAspectRatio": true,
                            "showScale": true
                        }

                    });
                } else {
                    new Chart(system_info_chart, {
                        "type": "doughnut",
                        "data": {
                            "labels": ["Disk Usage(%)", "Ram Usage(%)", "CPU Usage(%)", "CPU temp.(*C)"],
                            "datasets": [{
                                "label": "System Info",
                                "data": [disk_usage_percentage, ram_usage_percentage, cpu_usage_percentage, cpu_temperature],
                                "backgroundColor": [
                                    "rgb(210, 26, 11)",
                                    "rgb(57, 139, 255)",
                                    "rgb(255, 202, 37)",
                                    "rgb(93, 255, 172)"
                                ],
                                "borderWidth": 5,
                                "borderColor": "rgba(0, 0, 0, 0.5)",
                            }],
                        },
                        "options": {
                            "legend": {
                                "labels": {
                                    "fontColor": "white",
                                    "fontSize": 12
                                }
                            },
                            "segmentShowStroke": true,
                            "segmentStrokeColor": "#fff",
                            "segmentStrokeWidth": 50,
                            "cutoutPercentage": 80,  // thin of the donut as inverse between 50-100.
                            "animation:": {
                                "animationSteps": 100,
                                "animationEasing": "easeOutBounce",
                                "animateRotate": true,
                                "animateScale": true
                            },
                            "responsive": true,
                            "maintainAspectRatio": true,
                            "showScale": true
                        }

                    });
                    stand_version_p.innerHTML = "stand: v" + stand_version;
                    remote_ui_version_p.innerHTML = "remote_ui: v" + remote_ui_version;
                    t_system_version_p.innerHTML = "t_system: v" + t_system_version;
                }
                requested_data = null;
                clearInterval(timer_settings_cont)
            }
        }
    }, 300);
}