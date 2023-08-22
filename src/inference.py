import os
from mmocr.apis import MMOCRInferencer

import supervisely as sly

import src.globals as g


model = MMOCRInferencer(det="DBNetpp", rec="ABINet", device=g.DEVICE)


def dump_predictions(image_paths):
    sly.logger.info(f"Starting inference on {len(image_paths)} images...")
    predictions = model(image_paths, g.BATCH_SIZE)["predictions"]

    for pred, image_path in zip(predictions, image_paths):
        img_name, _ = os.path.splitext(os.path.basename(image_path))
        dataset_dir = os.path.basename(os.path.dirname(image_path))
        save_path = os.path.join(g.PROJECT_DIR, dataset_dir, f"{img_name}.json")
        texts = pred["rec_texts"]

        sly.json.dump_json_file(texts, save_path)

        sly.logger.debug(f"Predictions for image {image_path} were dumped to {save_path}")
