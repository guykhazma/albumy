from tests.base import BaseTestCase

from albumy.ml import MLService

class MLTestCase(BaseTestCase):
    def test_create_instance(self):
        ml_capabilities = MLService.get_ml_service("azure")
        self.assertEqual(ml_capabilities.provider, "azure")
    
    def test_caption(self):
        ml_capabilities = MLService.get_ml_service("azure")
        caption = ml_capabilities.generate_caption("images/test_image.jpeg")
        self.assertIn("red", caption)
    
    def test_tag(self):
        ml_capabilities = MLService.get_ml_service("azure")
        tags = ml_capabilities.generate_tags("images/test_image.jpeg", 5)
        self.assertTrue("red" in tags)