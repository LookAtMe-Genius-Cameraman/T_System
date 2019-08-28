// -*- coding: utf-8 -*-

/**
 * @module main
 * @fileoverview the top-level module of T_System that contains the communication methods with python flask of T_System.
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 */

let admin_id = false;
let timer;

let requested_data = null;
let response_data = null;

let interval = 0;

let current_arm_position = {
    "cartesian_coords": [30, 25, 42],
    "polar_coords": [1.5, 1.02, 0.5]
};
