from bs4 import BeautifulSoup
import requests
import csv
import json

def get_page_content(url):
    """
    Retrieves the HTML content of a web page.

    Args:
        url (str): URL of the page to be downloaded.

    Returns:
        str: HTML content of the page as string, or None in case of error.
        Displays an error message on the console in case of failure.
    """
    if not isinstance(url, str):
        print(f"\nError: The argument 'url' is expected to be a string. Retrieved URL: {type(url)}\n")
        return None
    if not url.startswith('http://') and not url.startswith('https://'):
        print(f"\nError: The URL has to be prefixed with 'http://'or 'https://'. Retrieved URL: {url}\n")
        return None
    
    try:
        response = requests.get(url, timeout=10)  # Dodajemy timeout, żeby uniknąć zawieszenia
        response.raise_for_status()  # Sprawdza, czy kod statusu HTTP jest OK (200)
        return response.text
    except requests.exceptions.Timeout:
        print(f"\nError: Server response timeout for URL exceeded: {url}")
        print("The problem may be with your Internet connection, or the target server may be taking too long to respond.\n")
        return None
    except requests.exceptions.RequestException as e:
        print(f"\nError: An error occurred while downloading the page for the URL: {url}")
        print(f"Error type: {type(e).__name__}") # Wyświetlamy typ wyjątku
        print(f"Details: {e}") # Wyświetlamy szczegółowy komunikat wyjątku
        print("\nPlease ensure that the URL is correct and that the website exists.\n")
        return None
    
def extract_attribute(html_content, tag_name, attribute):
    """
    Extracts the value of the specified attribute from the HTML tags.

    Args:
        html_content (str): HTML content of the page.
        tag_name (str): The name of the HTML tag (e.g. a, img, div).
        attribute (str): The name of the attribute to extract (e.g. href, src, class).

    Returns:
        list: A list of attribute values, or an empty list if there are no tags or an error.
        Displays an error message on the console in case of failure.
    """
    if not isinstance(html_content, str):
        print(f"\nError: Argument 'html_content' must be a string. Retrieved: {type(html_content)}\n")
        return []
    if not isinstance(tag_name, str):
        print(f"\nError: Argument 'tag_name' must be a string. Retrieved: {type(tag_name)}\n")
        return []
    if not isinstance(attribute, str):
        print(f"\nError: Argument 'attribute' must be a string. Retrieved: {type(attribute)}\n")
        return []

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        elements = soup.find_all(tag_name)
        attribute_values = [element.get(attribute) for element in elements if element.get(attribute)] # Pobieramy tylko, gdy atrybut istnieje
        return attribute_values
    except Exception as e: # Bardziej ogólny wyjątek, bo BeautifulSoup może rzucać różne wyjątki
        print(f"\nError: While extracting attribute '{attribute}' from '{tag_name}'.")
        print(f"Error type: {type(e).__name__}")
        print(f"Details: {e}\n")
        return []


def extract_text_by_tag(html_content, tag_name):
    """
    Extracts text from all HTML tags with the given name.

    Args:
        html_content (str): HTML content of the page.
        tag_name (str): The name of the HTML tag (e.g. p, h1, a).

    Returns:
        list: A list of tag text, or an empty list if there are no tags or an error.
        Displays an error message on the console in case of failure.
    """
    if not isinstance(html_content, str):
        print(f"\nError: Argument 'html_content' must be a string. Retrieved: {type(html_content)}\n")
        return []
    if not isinstance(tag_name, str):
        print(f"\nError: Argument 'tag_name' must be a string. Retrieved: {type(tag_name)}\n")
        return []

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        elements = soup.find_all(tag_name)
        return [element.text.strip() for element in elements]
    except Exception as e:
        print(f"\nError: While extracting string (text) from '{tag_name}'.")
        print(f"Error type: {type(e).__name__}")
        print(f"Details: {e}\n")
        return []


def extract_text_by_class(html_content, class_name):
    """
    Extracts text from HTML tags of a given CSS class.

    Args:
        html_content (str): HTML content of the page.
        class_name (str): The name of the CSS class.

    Returns:
        list: A list of tag text, or an empty list if there are no tags or an error.
        Displays an error message on the console in case of failure.
    """
    if not isinstance(html_content, str):
        print(f"\nError: Argument 'html_content' must be a string. Retrieved: {type(html_content)}\n")
        return []
    if not isinstance(class_name, str):
        print(f"\nError: Argument 'class_name' must be a string. Retrieved: {type(class_name)}\n")
        return []

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        elements = soup.find_all(class_=class_name)
        return [element.text.strip() for element in elements]
    except Exception as e:
        print(f"\nError: While extracting string (text) from CSS class '{class_name}'.")
        print(f"Error type: {type(e).__name__}")
        print(f"Details: {e}\n")
        return []


