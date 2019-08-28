import requests, time, shutil, re, os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

driver = webdriver.Chrome(executable_path=r'C:/chromedriver.exe')
driver.get("https://www.reddit.com/r/juicyasians/top/?sort=top&t=all")

download_folder = os.environ['C:/Users/Craig/Desktop/projects/scraping/Juicyasians/']

time.sleep(1)

num_pics_saved = 0
num_pics_to_save = os.environ['10']

elem = driver.find_element_by_tag_name("body")

def parseLink(link, regex):
    if (re.search(regex, link) is not None):
        return True
    else:
        return False

def checkDimensions(dimensions):
    width = int(dimensions.split('x')[0].strip())
    height = int(dimensions.split('x')[1].strip())
    if (width / height > 1.1 and width / height < 1.7):
        print ('Writing image file with dimensions: ', width, ' x ', height)
        return True

def parseAspectRatio(title):
    # Only match images with large dimensions
    regex = re.search(r'\d{4}\s*x\s*\d{4}', title)
    if (regex is not None):
        dimensions = regex.group(0)
        if (checkDimensions(dimensions)):
            return True
    else:
        return False

no_of_pagedowns = num_pics_to_save * 1.5

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    no_of_pagedowns-=1

pic_elems = driver.find_elements_by_class_name("scrollerItem")
pic_links = []

# Get individual user comment links where images are hosted
for pic in pic_elems:
    pic_link_tag = pic.find_elements_by_tag_name("a")
    if (len(pic_link_tag) > 3):
        pic_link = pic_link_tag[3].get_attribute('href')
    if (pic_link):
        pic_links.append(pic_link)

pic_links.pop(0)

# Get individual picture links and download each to a specified folder
for link in pic_links:
    if (num_pics_saved < num_pics_to_save):
        print ('\n')
        print ('Checking - ', link)
        if (parseLink(link, r'https:\/\/www.reddit.com\/r\/EarthPorn\/comments\/')):
            driver.get(link)
            time.sleep(1)
            #elem = driver.find_element_by_tag_name("img").get_attribute('src')
            elem = driver.find_elements_by_tag_name("img")
            elem = elem[1].get_attribute("src")
            print ('first elem:', elem)
            title = driver.find_element_by_tag_name("h2").text
            print ('got link, checking aspect ratio')
            if (parseAspectRatio(title) and elem):
                # Download the image
                print ('second elem: ', elem)
                if (parseLink(elem, r'https:\/\/i.redditmedia.com\/') or parseLink(elem, r'https:\/\/i.redd.it\/')):
                    print ('valid image link')
                    response = requests.get(elem, stream=True)
                    with open (download_folder + 'reddit-img-' + str(num_pics_saved) + '.jpg', 'wb') as out_file:
                        print ('saving image as' + download_folder + 'reddit-img-' + str(num_pics_saved) + '.jpg' + 'from address: ', elem)
                        shutil.copyfileobj(response.raw, out_file)
                        num_pics_saved+=1
                    del response
                else:
                    print ('image link not valid')
            else:
                print ('invalid aspect ratio')
        else:
            print ('invalid link')

driver.close()