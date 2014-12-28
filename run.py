from src import ObjectLoader
from src import TextureLoader
from src import SeamEquilizer
from src import ImageTransformer
import argparse
import logging

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-g', '--original', help="Original OBJ file")
    parser.add_argument('-m', '--modified', help="Modified OBJ file")
    parser.add_argument('-t', '--texture', help="PNG texture of the original OBJ file")
    parser.add_argument('-s', '--save', help="Filename to save the output as")

    return parser.parse_args()

def setup_logger():
    LOG_FORMAT = "Patternfy - %(asctime)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    return logging.getLogger(__name__)

def main(args):

    LOGGER.info("loading texture")
    image = TextureLoader(args.texture).load_texture()

    LOGGER.info("loading original OBJ")
    original_face_to_vt, original_edges, original_vt = ObjectLoader(args.original).load_obj()

    LOGGER.info("loading modified OBJ")
    modified_face_to_vt, modified_edges, modified_vt = ObjectLoader(args.modified).load_obj()

    LOGGER.info("seam equilizing")
    SeamEquilizer(modified_edges, modified_vt).equilize()

    LOGGER.info("transforming image")
    image_transformer = ImageTransformer(image, original_face_to_vt, original_vt, modified_face_to_vt, modified_vt)
    transformed_image = image_transformer.transform()
    
    LOGGER.info("saving")
    transformed_image.save(args.save)
                         
    LOGGER.info("success")

args = get_args()
LOGGER = setup_logger()

if __name__ == '__main__':
    main(args)

