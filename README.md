# about
i want this to be a blender add-on where a user inputs data and it creates a 3D image of QR code that can be scanned in real life

# rules and discipline
1. use of chatgpt or copilot (or any other preferred AI tool) is encouraged
2. **IMPORTANT** review the code and spend time to understand **AND** document the code it generates!!
3. think through the steps and algorithm, and work on it in small chunk at a time instead of throwing everything into the AI and expect it to magically "know" your plan from start to finish

# folder structure
root directory of the repo should contain a docker-compose.yml file, Dockerfile, README.md, and then the root directory of the add-on that i will make
<br />

it's really important that add-on's root directory name should be alpha-numeric with underscores ( _ ), should NOT use dashes ( - )
<br />

for example:
<br />
`my_simple_addon < correct`
<br />
`my-simple-addon < WRONG`
<br />
see below for the simple folder structure
```
my_simple_addon/
    __init__.py
    script1.py
    script2.py

my_simple_addon.zip 
```

# high level algorithm
1. cleanup the scene
1. create a single uv_sphere mesh
2. create black and white materials
3. assign both materials to the uv_sphere mesh, where top half is black and bottom half is white
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
1. cleanup_scene.py (step 1)
2. create_stone.py (step 2)
3. create_materials.py (step 3)

