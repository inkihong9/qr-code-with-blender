# about
i want this to be a blender add-on where a user inputs data and it creates a 3D image of QR code that can be scanned in real life

# setup
1. after blender is installed, update PATH environment variable by adding a full path to the directory containing blender executable file (e.g., `C:\Program Files\Blender Foundation\Blender 4.5`)
2. make sure this extension is installed in vscode - https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development (i'm syncing settings, so it'll be installed automatically in local machine)

# develop and debug addon in vscode:
1. make sure this extension is installed in vscode - https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development (i'm syncing settings, so it'll be installed automatically in local machine)
    1. if i need to create a brand new addon: Ctrl + Shift + P > Blender: New Addon
    2. after inputting to the prompts, it will create a skeleton addon as follows:
    ```
    my_simple_addon/
        __init__.py
        blender_manifest.toml
    ```
2. vscode needs to start and connect to a running instance of blender: Ctrl + Shift + P > Blender: Build and Start > input full path to blender executable file
    1. this seems to automatically install my extension, if not, then go to Edit > Preferences > Add-ons > install from disk
    2. make sure your add-on is enabled
3. in blender, go to Edit > Preferences > Save & Load > "Auto Run Python Scripts" (enable)
4. to reload the add-on changes (most likely python script changes), in blender, press F3 > type "Reload Scripts" > press Enter

# to build an addon
1. in the `qr_code_maker` directory, run command `blender --command extension build`
2. this is gonna create a new zip file named `qr_code_maker-1.0.0.zip` (version specified in the manifest file is 1.0.0, so it's probably that)

# to install additional pip packages
1. `libs` folder must exist in the same directory as this script
2. run command `python3 -m pip install <package_name> -t ./libs`

# rules and discipline
1. use of chatgpt or copilot (or any other preferred AI tool) is encouraged
2. **IMPORTANT** review the code and spend time to understand **AND** document the code it generates!!
3. think through the steps and algorithm, and work on it in small chunk at a time instead of throwing everything into the AI and expect it to magically "know" your plan from start to finish

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

# helpful links
[how to build extensions](https://docs.blender.org/manual/en/4.2/advanced/extensions/getting_started.html)
<br />
[blender python api](https://docs.blender.org/api/current/index.html)
