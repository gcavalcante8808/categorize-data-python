import unittest
import requests
import tablib


from app import check_is_local_file, check_is_remote_file, \
                user_agent, get_file_content, parse_content


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.json_url = 'https://gist.githubusercontent.com/israelbgf/' \
                        'fbdb325cd35bc5b956b2e350d354648a/' \
                        'raw/b26d28f4c01a1ec7298020e88a200d292293ae4b/' \
                        'conteudojson'

        self.csv_url = 'https://gist.githubusercontent.com/israelbgf/' \
                       '782a92243d0ba1ff47f9aaf46358f870/' \
                       'raw/86c7a2bf04242bd4262b203ca725ce1da69f035d/' \
                       'conteudocsv'

        self.local_file = "test_file.txt"
        self.local_file_content = "Test String"

        local_file = open(self.local_file, "w")
        local_file.write(self.local_file_content)
        local_file.close()

        headers = {'User-Agent': user_agent}
        self.json_remote_content = requests.get(self.json_url, 
                                                headers=headers)
        self.csv_remote_content = requests.get(self.csv_url,
                                               headers=headers)

    def test_local_file(self):
        """
        """
        content = check_is_local_file("test_file.txt")
        self.assertTrue(content)
    #     self.assertEqual(content, "Test String")

    def test_remote_input(self):
        """
        """
        # Check success workflow.
        content = check_is_remote_file(self.json_url)

        self.assertEqual(200, self.json_remote_content.status_code, 
                         "Request not successful.")
        self.assertTrue(content, "function could not get the given url.")
        self.assertEqual(content, self.json_remote_content.text)

        # Check non URL workflow.
        content = check_is_remote_file("http://nonecxiste.com")
        self.assertFalse(content)

        # Check non URI workflow
        content = check_is_remote_file("http://gitlab.ts3corp.com.br/invuri")
        self.assertFalse(content)


    def test_get_file_content(self):
        """
        """
        # First with local file.
        content = get_file_content(self.local_file)
        self.assertEqual(content, self.local_file_content)

        # Now a remote file.
        content = get_file_content(self.json_url)
        self.assertEqual(self.json_remote_content.text, content)

        # Now with a invalid local file
        
        with self.assertRaises(Exception):
            content = get_file_content("/tmp/invalid.txt")

        # Now with a invalid remote file
        with self.assertRaises(Exception):
            content = get_file_content("http://gitlab.ts3corp.com.br/invalid")

    def test_content_guessing(self):
        # JSON content
        jparsed = parse_content(self.json_remote_content.text)
        self.assertIsInstance(jparsed, tablib.Dataset)
        #CSV Content
        cparsed = parse_content(self.csv_remote_content.text)
        self.assertIsInstance(cparsed, tablib.Dataset)

        #Invalid Format
        with self.assertRaises(tablib.core.UnsupportedFormat):
            parse_content('Unsupported Format')

if __name__ == '__main__':
    unittest.main()
