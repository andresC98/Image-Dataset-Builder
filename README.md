# Image Dataset Builder
Image Dataset builder gathering images from Pixabay free API. Following guidelines of https://pixabay.com/api/docs/ for correct terms of usage.

Image Scraper from Pixabay API. 
Useful tool for e.g. downloading a dataset of images by categories. 
Stores results on separated folders named as each query introduced.

**Usage**: $python scrape_images.py

**Example input (answering prompts)**: *animals*
                                       *cat, dog, elephant*
                                       *50*
Will proceed to retrieve animal images of the specified queries, 50 each at maximum.

**Note: Is required to introduce your Pixabay API key in the line 28 of this script.**
       You can obtain your API key for free from https://pixabay.com/api/docs/
       Please **follow the API terms of use for a correct usage of this tool and gathered data.**
