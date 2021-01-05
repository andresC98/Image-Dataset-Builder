########################################################################################
# Author: Andrés Carrillo (github.com/andresC98)
#
# Image Scraper from Pixabay API. 
# Useful tool for e.g. downloading a dataset of images by categories.
#
# Usage: python scrape_images.py
# Example input (answering prompts): animals
#                                    cat, dog, elephant
#                                    50
# Will proceed to retrieve animal images of the specified queries, 50 each at maximum.
#
# Note: Is required to introduce your Pixabay API key in the line 28 of this script.
#       You can obtain your API key for free from https://pixabay.com/api/docs/
#       Please follow the API terms of use for a correct usage of this tool.
########################################################################################

import os, math
from queue import Queue
from threading import Thread
from time import time
import requests, json
from urllib.request import Request, urlopen
from io import BytesIO
from PIL import Image

## Pixabay API request construction and query
API_KEY = "INTRODUCE HERE YOUR KEY" # < === Pixabay API Key provided in https://pixabay.com/api/docs/


class ProcessWorker(Thread):
    """
    In charge of parsing the request information obtained by API (image urls) and
    processing and storing the image retrieved from the webserver.
    """
    
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            thread_id, urls_img, window, search_q = self.queue.get()
            try:
                for i, img in enumerate(urls_img):
                    url = img["webformatURL"]
                    thread_img_i = window*thread_id + i
                    req = Request(url, headers={'User-Agent' : "Magic Browser"}) 
                    file = BytesIO(urlopen(req).read())
                    img = Image.open(file)
                    savename = f"Scraped_Data/{search_q}/{search_q}_{thread_img_i}.jpg"
                    try:
                        img.save(savename) 
                    except:
                        img.convert('RGB').save(savename) 

                    #print(f"Thread {thread_id} processed and saved file: {savename}")
            finally:
                self.queue.task_done()


def main():
    queue = Queue()
    n_threads = 8
    if API_KEY == "INTRODUCE HERE YOUR KEY": 
        print("You have to specify your Pixabay API KEY in the code.")
        exit(1)
    category = input("Choose one category of the following: backgrounds, fashion, nature, science, education, "\
                     "feelings, health, people, religion, places, animals, industry, computer, food, sports, "\
                    "transportation, travel, buildings, business, music.\nIf no category desired, write none: ").lower()
    category = None if category == "none" else category
    queries = input("Introduce object(s) to search, separated in commas if more than one: ").split(",") # e.g. duck
    NUM = input("How many photos at most to retrieve for each search? (max: 200 ea.): ") # from 1 up to 200
    print(f"Starting retrieval of {len(queries)} image queries. Search list: {queries}.")

    for search_q in queries:
        ts = time()
        search_q = search_q.strip()
        
        QUERY = "+".join(search_q.split(" "))
        N_PHOTOS_Q = "&per_page=" + NUM
        CAT = "" if not category else ("&category=" + category) 
        IMG_TYPE = "&image_type=" + "photo"
        req_url = "https://pixabay.com/api/?key="+ API_KEY +"&q="+ QUERY + N_PHOTOS_Q + CAT + IMG_TYPE
        
        response = requests.get(req_url)
        content_array = json.loads(response.text)["hits"]
        n_images = len(content_array)

        # Creating folder for storing images with query name
        if not os.path.exists("Scraped_Data/"+search_q):
            os.makedirs("Scraped_Data/"+search_q)

        print(f"Query: [{search_q}]. Starting {n_threads} threads for parallel retrieval and processing of {n_images} images.")
        print("Nº request remaining on API until limit in this hour: ", response.headers['X-RateLimit-Remaining'])

        window = int(math.ceil( n_images / n_threads)) 
        links = []
        
        for x in range(n_threads):
            start_batch = window*x
            end_batch = start_batch + window
            links.append(content_array[start_batch:end_batch])
            worker = ProcessWorker(queue)
            worker.daemon = True # allows main thread exiting while workers are blocking
            worker.start()
        
        for i, links_thread in enumerate(links):
            queue.put((i, links_thread, window, search_q))
        queue.join()    # Main thread waits for queue to finish processing all tasks
        print("Finished downloading images of {}! Took {:.3f} seconds".format(search_q, time()-ts) )

    print("Done! You can find your downloaded data in the folder /Scraped_Data")
    exit(0)
if __name__ == '__main__':
    main()