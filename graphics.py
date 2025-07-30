# graphics specific functionality
# angel / jack - we will write some basic opengl graphics functions here.
# won't be to complex, all thats really needed are some cubes.
# ideally we should be done with this by today. Tommorow at the latest

# I need a function that can generate VAO's from a list of positions, indices, uvs, and normals. 
# it would look somthing like this
# ex :
# generate_vao(positions : list, indices : list, uvs : list, normals : list) -> int:
# if you could get this done by the end of today that would be great.

import pygame as pg
from OpenGL.GL import *
import sys
import numpy as np
from math import sin, cos, radians
from pyrr import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import os


def generate_vao(positions, indices, uvs=None, normals=None):
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    position_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, position_vbo)
    glBufferData(GL_ARRAY_BUFFER, np.array(positions, dtype=np.float32), GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    if uvs is not None:
        uv_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, uv_vbo)
        glBufferData(GL_ARRAY_BUFFER, np.array(uvs, dtype=np.float32), GL_STATIC_DRAW)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)
    if normals is not None:
        normal_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, normal_vbo)
        glBufferData(GL_ARRAY_BUFFER, np.array(normals, dtype=np.float32), GL_STATIC_DRAW)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(2)
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, np.array(indices, dtype=np.uint32), GL_STATIC_DRAW)
    
    glBindVertexArray(0)

    return vao

