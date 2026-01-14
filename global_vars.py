qr_code_coll = None
module = None
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
qr_matrix_size = 33 # default size for version 3 QR code
qr_matrix_length = qr_matrix_size + (border * 2)
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
