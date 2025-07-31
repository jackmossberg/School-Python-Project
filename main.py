from graphics import *
from directory_scraper import *

def cube_mesh() -> Model:
    positions = [
        -1.0, -1.0,  1.0,  1.0, -1.0,  1.0,  1.0,  1.0,  1.0,  -1.0,  1.0,  1.0,
        -1.0, -1.0, -1.0,  1.0, -1.0, -1.0,  1.0,  1.0, -1.0,  -1.0,  1.0, -1.0,
    ]

    indices = [
        0, 1, 2,  2, 3, 0,
        4, 5, 6,  6, 7, 4,
        0, 3, 7,  7, 4, 0,
        1, 5, 6,  6, 2, 1,
        0, 1, 5,  5, 4, 0,
        3, 2, 6,  6, 7, 3,
    ]

    uvs = [
        0.0, 0.0,  1.0, 0.0,  1.0, 1.0,  0.0, 1.0,
        0.0, 0.0,  1.0, 0.0,  1.0, 1.0,  0.0, 1.0,
    ]

    normals = [
        0.0, 0.0, 1.0,  0.0, 0.0, 1.0,  0.0, 0.0, 1.0,  0.0, 0.0, 1.0,
        0.0, 0.0, -1.0,  0.0, 0.0, -1.0,  0.0, 0.0, -1.0,  0.0, 0.0, -1.0,
    ]

    return Mesh(positions=positions, indices=indices, uvs=uvs, normals=normals)

def plane_mesh() -> Model:
    positions = [
        -1.0, -1.0, 0.0,  # Bottom-left
        1.0, -1.0, 0.0,  # Bottom-right
        1.0,  1.0, 0.0,  # Top-right
        -1.0,  1.0, 0.0   # Top-left
    ]

    indices = [
        0, 1, 2,  # First triangle
        2, 3, 0   # Second triangle
    ]

    uvs = [
        0.0, 0.0,  # Bottom-left
        1.0, 0.0,  # Bottom-right
        1.0, 1.0,  # Top-right
        0.0, 1.0   # Top-left
    ]

    normals = [
        0.0, 0.0, 1.0,  # Bottom-left
        0.0, 0.0, 1.0,  # Bottom-right
        0.0, 0.0, 1.0,  # Top-right
        0.0, 0.0, 1.0   # Top-left
    ]

    return Mesh(positions=positions, indices=indices, uvs=uvs, normals=normals)

prev_buffer_size : list = [0]
def forward_button_callback(app : App) -> None:
    if not app.hierarchy_tree.selection():
        return
    
    dir_buffer : str = app.hierarchy_tree.item(app.hierarchy_tree.selection()[0])['text']
    app.selected_directory += dir_buffer + "\\"
    prev_buffer_size.append(len(dir_buffer) + 1)

    app.clear_directories()
    populate_directory_tree(app)

def back_button_callback(app : App) -> None:  
    if len(app.selected_directory) == prev_buffer_size[0]:
        return

    print(len(app.selected_directory))
    print(prev_buffer_size[0])

    app.selected_directory = app.selected_directory[:-prev_buffer_size[len(prev_buffer_size)-1]]
    prev_buffer_size.remove(prev_buffer_size[len(prev_buffer_size)-1])

    app.clear_directories()
    populate_directory_tree(app)

    print(app.selected_directory)

def delete_button_callback(app : App) -> None:
    if not app.hierarchy_tree.selection():
        return
    
    if len(app.selected_directory) == prev_buffer_size[0]:
        return
    
    target_dir : str = app.selected_directory + app.hierarchy_tree.item(app.hierarchy_tree.selection()[0])['text']

    if os.path.exists(target_dir):
        os.remove(target_dir)
        print(f"{target_dir} has been deleted.")
    else:
        print(f"{target_dir} does not exist.")

def rename_button_callback(app : App) -> None:
    print("rename file")

def populate_directory_tree(app : App) -> None:
    app.clear_directories()
    folders = [entry.name for entry in os.scandir(app.selected_directory) if entry.is_dir()]
    for i in folders:
        app.insert_directory(i)

def main() -> None:
    app = App(
        500, 500, 500, 500, 
        True, 'viewport', 
        forward_button_callback,
        back_button_callback, 
        rename_button_callback,
        delete_button_callback
    )

    app.run_directory_popup()

    grid_model = Model(plane_mesh(), 'assets/shaders/default.vert', 'assets/shaders/default.frag',
        0.0, 0.0, 0.0, 
        0.0, 0.0, 0.0, 
        5.0, 5.0, 5.0
    )

    main_camera = Camera(
        45.0, 
        7.0, 7.0, -7.0, 
        0.0, 0.0, 0.0
    )

    inital_pop : bool = True
    while not app.should_app_close():
        if app.selected_directory != "_" and inital_pop == True:
            prev_buffer_size.insert(0, len(app.selected_directory))
            populate_directory_tree(app)
            inital_pop = False

        app.bind()

        grid_model.render(main_camera, app)

        app.unbind()
        app.render(60)

    grid_model.delete()
    pg.quit()

if __name__ == '__main__':
    main()