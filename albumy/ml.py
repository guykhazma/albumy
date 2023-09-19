import os
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
        return self.computervision_client.describe_image_in_stream(open(file_path, "rb"), max_candidates=1, language="en").captions[0].text
    
    def generate_tags(self, file_path, max_tags):
        tags_result_remote = self.computervision_client.tag_image_in_stream(open(file_path, "rb"))
        if len(tags_result_remote.tags) == 0:
            return []
        else:
            # return the top tags by confidence
            return [tag.name for tag in tags_result_remote.tags[:max_tags]]

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