import os

from typing import List
from mmocr.apis import MMOCRInferencer

import supervisely as sly

import globals as g
import functions as f


model = MMOCRInferencer(det=g.DET_MODEL, rec=g.REC_MODEL, device=g.DEVICE)


def save_predictions(image_paths: List[str], output_dataset_id: int) -> None:
    """Finds text on images, creates rectangle annotations with labeled text and uploads them to Supervisely.

    :param image_paths: list of local paths to the downloaded images.
    :type image_paths: List[str]
    :param output_dataset_id: ID of the dataset to upload images with annotations to.
    :type output_dataset_id: int
    :return: None
    :rtype: None
    """
    sly.logger.info(f"Starting inference on {len(image_paths)} images...")
    predictions = model(image_paths, g.BATCH_SIZE)["predictions"]
    sly.logger.info(f"Finished inference on {len(image_paths)} images.")

    image_names = []
    anns = []

    with sly.tqdm_sly(total=len(image_paths), message="Saving predictions") as pbar:
        for pred, image_path in zip(predictions, image_paths):
            img_name, _ = os.path.splitext(os.path.basename(image_path))

            labels = []
            for text, text_score, rect, rect_score in zip(*list(pred.values())):
                assert len(rect) == 8
                # Creating rectangle label from predicted polygon.
                label = f.det_polygon_2_label(rect)
                # Adding text recognition tag to the label.
                label = label.add_tag(sly.Tag(g.TAG_META, text))
                labels.append(label)

            # Creating Supervisely annotation from labels.
            img = sly.image.read(image_path)
            ann = sly.Annotation(img.shape[:2], labels)
            anns.append(ann)
            image_names.append(img_name)

            pbar.update(1)

    sly.logger.debug(f"Finished processing {len(image_paths)} images, will upload them now.")

    f.upload_images_with_anns(image_paths, image_names, anns, output_dataset_id)
