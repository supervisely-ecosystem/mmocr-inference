import os
import supervisely as sly

import src.globals as g
import src.inference as inference

app = sly.Application()

if not g.DATASET_ID:
    datasets_ids = [dataset_info.id for dataset_info in g.api.dataset.get_list(g.PROJECT_ID)]
else:
    datasets_ids = [g.DATASET_ID]

for dataset_id in datasets_ids:
    dataset_name = g.api.dataset.get_info_by_id(dataset_id).name
    dataset_dir = os.path.join(g.TMP_PROJECT_DIR, dataset_name)
    os.makedirs(dataset_dir, exist_ok=True)
    sly.logger.info(f"Processing dataset: {dataset_name} with ID: {dataset_id}")

    image_infos = g.api.image.get_list(dataset_id)
    sly.logger.debug(f"Found {len(image_infos)} images in dataset {dataset_name}")

    image_ids = [image_info.id for image_info in image_infos]
    image_names = [image_info.name for image_info in image_infos]
    image_paths = [os.path.join(dataset_dir, image_name) for image_name in image_names]

    g.api.image.download_paths(dataset_id, image_ids, image_paths)
    sly.logger.debug(f"Downloaded {len(image_paths)} images to {dataset_dir}")

    inference.dump_predictions(image_paths)
    sly.logger.debug(f"Predictions were dumped to {g.OUTPUT_DIR}")

    sly.output.set_download(g.OUTPUT_DIR)

    sly.logger.info("Output directory archived and uploaded, the app will be stopped...")

app.shutdown()
