import unittest
import requests
from app import check_is_local_file, check_is_remote_file, \
                user_agent, get_file_content


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.json_url = 'https://gist.githubusercontent.com/israelbgf/' \
                        'fbdb325cd35bc5b956b2e350d354648a/' \
                        'raw/b26d28f4c01a1ec7298020e88a200d292293ae4b/' \
                        'conteudojson'

        self.local_file = "test_file.txt"
        self.local_file_content = "Test String"

        local_file = open(self.local_file, "w")
        local_file.write(self.local_file_content)
        local_file.close()

        headers = {'User-Agent': user_agent}
        self.remote_content = requests.get(self.json_url, headers=headers)

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

        self.assertEqual(200, self.remote_content.status_code, 
                         "Request not successful.")
        self.assertTrue(content, "function could not get the given url.")
        self.assertEqual(content, self.remote_content.text)

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
        self.assertEqual(self.remote_content.text, content)

        # Now with a invalid local file
        
        with self.assertRaises(Exception):
            content = get_file_content("/tmp/invalid.txt")

        # Now with a invalid remote file
        with self.assertRaises(Exception):
            content = get_file_content("http://gitlab.ts3corp.com.br/invalid")

    def test_csv_type_hinting(self):
        self.fail("TODO")

    def test_json_type_hinting(self):
        self.fail("TODO")

    # def test_data_categorization(self):
    #     self.fail("TODO")

if __name__ == '__main__':
    unittest.main()
