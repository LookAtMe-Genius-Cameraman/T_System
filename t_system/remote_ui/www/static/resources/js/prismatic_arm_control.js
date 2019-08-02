let interval = 0;
x_up_btn.addEventListener("mousedown", function () {

    requested_data = {"status": "true", "for": "move_endpoint", "reason": "x", "options": "10"}; //reason: x means x axis, options: 1 means 10 mm.

    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.post_data("/api/scenario?id=<ID>&admin_id=<admin_id>", dict);

    }, 300);

});

x_down_btn.addEventListener("mousedown", function () {

    requested_data = {"status": "true", "for": "move_endpoint", "reason": "x", "options": "-10"};
    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.post_data("/api/scenario?id=<ID>&admin_id=<admin_id>", dict);

    }, 300);

});
y_up_btn.addEventListener("mousedown", function () {

    requested_data = {"status": "true", "for": "move_endpoint", "reason": "y", "options": "10"};
    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.post_data("/api/scenario?id=<ID>&admin_id=<admin_id>", dict);

    }, 300);

});
y_down_btn.addEventListener("mousedown", function () {

    requested_data = {"status": "true", "for": "move_endpoint", "reason": "y", "options": "-10"};
    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.post_data("/api/scenario?id=<ID>&admin_id=<admin_id>", dict);

    }, 300);

});
z_up_btn.addEventListener("mousedown", function () {

    requested_data = {"status": "true", "for": "move_endpoint", "reason": "z", "options": "10"};
    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.post_data("/api/scenario?id=<ID>&admin_id=<admin_id>", dict);

    }, 300);

});

z_down_btn.addEventListener("mousedown", function () {

    requested_data = {"status": "true", "for": "move_endpoint", "reason": "z", "options": "-10"};
    interval = setInterval(function () {
        // console.log("gönderdi");
        jquery_manager.post_data("/api/scenario?id=<ID>&admin_id=<admin_id>", dict);

    }, 300);

});

let elements = [x_up_btn, x_down_btn, y_up_btn, y_down_btn, z_up_btn, z_down_btn];
add_listener_to_elements(elements, "mouseup", function () {
    clearInterval(interval);
});

function add_listener_to_elements(elements, type, func) {

    for(let i = 0; i<elements.length ;i++){
        elements[i].addEventListener(type, func)
    }

}