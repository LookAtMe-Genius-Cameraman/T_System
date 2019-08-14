const system_info_btn = document.getElementById("system_info_btn");
const system_info_chart_div = document.getElementById("system_info_chart_div");
// const disk_usage_chart = document.getElementById('disk_usage_chart').getContext('2d');
const system_info_chart = document.getElementById('system_info_chart').getContext('2d');

system_info_btn.addEventListener("click", function () {
    set_system_info()
});

function get_system_info() {
    jquery_manager.get_data("/api/system_info?admin_id="+ admin_id);
}

function set_system_info() {
    // get_system_info();
    requested_data = {"status": "OK", "data": {"cpu_usage_percent": 15, "cpu_temperature": 37, "ram_usage_percent": 20, "disk_usage_percent": 55, "verisons": {"t_system": "0.9-alpha1.99", "stand": "0.3", "remote_ui": "1.8.7"}}};
    let timer_settings_cont = setInterval(function () {

        if (requested_data !== undefined) {
            if (requested_data["status"] === "OK") {

                let disk_usage_percentage = requested_data["data"]["disk_usage_percent"];
                let cpu_usage_percentage = requested_data["data"]["cpu_usage_percent"];
                let ram_usage_percentage = requested_data["data"]["ram_usage_percent"];
                let cpu_temperature = requested_data["data"]["cpu_temperature"];

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
                                "borderWidth": 5
                            }],
                        },
                        "options": {
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
                                "borderWidth": 5
                            }],
                        },
                        "options": {
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
                }

                requested_data = undefined;
                clearInterval(timer_settings_cont)
            }
        }
    }, 300);
}