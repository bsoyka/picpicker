import bs4
import os
import threading
import time
from urllib.request import urlopen, urlretrieve
if not os.path.isdir("photos"): # Check if "photos" directory doesn't exist
    os.mkdir("photos") # Directory doesn't exist yet, make it
os.chdir("photos") # Change directory to "photos" to save photos here
def get_pics(keyword): # Function that gets run by each thread
    page = urlopen("https://unsplash.com/search/photos/" + keyword) # Simulates an Unsplash search for the keyword
    soup = bs4.BeautifulSoup(page, "html.parser") # Make a BeautifulSoup object for the search results
    images = soup.find_all("img") # Find the images in the search results page
    i = 0 # Make a new counter to count how many images were collected
    used = [] # Make a list to hold the pictures already collected to avoid duplicates
    for image in images: # Loop through the images in the webpage
        if str(image["src"]) in used: # Check if the image is a duplicate
            continue # It is a duplicate, move to the next image
        else: # Image is not a duplicate
            if str(image["src"]).startswith("https://images.unsplash.com/photo-"): # Check if a good URL or if other picture (user, logo, etc.)
                used.append(str(image["src"])) # Add to list to avoid duplicates
                urlretrieve(str(image["src"]), keyword + "-" + str(i) + ".jpg") # Save the image
                i += 1 # Increase the counter
    print("{} images collected for keyword \"{}\"".format(i, keyword)) # Inform the user
keywords = input("Space separated keywords: ") # Get the user's input of keywords to use when finding images
if keywords == "``top": # User entered "``top", find top keywords
    page = urlopen("https://unsplash.com/") # Get the HTML of the Unsplash homepage
    soup = bs4.BeautifulSoup(page, "html.parser") # Make a BeautifulSoup object for the Unsplash homepage
    def check_content(tag): # Function to find the keyword list
        if not tag.has_attr("class"): # Check if tag has class
            return False # If the tag doesn't have a class, it isn't the right one
        if tag["class"] == ["_39Gnz", "_2Pvqc", "_1aofb"]: # Check if tag has these exact classes
            return True # Found the match
        else: # Tag did not have correct classes
            return False # Not a match
    keyword_list = soup.find_all(check_content)[0] # Pass the check_content function to find the list of keywords
    keywords = [] # Make empty list to hold the keywords
    keyword_li_list = keyword_list.find_all("li") # Find the list elements
    for keyword_li in keyword_li_list: # Loop through the liest elements inside the keyword list
        a = keyword_li.a # Find the link inside the list element
        keyword = a.encode_contents().decode("utf-8").lower() # Get the keyword inside the list element's link
        keywords.append(keyword) # Add it to the list
else: # User did not enter "``top"
    keywords = keywords.split(" ") # Turn space-separated string into list
for keyword in keywords: # Loop through the user specified keywords
    while threading.active_count() > 4: # Enfore maximum 5 active Threads at a time
        time.sleep(0.1) # Wait 0.1 seconds until checking again
    thread = threading.Thread(target=get_pics, args=(keyword,)) # Create new Thread that will run get_pics(keyword)
    thread.start() # Start the new Thread