# import
import logging, json, os, hashlib
import azure.functions as func
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

# Cognitive Services Endpoint
PREDICTION_ENDPOINT = os.environ['PREDICTION_ENDPOINT']
PREDICTION_KEY = os.environ['PREDICTION_KEY']
PREDICTION_PROJECT_ID = os.environ['PREDICTION_PROJECT_ID']
PREDICTION_PUBLISHED_NAME = os.environ['PREDICTION_PUBLISHED_NAME']

# main
def main(myblob: func.InputStream,
         images: func.Out[func.Document]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"URI: {myblob.uri}\n"
                 f"Blob Size: {myblob.length} bytes")

    # call Custom Vision predictor API endpoint to get predictions from blob
    predictor = CustomVisionPredictionClient(PREDICTION_KEY, endpoint=PREDICTION_ENDPOINT)
    detection = predictor.detect_image(PREDICTION_PROJECT_ID, PREDICTION_PUBLISHED_NAME, myblob.read())

    # generate a dictionary of metadata for this image based on the API response
    image = {}
    image['image_name'] = myblob.name
    image['image_uri'] = myblob.uri
    image['image_bytes'] = myblob.length
    # explicitely generate a Cosmos id based on image uri
    # so we get to overwrite it if we re-process the same image
    image['id'] = hashlib.md5(myblob.uri.encode('utf-8')).hexdigest()
    # gather predictions
    image['predictions'] = []
    CONFIDENCE_THRESHOLD = 0.7 # ignore all predictions with probability below this threshold
    for p in detection.predictions:
        if p.probability > CONFIDENCE_THRESHOLD:
            prediction = {}
            prediction['tag_name'] = p.tag_name
            prediction['probability'] = p.probability
            prediction['bounding_box_left'] = p.bounding_box.left
            prediction['bounding_box_top'] = p.bounding_box.top
            prediction['bounding_box_width'] = p.bounding_box.width
            prediction['bounding_box_height'] = p.bounding_box.height
            image['predictions'].append(prediction)

    # log image metadata
    logging.info(f"Image Predictions: {json.dumps(image, sort_keys=True, indent=2)}")

    # save image prediction metadata into cosmos DB function output
    images.set(func.Document.from_dict(image))