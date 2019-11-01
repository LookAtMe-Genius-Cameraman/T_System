// -*- coding: utf-8 -*-

/**
 * @module jsalert
 * @fileoverview the top-level module of T_System that contains the custom alert method of remote_ui of T_System.
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 */


function JSalert(title, text, confirm_btn_text, cancel_btn_text, confirm_function, confirm_text=null) {
    swal({
            title: title,
            text: text,
            icon: "warning",
            buttons: {
                cancel: {
                    text: cancel_btn_text,
                    value: null,
                    visible: true,
                    className: "",
                    closeModal: true,
                },
                confirm: {
                    text: confirm_btn_text,
                    value: true,
                    visible: true,
                    className: "",
                    closeModal: true
                }
            },
            // confirmButtonColor: "#DD6B55",
        }
    ).then(function (isConfirm) {
        if (isConfirm) {
            confirm_function();
            if (confirm_text !== null) {
                swal(translate_text_item("Process Completed!"), "", "success");
            } else {
                swal(confirm_text, "", "success");
            }
        } else {
            // swal("Hurray", "Account is not removed!", "error");
        }
    });
}