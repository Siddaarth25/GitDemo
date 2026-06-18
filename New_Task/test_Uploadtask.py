import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from conftest import take_step_screenshot


def test_task_assigned(browserInstance,browser_name):
    
    driver = browserInstance
    take_step_screenshot(driver, "01_homepage")

    file_name =[ r"C:\Users\SiddaarthChockalinga\Downloads\increased_resize-image-to-500kb-with-high-quality_100KB.jpg",r"C:\Users\SiddaarthChockalinga\Downloads\resize-image-to-500kb-with-high-.webp"]
    wait = WebDriverWait(driver, 10)
    if browser_name=="firefox":
        driver.find_element(By.XPATH, "//div/h3/a[text()='File Upload']").click()
    else:
        action = ActionChains(driver)
        action.move_to_element(driver.find_element(By.XPATH,"//div/h3/a[text()='File Upload']")).click().perform()

    take_step_screenshot(driver, "01_page2")
    driver.find_element(By.XPATH,"//div/input").send_keys(file_name[0])
    print(driver.find_element(By.XPATH,"//div/b").text)
    take_step_screenshot(driver, "01_Uploaded_over_500kb")
    driver.find_element(By.XPATH,"//div/input").send_keys(file_name[1])
    driver.find_element(By.XPATH,"//form/button").click()
    take_step_screenshot(driver, "01_Uploaded_under_500kb")
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div/h1")))
    print(driver.find_element(By.XPATH, "//div/h1").text)

