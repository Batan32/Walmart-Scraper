import unittest
from unittest.mock import patch, MagicMock
import product_scraper


class TestProductScraper(unittest.TestCase):

    def setUp(self):
        self.search_queries = ["computers"]
        self.sample_html = '''
            <html>
                <body>
                    <a href="/ip/sample-product-1">Product 1</a>
                    <a href="/ip/sample-product-2">Product 2</a>
                </body>
            </html>
        '''
        self.sample_product_html = '''
            <html>
                <body>
                    <script id="__NEXT_DATA__" type="application/json">
                        {"props":{"pageProps":{"initialData":{"data":{"product":{"priceInfo":{"currentPrice":{"price":100}},"usItemId":"12345","name":"Sample Product","brand":"Sample Brand","availabilityStatus":"In Stock","imageInfo":{"thumbnailUrl":"http://example.com/image.jpg"},"shortDescription":"This is a sample product"},"reviews":{"totalReviewCount":10,"averageOverallRating":4.5}}}}}}
                    </script>
                </body>
            </html>
        '''

    @patch('product_scraper.requests.get')
    def test_get_product_links_from_search_page(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = self.sample_html
        mock_get.return_value = mock_response

        product_links = product_scraper.get_product_links_from_search_page("computers", 1)
        self.assertEqual(len(product_links), 2)
        self.assertIn("https://www.walmart.com/ip/sample-product-1", product_links)
        self.assertIn("https://www.walmart.com/ip/sample-product-2", product_links)

    @patch('product_scraper.requests.get')
    def test_extract_product_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = self.sample_product_html
        mock_get.return_value = mock_response

        product_info = product_scraper.extract_product_info("https://www.walmart.com/ip/sample-product-1")
        self.assertIsNotNone(product_info)
        self.assertEqual(product_info["price"], 100)
        self.assertEqual(product_info["review_count"], 10)
        self.assertEqual(product_info["item_id"], "12345")
        self.assertEqual(product_info["avg_rating"], 4.5)
        self.assertEqual(product_info["product_name"], "Sample Product")
        self.assertEqual(product_info["brand"], "Sample Brand")
        self.assertEqual(product_info["availability"], "In Stock")
        self.assertEqual(product_info["image_url"], "http://example.com/image.jpg")
        self.assertEqual(product_info["short_description"], "This is a sample product")


if __name__ == '__main__':
    unittest.main()
