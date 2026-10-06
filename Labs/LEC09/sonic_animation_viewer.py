"""소닉 스프라이트 애니메이션 뷰어."""

import pico2d
from pathlib import Path

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
IMAGE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')


def main():
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
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
        pico2d.clear_canvas()
        pico2d.update_canvas()
        pico2d.delay(0.01)
    pico2d.close_canvas()


if __name__ == '__main__':
    main()
