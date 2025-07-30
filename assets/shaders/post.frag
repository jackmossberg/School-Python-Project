#version 330 core
out vec4 FragColor;
in vec3 position;
in vec2 uv;
uniform sampler2D tex0;
void main() {
    FragColor = texture(tex0, uv);
    //FragColor = vec4(uv, 1.0f, 1.0f);
}