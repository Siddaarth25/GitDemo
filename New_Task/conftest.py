import pytest
from selenium import webdriver
import os


driver=None

step_screenshots = []

def pytest_addoption(parser):
    parser.addoption("--browsername", action="store", default="edge", help="Browser to test")


@pytest.fixture(scope="function")
def browserInstance(request):
    global driver
    browser_name = request.config.getoption("browsername")


    if browser_name == "edge":
        edge_options = webdriver.EdgeOptions()
        # edge_options.add_argument("--headless")
        # edge_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Edge(options=edge_options)


    elif browser_name == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        # firefox_options.add_argument("--headless")
        firefox_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Firefox(options=firefox_options)

    elif browser_name == "chrome":
        chrome_options = webdriver.ChromeOptions()
        # firefox_options.add_argument("--headless")
        # firefox_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://practice.expandtesting.com/")
    driver.maximize_window()
    driver.implicitly_wait(5)
    yield driver
    driver.close()



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    global step_screenshots

    pytest_html = item.config.pluginmanager.getplugin("html")

    outcome = yield
    report = outcome.get_result()

    extras = getattr(report, "extras", [])

    if report.when == "call":

        html = ""

        for screenshot in step_screenshots:
            html += f"""
            <div style="margin-bottom:20px;">
                <img src="{screenshot}"
                     alt="screenshot"
                     style="width:500px;border:1px solid black;"
                     onclick="window.open(this.src)">
                <br>
                <span>{os.path.basename(screenshot)}</span>
            </div>
            """

        if html:
            extras.append(pytest_html.extras.html(html))

        report.extras = extras

        # Clear for next test
        step_screenshots.clear()

def _capture_screenshot(file_name):
    driver.get_screenshot_as_file(file_name)

def take_step_screenshot(driver, step_name):
    global step_screenshots

    reports_dir = os.path.join(os.path.dirname(__file__), "report")
    os.makedirs(reports_dir, exist_ok=True)

    file_path = os.path.join(reports_dir, f"{step_name}.png")

    driver.save_screenshot(file_path)

    step_screenshots.append(file_path)


@pytest.fixture(scope="function")
def browser_name(request):
    browser_name = request.config.getoption("browsername")
    return browser_name