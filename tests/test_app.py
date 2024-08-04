import time
import logging
from pytest_check import check
from constants import DEFAULT_SLEEP_TIME

log = logging.getLogger(__name__)


def test_play_btn(device_with_grdn, buttons):
    log.info("Starting test play button")
    device_with_grdn.wait_for_button_and_tap(buttons.play.image)
    log.info("Wait and check, if screen is changed (=game loaded) after tap")
    time.sleep(DEFAULT_SLEEP_TIME)
    play_btn_coords = device_with_grdn.find_pic_on_screen(buttons.play.image)
    with check:
        assert not play_btn_coords, "Play button is not on screen after tap"
        log.info("Play button is not on screen after tap")

