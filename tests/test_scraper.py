import unittest
from falconeye import scraper
import os
import json
import csv

class TestGetPageContent(unittest.TestCase):
    # ... (testy dla get_page_content - bez zmian) ...
    def test_get_page_content_valid_url(self):
        url = "http://example.com"
        content = scraper.get_page_content(url)
        self.assertIsInstance(content, str)
        self.assertTrue(len(content) > 0)

    def test_get_page_content_invalid_url_format(self):
        url = "niepoprawny-url"
        content = scraper.get_page_content(url)
        self.assertIsNone(content)

    def test_get_page_content_non_existent_url(self):
        url = "https://jakas-nieistniejaca-strona.com"
        content = scraper.get_page_content(url)
        self.assertIsNone(content)

    def test_get_page_content_timeout(self):
        url = "http://httpbin.org/delay/3" # Używamy httpbin z opóźnieniem 3 sekund, timeout w funkcji jest 10s
        content = scraper.get_page_content(url)
        self.assertIsInstance(content, str)
        self.assertTrue(len(content) > 0)


class TestExtractAttribute(unittest.TestCase):

    TEST_HTML = "<div class='test'><a href='https://example.com' data-value='123'>Link</a><img src='/image.png' alt='obrazek'></div>"

    def test_extract_attribute_valid_tag_attribute(self):
        attributes = scraper.extract_attribute(TestExtractAttribute.TEST_HTML, 'a', 'href')
        self.assertEqual(attributes, ['https://example.com'])

    def test_extract_attribute_non_existent_tag(self):
        attributes = scraper.extract_attribute(TestExtractAttribute.TEST_HTML, 'span', 'href')
        self.assertEqual(attributes, [])

    def test_extract_attribute_non_existent_attribute(self):
        attributes = scraper.extract_attribute(TestExtractAttribute.TEST_HTML, 'a', 'title')
        self.assertEqual(attributes, [])

    def test_extract_attribute_invalid_html_content_type(self):
        attributes = scraper.extract_attribute(123, 'a', 'href') # Niepoprawny typ html_content
        self.assertEqual(attributes, [])

    def test_extract_attribute_invalid_tag_name_type(self):
        attributes = scraper.extract_attribute(TestExtractAttribute.TEST_HTML, 123, 'href') # Niepoprawny typ tag_name
        self.assertEqual(attributes, [])

    def test_extract_attribute_invalid_attribute_type(self):
        attributes = scraper.extract_attribute(TestExtractAttribute.TEST_HTML, 'a', 123) # Niepoprawny typ attribute
        self.assertEqual(attributes, [])


class TestExtractTextByTag(unittest.TestCase):

    TEST_HTML = "<div><h1>Tytuł</h1><p>Akapit 1.</p><p>Akapit 2.</p></div>"

    def test_extract_text_by_tag_valid_tag(self):
        text_list = scraper.extract_text_by_tag(TestExtractTextByTag.TEST_HTML, 'p')
        self.assertEqual(text_list, ['Akapit 1.', 'Akapit 2.'])

    def test_extract_text_by_tag_non_existent_tag(self):
        text_list = scraper.extract_text_by_tag(TestExtractTextByTag.TEST_HTML, 'span')
        self.assertEqual(text_list, [])

    def test_extract_text_by_tag_invalid_html_content_type(self):
        text_list = scraper.extract_text_by_tag(123, 'p') # Niepoprawny typ html_content
        self.assertEqual(text_list, [])

    def test_extract_text_by_tag_invalid_tag_name_type(self):
        text_list = scraper.extract_text_by_tag(TestExtractTextByTag.TEST_HTML, 123) # Niepoprawny typ tag_name
        self.assertEqual(text_list, [])


