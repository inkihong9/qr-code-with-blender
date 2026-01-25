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
