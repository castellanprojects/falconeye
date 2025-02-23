# FalconEye Module Documentation

## Overview

The **FalconEye** module is designed to perform web scraping tasks by extracting data from various online sources. It provides an efficient way to gather structured information from HTML content through various helper functions. This module is capable of retrieving HTML page contents, extracting links, images, videos, and specific text based on HTML tags or attributes, and saving the scraped data in multiple formats (CSV or JSON).

The module leverages the **BeautifulSoup** library for parsing HTML content and extracting the desired data, combined with **requests** for fetching web pages. The output is customizable, allowing data extraction to be stored for further analysis or processing.

### Key Features
- Fetches HTML content from URLs
- Extracts images, videos, links, and text data
- Supports extraction by HTML tags, CSS classes, and IDs
- Data storage in CSV or JSON formats
- Error handling and logging for robustness
- Simple to integrate into larger web scraping projects

### Remember to import Scraper from FalconEye package before using.

---

## Main Functionality

### `get_page_content(url)`
**Purpose:** Retrieves the HTML content of a web page from the provided URL.

#### Arguments:
- **url (str)**: The URL of the web page to be scraped.

#### Returns:
- **str**: HTML content of the page as a string, or **None** in case of an error.

#### Example Usage:
```python
html_content = get_page_content('https://example.com')
```

#### Description:
This function fetches the HTML content of a given URL. It performs checks on the URL format and handles potential request timeouts or errors, returning the content or an error message.

---

### `extract_attribute(html_content, tag_name, attribute)`
**Purpose:** Extracts the value of a specific attribute from HTML tags.

#### Arguments:
- **html_content (str)**: The HTML content of the page.
- **tag_name (str)**: The name of the HTML tag (e.g., `<a>`, `<img>`, `<div>`).
- **attribute (str)**: The name of the attribute to extract (e.g., `href`, `src`, `class`).

#### Returns:
- **list**: A list of attribute values, or an empty list if no matching tags are found.

#### Example Usage:
```python
urls = extract_attribute(html_content, 'a', 'href')
```

#### Description:
This function extracts the values of a specified attribute from the tags in the HTML content. It returns a list of all values found, or an empty list if no matching tags or attributes exist.

---

### `extract_text_by_tag(html_content, tag_name)`
**Purpose:** Extracts text content from HTML tags with the specified name.

#### Arguments:
- **html_content (str)**: The HTML content of the page.
- **tag_name (str)**: The name of the HTML tag (e.g., `<p>`, `<h1>`, `<a>`).

#### Returns:
- **list**: A list of extracted text from the tags.

#### Example Usage:
```python
texts = extract_text_by_tag(html_content, 'p')
```

#### Description:
This function returns all text content found within the specified tags. It returns a list of strings, each representing the text content of an individual tag.

---

### `extract_videos(html_content, save_dir=None)`
**Purpose:** Extracts video URLs from the HTML content, with an optional feature to download the videos.

#### Arguments:
- **html_content (str)**: The HTML content of the page.
- **save_dir (str, optional)**: Path to the directory where videos should be saved.

#### Returns:
- **list**: A list of video URLs.

#### Example Usage:
```python
video_links = extract_videos(html_content, save_dir='./videos')
```

#### Description:
This function identifies and extracts video URLs from `<video>` and `<iframe>` tags. Optionally, it downloads the videos to the specified directory. It returns a list of video URLs, which can be used for further processing or saving.

---

### `extract_images(html_content, save_dir=None)`
**Purpose:** Extracts image URLs from the HTML content, with an optional feature to download the images.

#### Arguments:
- **html_content (str)**: The HTML content of the page.
- **save_dir (str, optional)**: Path to the directory where images should be saved.

#### Returns:
- **list**: A list of image URLs.

#### Example Usage:
```python
image_links = extract_images(html_content, save_dir='./images')
```

#### Description:
This function extracts image URLs from `<img>` tags in the HTML content. It can also download the images to a specified directory if provided. The function returns a list of unique image URLs.

---

### `save_data(data, filename, filetype='csv')`
**Purpose:** Saves the extracted data to a file in CSV or JSON format.

#### Arguments:
- **data (list)**: The data to be saved, typically a list of dictionaries (for JSON) or lists (for CSV).
- **filename (str)**: The name of the file to save the data to.
- **filetype (str, optional)**: The format to save the data in (`'csv'` or `'json'`). Default is `'csv'`.

#### Returns:
- **bool**: Returns `True` if the data was successfully saved, `False` otherwise.

#### Example Usage:
```python
save_data(data, 'output.csv', 'csv')
```

#### Description:
This function allows saving the extracted data in either CSV or JSON format, depending on the user's preference. It handles the data conversion and ensures the file is written properly.

---

## Example Use Case

```python
# Define the URL to scrape
url = 'https://example.com'

# Fetch the page content
html_content = get_page_content(url)

# Extract all links
links = extract_links(html_content)

# Extract images
image_links = extract_images(html_content, save_dir='./downloads/images')

# Save the extracted links to a CSV file
save_data(links, 'links.csv', 'csv')
```

---

## Error Handling

FalconEye includes robust error handling to ensure smooth execution:

- **Invalid URL Format**: The URL must be a string starting with either `http://` or `https://`.
- **Request Failures**: Timeout and request exceptions are caught, with helpful error messages for debugging.
- **Parsing Errors**: The module handles potential parsing issues with BeautifulSoup, providing error details when the extraction fails.

---

## Conclusion

The **FalconEye** module provides an efficient, robust solution for scraping and processing data from the web. Whether you're extracting specific text, images, or video URLs, or simply gathering all links on a page, FalconEye makes web scraping straightforward and easy to integrate into your projects. Its ability to save data in both CSV and JSON formats ensures compatibility with a wide range of data processing tools and workflows.

