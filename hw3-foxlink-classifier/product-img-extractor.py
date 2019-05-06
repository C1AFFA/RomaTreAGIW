from selenium import webdriver
import time



driver = webdriver.Firefox()

driver.get("https://www.amazon.it/Nilox-Bicicletta-Elettrica-Assistita-Autonomia/dp/B07CZV3B38/ref=sr_1_3?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=bicicletta&qid=1557158791&s=gateway&sr=8-3")
time.sleep(3)
images = driver.find_elements_by_tag_name('img')

prevWidth = 0
for image in images :
    size = image.size
    #print(size)
    #print(image.location)
    #print(image.get_attribute("src"))
    parentSize = image.find_element_by_xpath('..').size
    if size["height"] > 0 :
        if abs(1 - size["width"]/size["height"]) < 0.334 and prevWidth < size["width"]:
            prevWidth = size["width"]
            print(image.get_attribute("src"))


driver.close()