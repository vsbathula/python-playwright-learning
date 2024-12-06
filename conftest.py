import datetime

import pytest
import base64

from utilities.read_config import AppConfiguration
from utilities.axe_helper import AxeHelper
from playwright.sync_api import sync_playwright
from axe_core_python.sync_playwright import Axe
from pytest_metadata.plugin import metadata_key


@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    browser = pytestconfig.getoption("--browser") if pytestconfig.getoption("--browser") is not None else "chromium"
    return browser


@pytest.fixture(scope="function")
def setup(request, browser_name):
    configuration = AppConfiguration.get_app_configuration()
    common_info = AppConfiguration.get_common_info()
    base_url = common_info["baseUrl"]
    print("Base url: {0}".format(AppConfiguration.get_common_info()["baseUrl"]))

    # Browser options
    headless = eval(configuration["headless"])  # convert to bool
    slow_mo = float(configuration["slowMo"])
    launch_options = {"headless": headless, "slow_mo": slow_mo}

    # Start Playwright
    playwright = sync_playwright().start()
    browser = None
    if browser_name == "chromium":
        browser = playwright.chromium.launch(**launch_options, args=['--start-maximized'])
    elif browser_name == "chrome":
        browser = playwright.firefox.launch(channel="chrome", **launch_options, args=['--start-maximized'])
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(**launch_options, args=['--start-maximized'])
    else:
        print("Invalid browser selection")

    context_options = {'base_url': base_url}

    # Browser context settings
    browser_context = browser.new_context(**context_options, no_viewport=True)
    browser_context.set_default_navigation_timeout(float(configuration["defaultNavigationTimeout"]))
    browser_context.set_default_timeout(float(configuration["defaultTimeout"]))

    # Create Page
    page = browser_context.new_page()

    request.cls.page = page
    page.goto(base_url)

    yield page
    page.close()
    browser.close()
    playwright.stop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    screenshot_bytes = ""
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == "call":
        xfail = hasattr(report, 'wasxfail')
        if report.failed or xfail and "page" in item.funcargs:
            page = item.funcargs["setup"]

            screenshot_bytes = page.screenshot()
            extra.append(pytest_html.extras.image(base64.b64encode(screenshot_bytes).decode(), ''))
        report.extras = extra


def pytest_html_report_title(report):
    report.title = "Pytest Playwright HTML Test Report"


def pytest_configure(config):
    config.stash[metadata_key]["Project"] = "Playwright Python Learning"


@pytest.fixture(scope="session")
def axe_playwright():
    """Fixture to provide an instance of AxeHelper with Axe initialized.

        This fixture has a session scope, meaning it will be created once per test session
        and shared across all tests.

        Returns:
            AxeHelper: An instance of AxeHelper with Axe initialized.
    """
    yield AxeHelper(Axe())
