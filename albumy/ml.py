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

    def generate_caption(self, file_path):
        return self.computervision_client.describe_image_in_stream(open(file_path, "rb"), max_candidates=1, language="en").captions[0].text
    
    def generate_tags(self, file_path, max_tags=10):
        tags_result_remote = self.computervision_client.tag_image_in_stream(open(file_path, "rb"))
        if len(tags_result_remote.tags) == 0:
            return []
        else:
            # return the top tags by confidence
            return [tag.name for tag in tags_result_remote.tags[:max_tags]]
