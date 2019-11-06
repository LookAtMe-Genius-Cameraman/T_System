// -*- coding: utf-8 -*-

/**
 * @module main
 * @fileoverview the top-level module of T_System that contains the communication methods with python flask of T_System.
 * @author cem.baybars@gmail.com (Cem Baybars GÜÇLÜ)
 */

let admin_id = false;
let allow_root = false;

let interval = 0;

let dark_overlay_active = false;

let current_arm_position = {};

let action_db_name = "missions";