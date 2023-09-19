import os

from dotenv import load_dotenv

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

class MLCapabilities():

    def __init__(self):
        # Authenticate against Azure API
        load_dotenv()  # take environment variables from .env.
        subscription_key = os.environ["VISION_KEY"]
        endpoint = os.environ["VISION_ENDPOINT"]

        self.computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    def get_caption(self, file_path):
        return self.computervision_client.describe_image_in_stream(open(file_path, "rb"), max_candidates=1, language="en").captions[0].text
    
    def get_tags(self, file_path):
        tags_result_remote = self.computervision_client.tag_image_in_stream(open(file_path, "rb"))
        if len(tags_result_remote.tags) == 0:
            return []
        else:
            return [tag.name for tag in tags_result_remote.tags]