class TestExtractTextByClass(unittest.TestCase):

    TEST_HTML = "<div class='container'><p class='text-段落'>Tekst klasy 1.</p><p class='text-段落'>Tekst klasy 2.</p><p class='other-class'>Inny tekst.</p></div>"

    def test_extract_text_by_class_valid_class(self):
        text_list = scraper.extract_text_by_class(TestExtractTextByClass.TEST_HTML, 'text-段落')
        self.assertEqual(text_list, ['Tekst klasy 1.', 'Tekst klasy 2.'])

    def test_extract_text_by_class_non_existent_class(self):
        text_list = scraper.extract_text_by_class(TestExtractTextByClass.TEST_HTML, 'non-existent-class')
        self.assertEqual(text_list, [])

    def test_extract_text_by_class_invalid_html_content_type(self):
        text_list = scraper.extract_text_by_class(123, 'text-段落') # Niepoprawny typ html_content
        self.assertEqual(text_list, [])

    def test_extract_text_by_class_invalid_class_name_type(self):
        text_list = scraper.extract_text_by_class(TestExtractTextByClass.TEST_HTML, 123) # Niepoprawny typ class_name
        self.assertEqual(text_list, [])


class TestExtractTextById(unittest.TestCase):

    TEST_HTML = "<div><p id='akapit-1'>Tekst akapitu 1.</p><p id='akapit-2'>Tekst akapitu 2.</p></div>"

    def test_extract_text_by_id_valid_id(self):
        text = scraper.extract_text_by_id(TestExtractTextById.TEST_HTML, 'akapit-1')
        self.assertEqual(text, 'Tekst akapitu 1.')

    def test_extract_text_by_id_non_existent_id(self):
        text = scraper.extract_text_by_id(TestExtractTextById.TEST_HTML, 'non-existent-id')
        self.assertIsNone(text) # Sprawdzamy, czy zwraca None, gdy ID nie ma

    def test_extract_text_by_id_invalid_html_content_type(self):
        text = scraper.extract_text_by_id(123, 'akapit-1') # Niepoprawny typ html_content
        self.assertIsNone(text)

    def test_extract_text_by_id_invalid_id_name_type(self):
        text = scraper.extract_text_by_id(TestExtractTextById.TEST_HTML, 123) # Niepoprawny typ id_name
        self.assertIsNone(text)


class TestExtractVideos(unittest.TestCase):

    TEST_HTML_VIDEO_TAG = "<video><source src='video1.mp4' type='video/mp4'><source src='video2.webm' type='video/webm'></video><video src='video3.ogg'></video>"
    TEST_HTML_IFRAME_TAG = "<iframe src='https://www.youtube.com/embed/VIDEO_ID_1'></iframe><iframe src='https://vimeo.com/VIDEO_ID_2'></iframe><iframe></iframe>" # Dodano pusty iframe
    TEST_HTML_MIXED = TEST_HTML_VIDEO_TAG + TEST_HTML_IFRAME_TAG

    def test_extract_videos_video_tags(self):
        video_links = scraper.extract_videos(TestExtractVideos.TEST_HTML_VIDEO_TAG)
        self.assertEqual(set(video_links), {'video1.mp4', 'video2.webm', 'video3.ogg'}) # Używamy set, bo kolejność nie jest ważna, a chcemy uniknąć duplikatów

    def test_extract_videos_iframe_tags(self):
        video_links = scraper.extract_videos(TestExtractVideos.TEST_HTML_IFRAME_TAG)
        expected_links = ['https://www.youtube.com/embed/VIDEO_ID_1', 'https://vimeo.com/VIDEO_ID_2']
        self.assertEqual(set(video_links), set(expected_links)) # Używamy set, kolejność nie jest ważna

    def test_extract_videos_mixed_tags(self):
        video_links = scraper.extract_videos(TestExtractVideos.TEST_HTML_MIXED)
        expected_links = {'video1.mp4', 'video2.webm', 'video3.ogg', 'https://www.youtube.com/embed/VIDEO_ID_1', 'https://vimeo.com/VIDEO_ID_2'}
        self.assertEqual(set(video_links), expected_links)

    def test_extract_videos_no_videos(self):
        video_links = scraper.extract_videos("<div>No videos here</div>")
        self.assertEqual(video_links, [])

    def test_extract_videos_invalid_html_content_type(self):
        video_links = scraper.extract_videos(123) # Niepoprawny typ html_content
        self.assertEqual(video_links, [])


