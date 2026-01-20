qr_code_coll = None
module = None
qr_matrix = None
quiet_zone = 0
flip_time_input_params = {
    'name' : "Flip Time (1 - 60)",
    'default' : 12,
    'description' : "Number of allocated frames for animating the bit flips",
    'min' : 1, 
    'max' : 60
}
time_interval_input_params = {
    'name' : "Time Interval (1 - 60)",
    'default' : 24,
    'description' : "Number of frames between the different QR codes in the animation",
    'min' : 1, 
    'max' : 60
}
will_include_logo_input_params = {
    'name' : "Will Include Logo?",
    'default' : True,
    'description' : "If flag is turned on, it will make a square hole in the center for logo to go in. Else, such hole will not be made"
}
quiet_zone_input_params = {
    'name' : "Quiet Zone (0 - 5)",
    'default' : 2,
    'description' : "Border (quiet zone) thickness around the QR code",
    'min' : 0, 
    'max' : 5
}
qr_matrix_size = 33 # default size for version 3 QR code
qr_matrix_length = qr_matrix_size + (quiet_zone * 2)
qr_matrix_module_names = [
    ['' for _ in range(qr_matrix_length)] 
    for _ in range(qr_matrix_length)
]
qr_matrix_prev_state = [
    [True for _ in range(qr_matrix_length)] 
    for _ in range(qr_matrix_length)
]
saved_time_interval = 0
saved_flip_time = 0
ivory_white_rgba = (1, 0.939, 0.584, 1)
jet_black_rgba = (0.002, 0.000607, 0.000911, 1)
will_include_logo = True
