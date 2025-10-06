import qrcode

# this function takes input data (string) and returns the QR code matrix
def get_qr_matrix(data: str):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=2,  # extra border helps scanners
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Get matrix
    matrix = qr.get_matrix()

    return matrix
