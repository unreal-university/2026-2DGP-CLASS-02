"""소닉 스프라이트 애니메이션 뷰어."""

import pico2d

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800


def main():
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    running = True
    while running:
        for event in pico2d.get_events():
            if event.type == pico2d.SDL_QUIT:
                running = False
            elif event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
                running = False
        pico2d.clear_canvas()
        pico2d.update_canvas()
        pico2d.delay(0.01)
    pico2d.close_canvas()


if __name__ == '__main__':
    main()
