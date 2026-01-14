qr_code_coll = None
stone = None
qr_matrix = None
border = 4
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
module_size_input_params = {
    'name' : "Module Size",
    'default' : 0.1,
    'description' : "Number of frames between the different QR codes in the animation",
    'min' : 0.1,
    'max' : 1
}
padding_input_params = {
    'name' : "Padding",
    'default' : 0.01,
    'description' : "Number of frames between the different QR codes in the animation",
    'min' : 0, 
    'max' : 0.1
}
spacing_input_params = {
    'name' : "Time Interval (1 - 60)",
    'default' : 0.01,
    'description' : "Number of frames between the different QR codes in the animation",
    'min' : 0, 
    'max' : 0.1
}


qr_matrix_size = 33 # default size for version 3 QR code
qr_matrix_length = qr_matrix_size + (border * 2)
qr_matrix_stone_names = [
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