class TestExtractImages(unittest.TestCase):

    TEST_HTML = "<div><img src='/image1.jpg' alt='Obraz 1'><img src='image2.png'></div><p>Tekst bez obrazka.</p>"

    def test_extract_images_valid_images(self):
        image_links = scraper.extract_images(TestExtractImages.TEST_HTML)
        self.assertEqual(set(image_links), {'/image1.jpg', 'image2.png'}) # Używamy set, kolejność nie jest ważna

    def test_extract_images_no_images(self):
        image_links = scraper.extract_images("<div>No images here</div>")
        self.assertEqual(image_links, [])

    def test_extract_images_invalid_html_content_type(self):
        image_links = scraper.extract_images(123) # Niepoprawny typ html_content
        self.assertEqual(image_links, [])


class TestExtractLinkById(unittest.TestCase):

    TEST_HTML = "<div><a id='link-1' href='https://link1.com'>Link 1</a><p id='akapit-1'>Tekst.</p></div>"

    def test_extract_link_by_id_valid_id(self):
        link = scraper.extract_link_by_id(TestExtractLinkById.TEST_HTML, 'link-1')
        self.assertEqual(link, 'https://link1.com')

    def test_extract_link_by_id_non_existent_id(self):
        link = scraper.extract_link_by_id(TestExtractLinkById.TEST_HTML, 'non-existent-id')
        self.assertIsNone(link) # Sprawdzamy, czy zwraca None, gdy ID nie ma

    def test_extract_link_by_id_element_not_a_tag(self):
        link = scraper.extract_link_by_id(TestExtractLinkById.TEST_HTML, 'akapit-1') # Element z ID to <p>, a nie <a>
        self.assertIsNone(link) # Powinien zwrócić None, bo to nie tag <a>

    def test_extract_link_by_id_no_href_attribute(self):
        html_no_href = "<div><a id='link-no-href'>Link bez href</a></div>"
        link = scraper.extract_link_by_id(html_no_href, 'link-no-href') # Tag <a> bez atrybutu href
        self.assertIsNone(link) # Powinien zwrócić None, bo brak href

    def test_extract_link_by_id_invalid_html_content_type(self):
        link = scraper.extract_link_by_id(123, 'link-1') # Niepoprawny typ html_content
        self.assertIsNone(link)

    def test_extract_link_by_id_invalid_id_name_type(self):
        link = scraper.extract_link_by_id(TestExtractLinkById.TEST_HTML, 123) # Niepoprawny typ id_name
        self.assertIsNone(link)


class TestExtractLinks(unittest.TestCase):

    TEST_HTML = "<div><a href='https://link1.com'>Link 1</a><p><a href='/link2.html'>Link 2</a></p><span><a href='#link3'>Link 3</a></span><a>Tekst bez linku</a></div>"

    def test_extract_links_valid_links(self):
        links = scraper.extract_links(TestExtractLinks.TEST_HTML)
        self.assertEqual(set(links), {'https://link1.com', '/link2.html', '#link3'}) # Używamy set, kolejność nie jest ważna

    def test_extract_links_no_links(self):
        links = scraper.extract_links("<div>No links here</div>")
        self.assertEqual(links, [])

    def test_extract_links_invalid_html_content_type(self):
        links = scraper.extract_links(123) # Niepoprawny typ html_content
        self.assertEqual(links, [])


