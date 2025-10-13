import qrcode
from .. import global_vars as gv

# this function takes input data (string) and returns the QR code matrix
# see https://pypi.org/project/qrcode/ for full documentation
def get_qr_matrix(data: str):
    qr = qrcode.QRCode(
        # 25% error correction capability
        error_correction=qrcode.constants.ERROR_CORRECT_Q,

        # border around the qr code for improved readability, needs to be closer to white
        border=gv.border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Get matrix
    matrix = qr.get_matrix()

    return matrix
