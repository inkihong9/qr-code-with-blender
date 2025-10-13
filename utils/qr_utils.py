import qrcode

# this function takes input data (string) and returns the QR code matrix
def get_qr_matrix(data: str):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1, # needs to be greater than 0, still have no idea what this is
        border=2,   # border around the qr code for improved readability, needs to be closer to white
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Get matrix
    matrix = qr.get_matrix()

    return matrix
