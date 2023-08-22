import os

from typing import List
from mmocr.apis import MMOCRInferencer

import supervisely as sly

import globals as g
import functions as f


model = MMOCRInferencer(det=g.DET_MODEL, rec=g.REC_MODEL, device=g.DEVICE)


def get_ann(image_path: str) -> sly.Annotation:
    """Finds text on images, creates rectangle annotations with labeled text and uploads them to Supervisely.

    :param image_paths: path to the image to run inference on.
    :type image_paths: str
    :return: Supervisely rectangle annotation with text labels.
    :rtype: sly.Annotation
    """

    sly.logger.debug(f"Running inference on image {image_path}")
    predictions = model(image_path, g.BATCH_SIZE)["predictions"]
    sly.logger.debug(f"Finished inference on image {image_path}")

    labels = []
    for text, text_score, rect, rect_score in zip(*list(predictions[0].values())):
        assert len(rect) == 8
        # Creating rectangle label from predicted polygon.
        label = f.det_polygon_2_label(rect)
        # Adding text recognition tag to the label.
        label = label.add_tag(sly.Tag(g.TAG_META, text))
        labels.append(label)

    # Creating Supervisely annotation from labels.
    img = sly.image.read(image_path)
    ann = sly.Annotation(img.shape[:2], labels)

    sly.logger.debug(f"Processed annotation for image {image_path}")
    sly.fs.silent_remove(image_path)
    return ann
