import os

from typing import List
from mmocr.apis import MMOCRInferencer

import supervisely as sly

import globals as g
import functions as f


model = MMOCRInferencer(det="DBNetpp", rec="ABINet", device=g.DEVICE)


def save_predictions(image_paths: List[str], output_dataset_id: int):
    sly.logger.info(f"Starting inference on {len(image_paths)} images...")
    predictions = model(image_paths, g.BATCH_SIZE)["predictions"]

    img_names = []
    anns = []

    with sly.tqdm_sly(total=len(image_paths), message="Saving predictions") as pbar:
        for pred, image_path in zip(predictions, image_paths):
            img_name, _ = os.path.splitext(os.path.basename(image_path))

            labels = []
            for text, text_score, rect, rect_score in zip(*list(pred.values())):
                assert len(rect) == 8
                label = f.det_polygon_2_label(rect)
                label = label.add_tag(sly.Tag(g.TAG_META, text))
                labels.append(label)

            img = sly.image.read(image_path)
            ann = sly.Annotation(img.shape[:2], labels)
            anns.append(ann)
            img_names.append(img_name)

            pbar.update(1)

    sly.logger.debug(f"Finished inference on {len(image_paths)} images, will upload them now.")

    with sly.tqdm_sly(total=len(image_paths), message="Uploading images") as pbar:
        for batched_img_paths, batched_img_names, batched_anns in zip(
            sly.batched(image_paths), sly.batched(img_names), sly.batched(anns)
        ):
            uploaded_image_infos = g.api.image.upload_paths(
                output_dataset_id, batched_img_names, batched_img_paths
            )
            uploaded_image_ids = [image_info.id for image_info in uploaded_image_infos]
            g.api.annotation.upload_anns(uploaded_image_ids, batched_anns)
            pbar.update(len(batched_img_paths))

            sly.logger.debug(
                f"Uploaded batch of {len(batched_img_paths)} images to dataset with ID: {output_dataset_id}"
            )
