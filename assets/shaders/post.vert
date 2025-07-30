#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec2 aUV;
layout(location = 2) in vec3 aNormal;
uniform mat4 transform_matrix;
out vec3 position;
out vec2 uv;
void main() {
    position = aPos;
    uv = aUV;
    gl_Position = vec4(aPos, 1.0);
}