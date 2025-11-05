qr_code_coll = None
# white_stone = None
# black_stone = None
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
qr_matrix_size = 33 # default size for version 4 QR code
qr_matrix_length = qr_matrix_size + (border * 2)
qr_matrix_state_map = [
    [False for _ in range(qr_matrix_length)] 
    for _ in range(qr_matrix_length)
]