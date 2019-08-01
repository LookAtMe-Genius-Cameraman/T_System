var interval_rotate = 0;
joint_1_cw_btn.addEventListener("mousedown", function () {

    requested_data = {"status": "true", "for": "turn_joint", "reason": "1", "options": "1"}; //reason: 1 means axis1, options: 1 means 1 degree.
    interval_rotate = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.post_data("/fulfill_command", dict);

    }, 300);

});

joint_1_ccw_btn.addEventListener("mousedown", function () {

    requested_data = {"status": "true", "for": "turn_joint", "reason": "1", "options": "-1"}; //tell turn 1 degree.
    interval_rotate = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.post_data("/fulfill_command", dict);

    }, 300);

});
joint_2_cw_btn.addEventListener("mousedown", function () {

    requested_data = {"status": "true", "for": "turn_joint", "reason": "2", "options": "1"}; //tell turn 1 degree.
    interval_rotate = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.post_data("/fulfill_command", dict);

    }, 300);

});
joint_2_ccw_btn.addEventListener("mousedown", function () {

    requested_data = {"status": "true", "for": "turn_joint", "reason": "2", "options": "-1"}; //tell turn 1 degree.
    interval_rotate = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.post_data("/fulfill_command", dict);

    }, 300);

});
joint_3_cw_btn.addEventListener("mousedown", function () {

    requested_data = {"status": "true", "for": "turn_joint", "reason": "3", "options": "1"}
    interval_rotate = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.post_data("/fulfill_command", dict);

    }, 300);

});

joint_3_ccw_btn.addEventListener("mousedown", function () {

    requested_data = {"status": "true", "for": "turn_joint", "reason": "3", "options": "-1"}
    interval_rotate = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.post_data("/fulfill_command", dict);

    }, 300);

});

let elements = [joint_1_cw_btn, joint_1_ccw_btn, joint_2_cw_btn, joint_2_ccw_btn, joint_3_cw_btn, joint_3_ccw_btn];
add_listener_to_elements(elements, "mouseup", function () {
    clearInterval(interval_rotate);
});

function add_listener_to_elements(elements, type, func) {

    for(let i = 0; i<elements.length ;i++){
        elements[i].addEventListener(type, func)
    }

}