from selenium import webdriver
import time



driver = webdriver.Firefox()

driver.get("https://www.chainreactioncycles.com/it/it/fuji-cross-1-3-cyclocross-bike-2019/rp-prod179657")
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
        ratio = (size["width"]/size["height"] if size["width"] > size["height"] else size["height"]/size["width"])
        print(ratio)
        print(size["width"])
        print(image.get_attribute("src"))
        print("--------------")
        if abs(1 - ratio) < 1.55 and prevWidth < size["width"]:
            prevWidth = size["width"]
            print(image.get_attribute("src"))


driver.close()