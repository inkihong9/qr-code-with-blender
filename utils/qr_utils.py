import qrcode
from .. import global_vars as gv


'''
this function takes input data (string) and returns the QR code matrix
see https://pypi.org/project/qrcode/ for full documentation
'''
def get_qr_matrix(data: str, ver=None):
    error_correction = qrcode.constants.ERROR_CORRECT_Q if gv.will_include_logo else qrcode.constants.ERROR_CORRECT_L

    qr = qrcode.QRCode(
        # 25% error correction capability
        error_correction=error_correction,

        # quite zone - border around the qr code for improved readability
        border=gv.quiet_zone,

        version=ver
    )
    qr.add_data(data)
    qr.make(fit=True)

    # get qr code version, qr code matrix
    return qr.version, qr.modules_count, qr.get_matrix()


# this functions takes version (should be 1 to 40) and returns the QR code size 
# in number of rows and columns
def temp_get_qr_matrix(ver: int):
    qr = qrcode.QRCode(
        # 25% error correction capability
        error_correction=qrcode.constants.ERROR_CORRECT_Q,

        # border around the qr code for improved readability, needs to be closer to white
        border=gv.quiet_zone,

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
