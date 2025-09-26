# about
i want this to be a blender add-on where a user inputs data and it creates a 3D image of QR code that can be scanned in real life

# high level algorithm
1. create a single icosphere mesh
2. create black and white materials
3. assign both materials to the icosphere mesh, where top half is black and bottom half is white
4. get the qr code matrix
5. iterate through the qr code matrix
    1. for each row in the matrix: (y-axis)
        1. for each column in the row: (x-axis)
            1. duplicate the mesh created from step 1
            1. move the duplicated mesh to new x and y coordinates, z = 0 always
            1. determine true/false binary value
            1. if true - leave it as is
            1. if false - rotate it 180 degrees along x axis (basically flip it)
            1. increment x by 0.1 meters
        1. increment y by 0.1 meters

# script steps (tbd)
1. create_materials.py
2. create_icosphere_meshes.py

