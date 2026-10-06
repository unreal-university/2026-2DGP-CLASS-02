"""소닉 스프라이트 애니메이션 뷰어."""

import pico2d
from pathlib import Path
from typing import NamedTuple
from time import perf_counter

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
SCALE = 4
FRAMES_PER_SECOND = 10
FRAME_SECONDS = 1 / FRAMES_PER_SECOND
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
    Animation('동작 01', (
        Frame(1, 39, 29, 39), Frame(31, 40, 26, 38),
        Frame(58, 39, 28, 39), Frame(86, 40, 30, 38),
        Frame(118, 40, 30, 38), Frame(150, 40, 30, 38),
        Frame(182, 40, 29, 38), Frame(211, 39, 29, 38),
        Frame(240, 39, 29, 38), Frame(270, 45, 24, 32),
        Frame(302, 51, 29, 26),
    )),
    Animation('동작 02', (
        Frame(8, 80, 26, 37),
        Frame(37, 80, 27, 37),
        Frame(65, 80, 31, 38),
        Frame(97, 80, 37, 37),
        Frame(135, 80, 32, 35),
        Frame(170, 79, 32, 38),
        Frame(206, 79, 26, 38),
        Frame(238, 80, 24, 37),
        Frame(263, 80, 30, 37),
        Frame(295, 80, 36, 37),
        Frame(334, 80, 32, 36),
        Frame(370, 79, 29, 38),
    )),
    Animation('동작 03', (
        Frame(1, 124, 33, 40),
        Frame(39, 124, 35, 39),
        Frame(89, 125, 35, 38),
        Frame(130, 121, 34, 42),
        Frame(181, 122, 34, 41),
        Frame(228, 122, 33, 40),
    )),
)


class Playback:
    def __init__(self):
        self.animation_index = 0
        self.frame_index = 0
        self.frame_elapsed = 0.0

    @property
    def frame(self):
        return ANIMATIONS[self.animation_index].frames[self.frame_index]

    def update(self, delta):
        self.frame_elapsed += delta
        frames = ANIMATIONS[self.animation_index].frames
        while self.frame_elapsed >= FRAME_SECONDS:
            self.frame_elapsed -= FRAME_SECONDS
            self.frame_index = (self.frame_index + 1) % len(frames)


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
    playback = Playback()
    previous = perf_counter()
    while running:
        for event in pico2d.get_events():
            if event.type == pico2d.SDL_QUIT:
                running = False
            elif event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
                running = False
        now = perf_counter()
        playback.update(now - previous)
        previous = now
        # pico2d의 기본 단색 배경(200, 200, 210)은 소닉과 대비된다.
        pico2d.clear_canvas()
        draw_frame(image, playback.frame)
        pico2d.update_canvas()
        pico2d.delay(0.01)
    pico2d.close_canvas()


if __name__ == '__main__':
    main()
