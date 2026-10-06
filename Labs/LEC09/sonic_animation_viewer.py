"""소닉 스프라이트 애니메이션 뷰어."""

import pico2d
from pathlib import Path
from typing import NamedTuple

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
SCALE = 4
IMAGE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')

# 원본 시트의 위쪽부터 순서대로: 총 10개 동작, 76개 프레임.
ROW_FRAME_COUNTS = (11, 12, 6, 9, 6, 6, 6, 8, 8, 4)


class Frame(NamedTuple):
    left: int
    top: int
    width: int
    height: int


class Animation(NamedTuple):
    name: str
    frames: tuple


ANIMATIONS = (
    Animation('동작 01', (Frame(1, 39, 29, 39),)),
)


def draw_frame(image, frame):
    bottom = image.h - frame.top - frame.height
    image.clip_draw(frame.left, bottom, frame.width, frame.height,
                    CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2,
                    frame.width * SCALE, frame.height * SCALE)


def main():
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    pico2d.hide_lattice()
    try:
        if not IMAGE_PATH.is_file():
            raise FileNotFoundError('스프라이트 이미지 파일이 없습니다.')
        image = pico2d.load_image(str(IMAGE_PATH))
    except Exception as error:
        print(f'이미지 로드 실패: {IMAGE_PATH}\n원인: {error}')
        pico2d.close_canvas()
        return 1
    running = True
    while running:
        for event in pico2d.get_events():
            if event.type == pico2d.SDL_QUIT:
                running = False
            elif event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
                running = False
        # pico2d의 기본 단색 배경(200, 200, 210)은 소닉과 대비된다.
        pico2d.clear_canvas()
        draw_frame(image, ANIMATIONS[0].frames[0])
        pico2d.update_canvas()
        pico2d.delay(0.01)
    pico2d.close_canvas()


if __name__ == '__main__':
    main()
