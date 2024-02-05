from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import requests

# Initialize the error counter
error_counter = 0

# Setup Chrome options for headless operation
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("--window-size=1920x1080")  # Specify window size


# Setup Selenium with ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the page with the dynamic content
url = ''

# Funciton to resize the image to the size of the window dynamically
def resize_image(img, max_width, max_height):
    original_width, original_height = img.size

    # Calculate the ratio to maintain aspect ratio
    width_ratio = max_width / original_width
    height_ratio = max_height / original_height
    min_ratio = min(width_ratio, height_ratio)

    # Calculate new size using the minimum ratio
    new_width = int(original_width * min_ratio)
    new_height = int(original_height * min_ratio)

    # Resize and return the image using Image.Resampling.LANCZOS for high-quality downsampling
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Function to reconnect the driver
def reconnect_driver():
    global driver
    driver.quit()  # Close the current driver

    # Setup Chrome options for headless operation
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    chrome_options.add_argument("--window-size=1920x1080")  # Specify window size

    # Reinitialize the driver with headless options
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)  # Reopen the URL

# Function to update the image in the Tkinter window
def update_image():
    global error_counter  # Use the global error counter

    # Find the image element on the webpage
    image_element = driver.find_element(By.ID, 'liveviewImage')
    image_src = image_element.get_attribute('src')

    # Check if image_src is not empty and has a valid URL scheme
    if image_src and image_src.startswith(('http://', 'https://')):
        # Fetch the image content
        response = requests.get(image_src)
        if response.status_code == 200:
            error_counter = 0  # Reset error counter on successful fetch

            # Use BytesIO to convert bytes data to a file-like object for ImageTk
            image_data = BytesIO(response.content)
            # Open the image
            img = Image.open(image_data)

            # Resize the image to fill the window while maintaining aspect ratio
            img = resize_image(img, root.winfo_width(), root.winfo_height())

            # Convert the image to a format Tkinter can use
            imgtk = ImageTk.PhotoImage(image=img)
            panel.imgtk = imgtk  # Keep a reference so it's not garbage collected
            panel.config(image=imgtk)
        elif response.status_code == 404:
            error_counter += 1  # Increment error counter on 404
            print(f"404 error encountered. Error count: {error_counter}")
            if error_counter >= 5:  # Check if error limit reached
                print("Attempting to reconnect...")
                reconnect_driver()
                error_counter = 0  # Reset error counter after reconnecting
        else:
            print(f"Failed to retrieve image, status code: {response.status_code}")
    else:
        print(f"Invalid or empty image source: {image_src}")

    # Schedule the function to be called again after 1000ms (1 second)
    root.after(1000, update_image)
# Tkinter setup
root = tk.Tk()
root.title("Live Feed")
root.state('zoomed')
panel = tk.Label(root)  # Panel to display images
panel.pack()

# Open the URL initially
driver.get(url)

# Start the GUI loop and image update process
update_image()
root.mainloop()

# Clean up: close the browser window when the Tkinter window is closed
driver.quit()