def extract_text_by_id(html_content, id_name):
    """
    Extracts text from the HTML tag with the given ID.

    Args:
        html_content (str): HTML content of the page.
        id_name (str): The name of the ID.

    Returns:
        str: Text from the tag, or None if there is no tag or an error.
        Displays an error message on the console in case of failure.
    """
    if not isinstance(html_content, str):
        print(f"\nError: Argument 'html_content' must be a string. Retrieved: {type(html_content)}\n")
        return None # Zwracamy None, bo funkcja ma zwracać pojedynczy string lub None
    if not isinstance(id_name, str):
        print(f"\nError: Argument 'id_name' must be a string. Retrieved: {type(id_name)}\n")
        return None

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        element = soup.find(id=id_name)
        if element:
            return element.text.strip()
        else:
            print(f"\nWarning: Couldn't find tag with ID '{id_name}'.\n") # Uwaga, a nie błąd, bo ID może opcjonalnie istnieć
            return None # Zwracamy None, jeśli nie znaleziono elementu
    except Exception as e:
        print(f"\nError: While extracting strint (text) from ID '{id_name}'.")
        print(f"Error type: {type(e).__name__}")
        print(f"Details: {e}\n")
        return None


def extract_videos(html_content, save_dir=None):
    """
    Extracts links to video and optionally saves video files.

    Args:
        html_content (str): HTML content of the page.
        save_dir (str, optional): Path to the directory where to save the video files.
                                      If None, the files are not saved.

    Returns:
        list: A list of URLs to the video files, or an empty list if there is no video or an error.
        Displays an error message on the console in case of failure.
    """
    if not isinstance(html_content, str):
        print(f"\nError: Argument 'html_content' must be a string. Retrieved: {type(html_content)}\n")
        return []
    if save_dir is not None and not isinstance(save_dir, str):
        print(f"\nError: Argument 'save_dir' must be a string or None. Retrieved: {type(save_dir)}\n")
        return []

    video_links = []
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        video_tags = soup.find_all('video')
        for video_tag in video_tags:
            source_tags = video_tag.find_all('source') # Szukamy tagów <source> wewnątrz <video>
            for source_tag in source_tags:
                video_url = source_tag.get('src')
                if video_url:
                    video_links.append(video_url)
            video_src = video_tag.get('src') # Sprawdzamy też atrybut src bezpośrednio w <video>
            if video_src:
                video_links.append(video_src)

        iframe_tags = soup.find_all('iframe') # Szukamy tagów <iframe> (np. YouTube, Vimeo)
        for iframe_tag in iframe_tags:
            iframe_url = iframe_tag.get('src')
            if iframe_url and ("youtube.com" in iframe_url or "vimeo.com" in iframe_url): # Proste filtrowanie iframe'ów
                video_links.append(iframe_url)

        video_links = list(set(video_links)) # Usuwamy duplikaty linków

        if save_dir:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir) # Tworzymy katalog, jeśli nie istnieje
            for video_url in video_links:
                try:
                    print(f"\nDownloading video: {video_url}")
                    video_response = requests.get(video_url, stream=True, timeout=10)
                    video_response.raise_for_status()
                    filename = os.path.join(save_dir, os.path.basename(video_url.split("?")[0])) # Nazwa pliku z URL-a, usuwamy parametry query
                    with open(filename, 'wb') as f:
                        for chunk in video_response.iter_content(chunk_size=8192): # Pobieranie strumieniowe
                            f.write(chunk)
                    print(f"Video saved as: {filename}\n")
                except requests.exceptions.RequestException as e:
                    print(f"\nError: While downloading video from {video_url}")
                    print(f"Error type: {type(e).__name__}")
                    print(f"Details: {e}\n")

        return video_links

    except Exception as e:
        print(f"\nError: While retrieving video links")
        print(f"Error type: {type(e).__name__}")
        print(f"Details: {e}\n")
        return []


