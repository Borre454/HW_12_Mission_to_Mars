# Mission to Mars

Built a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

- Initial scraping was accomplished using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
  - Scraped the [NASA Mars News Site](https://mars.nasa.gov/news/) and collected the latest News Title and Paragraph Text.
  - Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    - Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
    - Make sure to find the image url to the full size `.jpg` image.
    - Make sure to save a complete url string for this image.
  
