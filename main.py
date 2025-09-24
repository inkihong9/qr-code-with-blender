import qrcode

# rickroll ppl data
data = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Create QR code object
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,
    border=2,  # extra border helps scanners
)
qr.add_data(data)
qr.make(fit=True)

# Get matrix
matrix = qr.get_matrix()

# Print ASCII QR code
for row in matrix:
    line = "".join("██" if col else "  " for col in row)
    print(line)