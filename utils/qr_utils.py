import qrcode
from .. import global_vars as gv


'''
this function takes input data (string) and returns the QR code matrix
see https://pypi.org/project/qrcode/ for full documentation
'''
def get_qr_matrix(data: str):
    qr = qrcode.QRCode(
        # 25% error correction capability
        error_correction=qrcode.constants.ERROR_CORRECT_Q,

        # border around the qr code for improved readability, needs to be closer to white
        border=gv.border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    matrix = qr.get_matrix()

    return matrix


# this functions takes version (should be 1 to 40) and returns the QR code size 
# in number of rows and columns
def temp_get_qr_matrix(ver: int):
    qr = qrcode.QRCode(
        # 25% error correction capability
        error_correction=qrcode.constants.ERROR_CORRECT_Q,

        # border around the qr code for improved readability, needs to be closer to white
        border=gv.border,

        # QR code version
        version=ver
    )
    qr.add_data('hello world')
    qr.make(fit=True)

    # Get matrix
    matrix = qr.get_matrix()

    rows = len(matrix)
    cols = len(matrix[0])

    return (rows, cols)
