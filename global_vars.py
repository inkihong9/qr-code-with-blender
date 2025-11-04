qr_code_coll = None
white_stone = None
black_stone = None
stone = None
qr_matrix = None
border = 2
# time_interval_description = "amount of frames there should be between series of QR codes before flipping the bits to 'create' the next QR code"
# flip_time_description = "amount of frames the bits will take to flip to 'create' the next QR code"
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

# quick_test = ("Time Interval (1 - 60)", 24, "amount of frames there should be between series of QR codes before flipping the bits to 'create' the next QR code", 1, 60)

# quick_test = {
#         'name':"Time Interval (1 - 60)",
#         'default':24,
#         'description':"amount of frames there should be between series of QR codes before flipping the bits to 'create' the next QR code",
#         'min':1, 
#         'max':60
#     }