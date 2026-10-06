"""소닉 스프라이트 애니메이션 뷰어."""

import pico2d

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800


def main():
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    pico2d.close_canvas()


if __name__ == '__main__':
    main()