# generate_shader(vertex_file_path : str, fragment_file_path : str) -> int:
def generate_shader(vertex_file_path: str, fragment_file_path: str) -> int:
    try:
        with open(vertex_file_path, 'r') as vertex_file:
            vertex_shader_source = vertex_file.read()
        
        with open(fragment_file_path, 'r') as fragment_file:
            fragment_shader_source = fragment_file.read()
        
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vertex_shader_source)
        glCompileShader(vertex_shader)
        
        if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(vertex_shader).decode()
            raise RuntimeError(f"Vertex shader compilation failed: {error}")
            
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_shader_source)
        glCompileShader(fragment_shader)

        if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment_shader).decode()
            raise RuntimeError(f"Fragment shader compilation failed: {error}")

        shader_program = glCreateProgram()
        glAttachShader(shader_program, vertex_shader)
        glAttachShader(shader_program, fragment_shader)
        glLinkProgram(shader_program)

        if not glGetProgramiv(shader_program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(shader_program).decode()
            raise RuntimeError(f"Shader program linking failed: {error}")

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        
        return shader_program
    except Exception as e:
        print(f"Error generating shader: {e}")
        return -1


class App():
    def __init__(self, 
            width : int, 
            height : int, 
            fwidth : int, 
            fheight : int, 
            resizable : bool, 
            title : str, 
            forward_button_callback,
            backward_button_callback,
            rename_button_callback,
            delete_button_callback
        ) -> None:
        self.__should_close = False
        self.window_width = width
        self.window_height = height
        self.frame_width = fwidth
        self.frame_height = fheight
        self.window_rgba_texture = 0

        self.__should_close = False
        self.__window_frame = 0
        self.__window_quad = 0
        self.__window_shader = 0
        self.__window_resizable = resizable
        self.__window_title = title

        self.forward_button_callback = forward_button_callback
        self.backward_button_callback = backward_button_callback
        self.rename_button_callback = rename_button_callback
        self.delete_button_callback = delete_button_callback

        pg.init()
        pg.display.set_mode(size= (self.window_width, self.window_height), flags= pg.OPENGL | pg.DOUBLEBUF | pg.HIDDEN)
        pg.display.set_caption(self.__window_title)

        self.clock = pg.time.Clock()

        self.__window_frame = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__window_frame)
    
        self.__window_rgba_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__window_rgba_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.frame_width, self.frame_height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.window_rgba_texture, 0)

        self.depth_renderbuffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.depth_renderbuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, self.frame_width, self.frame_height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.depth_renderbuffer)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("[graphics.py] - main framebuffer initialization failure")

        quad_positions = [
            -1.0, -1.0, 0.0,
            1.0, -1.0, 0.0,
            1.0,  1.0, 0.0,
            -1.0,  1.0, 0.0
        ]
        quad_uvs = [
            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0
        ]
        quad_normals = [
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0
        ]
        quad_indices = [
            0, 1, 2,
            0, 2, 3
        ]

        self.__window_quad = generate_vao(quad_positions, quad_indices, quad_uvs, quad_normals)
        self.__window_shader = generate_shader("assets/shaders/post.vert", "assets/shaders/post.frag")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        pg.display.flip()
        
        self.tkroot = tk.Tk()
        self.tkroot.configure(background="black")
        self.tkroot.title("OVERDRIVE")
        self.tkroot.geometry(f"{self.window_width + 150}x{self.window_height + 80}")

        self.framebuffer_label = None
        self.hierarchy_tree = None
        self.photo = None
        self.__instansiate_gui()

    def __instansiate_gui(self) -> None:
        main_frame = tk.Frame(self.tkroot)
        main_frame.pack(fill="both", expand=True)
        main_frame.configure(bg="darkblue")

        viewport_frame = tk.LabelFrame(main_frame, text="Viewport", background="darkgrey", foreground="black")
        viewport_frame.pack(side="left", anchor="se", fill="both")
        
        self.framebuffer_label = tk.Label(viewport_frame, bg="black")
        self.framebuffer_label.pack(fill="both", expand=True)

        hierarchy_frame = tk.LabelFrame(main_frame, text="File Paths", background="darkgrey", foreground="black")
        hierarchy_frame.pack(side="right", anchor="sw", fill="both", expand=True)

        style = ttk.Style()
        style.configure("Custom.Treeview", background="darkgrey", foreground="black", fieldbackground="darkgrey")

        self.hierarchy_tree = ttk.Treeview(hierarchy_frame, show="tree", style="Custom.Treeview")
        self.hierarchy_tree.pack(fill="both", expand=True)

        self.hierarchy_tree.insert("", "end", "root", text="Directories")

        command_frame = tk.Frame(self.tkroot, bg="red")
        command_frame.pack(side="top", anchor="n", fill="both", expand=False)

        command_vp = tk.LabelFrame(command_frame, text="cmd", background="darkgrey", foreground="black")
        command_vp.pack(side="left", anchor="s", fill="both", expand=True)

        delete_button = tk.Button(command_vp, text="delete", command=self.delete_button_callback)
        delete_button.pack(side="left", anchor="w", padx=5, pady=0)

        rename_button = tk.Button(command_vp, text="rename", command=self.rename_button_callback)
        rename_button.pack(side="left", anchor="w", padx=5, pady=2)

        backward_button = tk.Button(command_vp, text="<--", command=self.backward_button_callback)
        backward_button.pack(side="left", anchor="w", padx=5, pady=2)

        forward_button = tk.Button(command_vp, text="-->", command=self.forward_button_callback)
        forward_button.pack(side="left", anchor="w", padx=5, pady=2)
    
    def insert_directory(self, element : str):
        self.hierarchy_tree.insert("root", "end", text=element)
        

    def __render_fbuffer_to_canvas(self):
        glBindFramebuffer(GL_READ_FRAMEBUFFER, 0)

        fbpixels = glReadPixels(0, 0, self.window_width, self.window_height, GL_RGBA, GL_UNSIGNED_BYTE)
        fbimg = Image.frombytes("RGBA", (self.window_width, self.window_height), fbpixels)
        fbimg = fbimg.transpose(Image.FLIP_TOP_BOTTOM)

        self.photo = ImageTk.PhotoImage(fbimg)
        if self.framebuffer_label:
            self.framebuffer_label.configure(image=self.photo)
        else:
            print("[graphics.py] - framebuffer_lable failure")
        glBindFramebuffer(GL_READ_FRAMEBUFFER, 0)

    def bind(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__should_close = True
        
        #glBindFramebuffer(GL_FRAMEBUFFER, self.__window_frame)
        glClearColor(0.1, 0.1, 0.13, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def unbind(self) -> None:
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def render(self, tickrate) -> None:
        self.clock.tick(tickrate)
        self.__render_fbuffer_to_canvas()
        self.tkroot.update()

    def should_app_close(self) -> bool:
        return self.__should_close
        
class Camera():
    def __init__(self,
        fovy : float,
        xposition : float, 
        yposition : float, 
        zposition : float, 
        xrotation : float,
        yrotation : float,
        zrotation : float,
    ) -> None:
        self.fovy = fovy
        self.xposition = xposition
        self.yposition = yposition
        self.zposition = zposition
        self.xrotation = xrotation
        self.yrotation = yrotation
        self.zrotation = zrotation
        
        self.camera_matrix = []
        
    def __camera_matrix(self, eye, target, up, app) -> None:
        projection = Matrix44.perspective_projection(
            fovy=self.fovy,
            aspect=app.window_width / app.window_height,
            near=0.1,
            far=100.0,
            dtype=np.float32
        )

        eye = Vector3([self.xposition, self.yposition, self.zposition])
        target = Vector3([self.xrotation, self.yrotation, self.zrotation])
        view = Matrix44.look_at(
            eye=eye,
            target=target,
            up=up,
            dtype=np.float32
        )

        self.camera_matrix = projection * view

    def tick(self, app : App) -> None:
        self.__camera_matrix(
           eye=[self.xposition, self.yposition, self.zposition], 
           target=[self.xrotation, self.yrotation, self.zrotation],
           up=[0.0, 0.0, -1.0],
           app=app
        )

class Mesh():
    def __init__(self, 
        positions : list,
        indices : list,
        uvs : list,
        normals : list
    ) -> None:
        self.positions = positions
        self.indices = indices
        self.uvs = uvs
        self.normals = normals

class Model():
    def __init__(self,
        mesh : Mesh,
        vpath : str,
        fpath : str,
        xposition : float, 
        yposition : float, 
        zposition : float, 
        xrotation : float,
        yrotation : float,
        zrotation : float,
        xscale : float,
        yscale : float,
        zscale : float
    ) -> None:
        self.mesh = mesh
        self.xposition = xposition
        self.yposition = yposition
        self.zposition = zposition
        self.xrotation = xrotation
        self.yrotation = yrotation
        self.zrotation = zrotation
        self.xscale = xscale
        self.yscale = yscale
        self.zscale = zscale

        self.__vao = generate_vao(
            positions=self.mesh.positions,
            indices=self.mesh.indices,
            uvs=self.mesh.uvs,
            normals=self.mesh.normals
        )

        self.__shader = generate_shader(
            vertex_file_path=vpath,
            fragment_file_path=fpath
        )

        #self.__texture = generate_texture()

        self.model_matrix = []

    def __transform_matrix(self, tx, ty, tz, rx, ry, rz, sx, sy, sz) -> None:
        scale = Matrix44.from_scale([self.xscale, self.yscale, self.zscale], dtype=np.float32)
        rotation = Matrix44.from_eulers(
            [np.radians(self.xrotation), np.radians(self.yrotation), np.radians(self.zrotation)],
            dtype=np.float32
        )
        translation = Matrix44.from_translation(
            [self.xposition, self.yposition, self.zposition],
            dtype=np.float32
        )
        self.model_matrix = translation * rotation * scale

    def render(self, camera: Camera, app: App) -> None:
        glEnable(GL_DEPTH_TEST)
        camera.tick(app)
        self.__transform_matrix(
            self.xposition, self.yposition, self.zposition,
            self.xrotation, self.yrotation, self.zrotation,
            self.xscale, self.yscale, self.zscale
        )

        final_matrix = camera.camera_matrix * self.model_matrix

        glUseProgram(self.__shader)
        glBindVertexArray(self.__vao)
        transform_loc = glGetUniformLocation(self.__shader, "transform_matrix")
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, final_matrix.astype(np.float32))
        glDrawElements(GL_TRIANGLES, len(self.mesh.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        glUseProgram(0)

    
    def delete(self) -> None:
        glDeleteVertexArrays(1, [self.__vao])
        glDeleteProgram(self.__shader)