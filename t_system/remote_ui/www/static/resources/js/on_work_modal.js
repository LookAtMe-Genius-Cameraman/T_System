const on_work_windows_size_select = document.getElementById("on_work_windows_size_select");

/**
 * The high-level method to playing and pausing the streams from t_system.
 */
function playPause() {
  if (stream_area_video.paused)
    stream_area_video.play();
  else
    stream_area_video.pause();
}

/**
 * The high-level method to set size of the video window by given parameter.
 * @param {int} size: size value of window.
 */
function set_window_size(size) {
        stream_area_video.width = size;
}

on_work_windows_size_select.addEventListener("change", function () {

    if (window_size_select.value === "small"){set_window_size(320)}
    else if (window_size_select.value === "normal"){set_window_size(420)}
    else if (window_size_select.value === "big"){set_window_size(560)}

});