def extract_images(html_content, save_dir=None):
    """
    Extracts links to images and optionally saves image files.

    Args:
        html_content (str): HTML content of the page.
        save_dir (str, optional): Path to the directory where to save the image files.
                                      If None, the files are not saved.

    Returns:
        list: A list of URLs to images, or an empty list if no images or an error.
        Displays an error message on the console in case of failure.
    """
    if not isinstance(html_content, str):
        print(f"\nError: Argument 'html_content' must be a string. Retrieved: {type(html_content)}\n")
        return []
    if save_dir is not None and not isinstance(save_dir, str):
        print(f"\nError: Argument 'save_dir' must be a string or None. Retrieved: {type(save_dir)}\n")
        return []

    image_links = []
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            image_url = img_tag.get('src')
            if image_url:
                image_links.append(image_url)

        image_links = list(set(image_links)) # Usuwamy duplikaty linków

        if save_dir:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            for image_url in image_links:
                try:
                    print(f"\nDownloading image: {image_url}")
                    image_response = requests.get(image_url, stream=True, timeout=10)
                    image_response.raise_for_status()
                    filename = os.path.join(save_dir, os.path.basename(image_url.split("?")[0]))
                    with open(filename, 'wb') as f:
                        for chunk in image_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Image saved as: {filename}\n")
                except requests.exceptions.RequestException as e:
                    print(f"\nError: While downloading image from {image_url}")
                    print(f"Error type: {type(e).__name__}")
                    print(f"Details: {e}\n")

        return image_links

    except Exception as e:
        print(f"\nError: While retrieving image links")
        print(f"Error type: {type(e).__name__}")
        print(f"Details: {e}\n")
        return []


def extract_link_by_id(html_content, id_name):
    """
    Wyciąga link (URL) z elementu HTML o danym ID.

    Args:
        html_content (str): Zawartość HTML strony.
        id_name (str): Nazwa ID elementu.

    Returns:
        str: Link (URL) z atrybutu href tagu <a>, lub None w przypadku braku linku lub błędu.
        Displays an error message on the console in case of failure.
    """
    if not isinstance(html_content, str):
        print(f"\nError: Argument 'html_content' must be a string. Retrieved: {type(html_content)}\n")
        return None
    if not isinstance(id_name, str):
        print(f"\nError: Argument 'id_name' must be a string. Retrieved: {type(id_name)}\n")
        return None

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        element = soup.find(id=id_name)
        if element and element.name == 'a': # Sprawdzamy, czy element istnieje i jest tagiem <a>
            link = element.get('href')
            if link:
                return link
            else:
                print(f"\nWarning: Tag <a> from ID '{id_name}' don't have attribute called 'href'\n")
                return None
        else:
            print(f"\nWarning: Couldn't find tag <a> from ID '{id_name}'\n")
            return None
    except Exception as e:
        print(f"\nError: While retrieving link from ID '{id_name}'")
        print(f"Error type: {type(e).__name__}")
        print(f"Details: {e}\n")
        return None


def extract_links(html_content):
    """
    Extracts all links (URLs) from the page (from the <a> tags).

    Args:
        html_content (str): HTML content of the page.

    Returns:
        list: A list of URLs, or an empty list if there are no links or an error.
        Displays an error message on the console in case of failure.
    """
    if not isinstance(html_content, str):
        print(f"\nError: Argument 'html_content' must be a string. Retrieved: {type(html_content)}\n")
        return []

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        a_tags = soup.find_all('a')
        links = [a_tag.get('href') for a_tag in a_tags if a_tag.get('href')] # Wyciągamy tylko, gdy atrybut href istnieje
        return links
    except Exception as e:
        print(f"\nError: While retrieving all links from the website")
        print(f"Error type: {type(e).__name__}")
        print(f"Details: {e}\n")
        return []


def save_data(data, filename, filetype='csv'):
    """
    Saves the data to a file in the specified format (CSV or JSON).

    Args:
        data (list): The data to be saved. Can be a list of lists (for CSV) or a list of dictionaries (for JSON).
        filename (str): The name of the file to save (including the path, if needed).
        filetype (str, optional): The format of the file. Available: csv, json. Default: csv.

    Returns:
        bool: True if saved successfully, False in case of error.
        Displays an error message on the console in case of failure.
    """
    if not isinstance(filename, str):
        print(f"\nError: Argument 'filename' must be a string. Retrieved: {type(filename)}\n")
        return False
    if not isinstance(filetype, str):
        print(f"\nError: Argument 'filetype' must be a string. Retrieved: {type(filetype)}\n")
        return False

    filetype = filetype.lower() # Dla pewności, małe litery
    if filetype not in ['csv', 'json']:
        print(f"\nError: Unsupported file format '{filetype}'. Available formats: 'csv', 'json'\n")
        return False

    try:
        if filetype == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(data) # Zakładamy, że data to lista list
        elif filetype == 'json':
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=4, ensure_ascii=False) # Zakładamy, że data to lista słowników lub coś, co json.dump obsłuży
        print(f"\nData saved to file: {filename} (format: {filetype.upper()})\n")
        return True
    except Exception as e:
        print(f"\nError: While saving data to file '{filename}' (format: {filetype.upper()}).")
        print(f"Error type: {type(e).__name__}")
        print(f"Details: {e}\n")
        return False