import time
import logging
from pprint import pformat
from appium import webdriver
from appium.options.android import UiAutomator2Options
from classes.cv import CvImage, find_templ_in_img
from constants import GRDN_APP, DEFAULT_SLEEP_TIME
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

# Let's assume we dynamically get these variables somewhere from outside, like os.environ.get("TESTING_DEVICE") or
# from cli
from dynamic_env import CAPABILITIES, APPIUM_SERV_URL


class Device:
    """
    Class for interacting with Android device using Appium driver
    :var driver: Appium driver object
    :var log: Logger object
    """
    def __init__(self, capabilities=CAPABILITIES, appium_serv=APPIUM_SERV_URL):
        """
        Initialize Device class
        :param driver: Appium driver object
        :param capabilities: Appium capabilities object
        :param appium_serv: Appium server URL
        """
        self.log = logging.getLogger(__name__)
        self.log.info(f"Connecting to appium at {appium_serv} with capabilities: {pformat(capabilities)}")
        self.driver = webdriver.Remote(appium_serv, options=UiAutomator2Options().load_capabilities(capabilities))

    def activate_app(self, app=GRDN_APP):
        self.log.info(f"Activating app {app}")
        self.driver.activate_app(app)

    def terminate_app(self, app=GRDN_APP):
        self.log.info(f"Terminating app {app}")
        self.driver.terminate_app(app_id=app)

    def quit_session(self):
        self.log.info(f"Quitting session")
        self.driver.quit()

    def get_screen(self):
        return self.driver.get_screenshot_as_base64()

    def tap(self, x, y):
        self.log.info(f"Tapping at {x}, {y}")
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(x, y) \
            .pointer_down() \
            .release()
        actions.perform()

    def find_pic_on_screen(self, pic: CvImage, thrsh=0.98):
        self.log.debug(f"Looking for pic on screen")
        screen = CvImage(self.get_screen())
        max_loc, max_val = find_templ_in_img(screen, pic)
        if max_val > thrsh:
            self.log.debug(f"Found pic at {max_loc} with {max_val}")
            return max_loc
        else:
            self.log.debug(f"Pic not found with {max_val}")
            return None

    def wait_for_pic(self, pic: CvImage, thrsh=0.98, retries=10, period=DEFAULT_SLEEP_TIME):
        for _ in range(retries):
            coords = self.find_pic_on_screen(pic, thrsh=thrsh)
            if coords:
                self.log.info(f"Pic found after {retries} with period {period}s")
                return coords
            else:
                time.sleep(period)
        self.log.info(f"Pic not found after {retries} with period {period}s")
        return None

    def wait_for_button_and_tap(self, btn_pic: CvImage, retries=10, period=1):
        coords = self.wait_for_pic(btn_pic, retries=retries, period=period)
        assert coords, f"Button not found after {retries} with period {period}s"
        self.tap(coords[0] + 1, coords[1] + 1)
