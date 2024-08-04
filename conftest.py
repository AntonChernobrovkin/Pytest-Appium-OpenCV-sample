import pytest
import logging
from pathlib import Path
from classes.buttons import Buttons
from classes.device import Device

log = logging.getLogger(__name__)


@pytest.fixture
def device_with_grdn():
    log.info("Creating device with Gardenscape app")
    device = Device()
    device.activate_app()
    yield Device()
    log.info("Terminating Gardenscape app and quitting session")
    device.terminate_app()
    device.quit_session()


@pytest.fixture
def buttons():
    buttons = Buttons()
    # In real project list of buttons abd their path should be loaded from separate file
    for name, path in [("play", "resources/play.png")]:
        button_path = Path(path)
        if button_path.is_file():
            buttons.add_button("play", button_path)
        else:
            raise FileNotFoundError(f"File {button_path} for button {name} not found")
    yield buttons
