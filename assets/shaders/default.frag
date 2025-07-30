#version 330 core
out vec4 FragColor;
in vec2 uv;
in vec3 position;

vec2 grid(vec2 uv, float columns, float rows) {
    return fract(vec2(uv.x * columns, uv.y * rows));
}

void main() {
    float thickness = 0.02;
    float gscale = 15.0;
    vec2 grid = grid(uv, gscale, gscale);

    if (grid.x < thickness || grid.y < thickness || grid.x > (1.0f - thickness) || grid.y > (1.0f - thickness)) {
        FragColor = vec4(0.5, 0.5, 0.5, 1.0);
    } else {
        discard;
    }
}