class TestSaveData(unittest.TestCase):

    TEST_DATA_CSV = [['Name', 'Age'], ['Alice', '30'], ['Bob', '25']]
    TEST_DATA_JSON = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
    TEST_FILENAME_CSV = "test_data.csv"
    TEST_FILENAME_JSON = "test_data.json"
    TEST_SAVE_DIR = "test_save_dir"

    def setUp(self): # Metoda setUp uruchamiana przed każdym testem
        if os.path.exists(TestSaveData.TEST_FILENAME_CSV):
            os.remove(TestSaveData.TEST_FILENAME_CSV) # Usuwamy plik testowy CSV, jeśli istnieje
        if os.path.exists(TestSaveData.TEST_FILENAME_JSON):
            os.remove(TestSaveData.TEST_FILENAME_JSON) # Usuwamy plik testowy JSON, jeśli istnieje
        if os.path.exists(TestSaveData.TEST_SAVE_DIR):
            os.rmdir(TestSaveData.TEST_SAVE_DIR) # Usuwamy folder testowy, jeśli istnieje

    def tearDown(self): # Metoda tearDown uruchamiana po każdym teście
        if os.path.exists(TestSaveData.TEST_FILENAME_CSV):
            os.remove(TestSaveData.TEST_FILENAME_CSV) # Usuwamy plik testowy CSV po teście
        if os.path.exists(TestSaveData.TEST_FILENAME_JSON):
            os.remove(TestSaveData.TEST_FILENAME_JSON) # Usuwamy plik testowy JSON po teście
        if os.path.exists(TestSaveData.TEST_SAVE_DIR):
            os.rmdir(TestSaveData.TEST_SAVE_DIR) # Usuwamy folder testowy po teście

    def test_save_data_csv_valid(self):
        result = scraper.save_data(TestSaveData.TEST_DATA_CSV, TestSaveData.TEST_FILENAME_CSV, filetype='csv')
        self.assertTrue(result) # Sprawdzamy, czy funkcja zwróciła True (sukces)
        self.assertTrue(os.path.exists(TestSaveData.TEST_FILENAME_CSV)) # Sprawdzamy, czy plik CSV został utworzony
        with open(TestSaveData.TEST_FILENAME_CSV, 'r', encoding='utf-8') as f:
            csv_content = f.read()
            self.assertIn("Name,Age", csv_content) # Sprawdzamy, czy plik CSV zawiera nagłówki
            self.assertIn("Alice,30", csv_content) # Sprawdzamy, czy plik CSV zawiera dane

    def test_save_data_json_valid(self):
        result = scraper.save_data(TestSaveData.TEST_DATA_JSON, TestSaveData.TEST_FILENAME_JSON, filetype='json')
        self.assertTrue(result) # Sprawdzamy, czy funkcja zwróciła True (sukces)
        self.assertTrue(os.path.exists(TestSaveData.TEST_FILENAME_JSON)) # Sprawdzamy, czy plik JSON został utworzony
        with open(TestSaveData.TEST_FILENAME_JSON, 'r', encoding='utf-8') as f:
            json_content = json.load(f) # Wczytujemy JSON z pliku
            self.assertEqual(json_content, TestSaveData.TEST_DATA_JSON) # Porównujemy zawartość JSON z oczekiwanymi danymi

    def test_save_data_invalid_filetype(self):
        result = scraper.save_data(TestSaveData.TEST_DATA_CSV, TestSaveData.TEST_FILENAME_CSV, filetype='txt') # Niepoprawny filetype
        self.assertFalse(result) # Sprawdzamy, czy funkcja zwróciła False (błąd)
        self.assertFalse(os.path.exists(TestSaveData.TEST_FILENAME_CSV)) # Sprawdzamy, czy plik TXT NIE został utworzony

    def test_save_data_invalid_filename_type(self):
        result = scraper.save_data(TestSaveData.TEST_DATA_CSV, 123, filetype='csv') # Niepoprawny typ filename
        self.assertFalse(result)
        self.assertFalse(os.path.exists(TestSaveData.TEST_FILENAME_CSV))

    def test_save_data_invalid_filetype_type(self):
        result = scraper.save_data(TestSaveData.TEST_DATA_CSV, TestSaveData.TEST_FILENAME_CSV, filetype=123) # Niepoprawny typ filetype
        self.assertFalse(result)
        self.assertFalse(os.path.exists(TestSaveData.TEST_FILENAME_CSV))


if __name__ == '__main__':
    unittest.main()