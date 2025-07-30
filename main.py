from graphics import *
from directory_scraper import *

def forward_button_callback() -> None:
    print("-->")

def back_button_callback() -> None:
    print("<--")

def delete_button_callback() -> None:
    print("deleted fpath")

def rename_button_callback() -> None:
    print("rename file")

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

def main():
    app = App(
        500, 500, 500, 500, 
        True, 'viewport', 
        forward_button_callback,
        back_button_callback, 
        rename_button_callback, 
        delete_button_callback
    )
    for i in range(10):
        app.insert_directory(f"some folder {i}")

    test_model = Model(plane_mesh(), 'assets/shaders/default.vert', 'assets/shaders/default.frag',
        0.0, 0.0, 0.0, 
        0.0, 0.0, 0.0, 
        5.0, 5.0, 5.0
    )

    main_camera = Camera(
        45.0, 
        7.0, 7.0, -7.0, 
        0.0, 0.0, 0.0
    )

    while not app.should_app_close():
        app.bind()
        test_model.render(main_camera, app)
        app.unbind()
        app.render(60)

    test_model.delete()
    pg.quit()

if __name__ == '__main__':
    main()