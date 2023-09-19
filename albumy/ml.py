import os
import logging
from typing import List
from abc import ABC, abstractmethod

from dotenv import load_dotenv

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

class MLCapabilities(ABC):
    """
    An Abstract class representing the ML capabilities of the application.
    """

    @abstractmethod
    def generate_caption(self, file_path: str) -> str:
        """
        Generate a caption for the image at the given file path.
        """
        pass
    
    @abstractmethod
    def generate_tags(self, file_path:str, max_tags) -> List[str]:
        """
        Generate a list of tags for the image at the given file path.
        """
        pass

class AzureMLCapabilities(MLCapabilities):
    """
    An implementation of MLCapabilities using Azure Cognitive Services.
    """

    def __init__(self):
        self.provider = "azure"
        # Authenticate against Azure API
        load_dotenv()  # take environment variables from .env.
        subscription_key = os.environ["VISION_KEY"]
        endpoint = os.environ["VISION_ENDPOINT"]

        self.computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    def generate_caption(self, file_path):
        res = ""
        try:
            with open(file_path, "rb") as image:
                res = self.computervision_client.describe_image_in_stream(image, max_candidates=1, language="en").captions[0].text
        except Exception as e:
            logging.error("Failed to open image, falling back to empty caption")
            logging.error(e)
        return res
    
    def generate_tags(self, file_path, max_tags):
        res = []
        try:
            with open(file_path, "rb") as image:
                tags_result_remote = self.computervision_client.tag_image_in_stream(image)
                res = tags_result_remote.tags
                if len(res) > 0:
                    res = [tag.name for tag in res[:max_tags]]
        except Exception as e:
            logging.error("Failed to open image, falling back to empty tags list")
            logging.error(e)
        return res

class MLService():
    """
    A factory class for creating ML services.
    """

    @staticmethod
    def get_ml_service(provider) -> MLCapabilities:
        if provider == "azure":
            return AzureMLCapabilities()
        else:
            raise Exception("Invalid provider")