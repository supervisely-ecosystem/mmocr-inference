import os
import supervisely as sly

import globals as g
import functions as f
import inference as inference

app = sly.Application()

if not g.DATASET_ID:
    datasets_ids = [dataset_info.id for dataset_info in g.api.dataset.get_list(g.PROJECT_ID)]
else:
    datasets_ids = [g.DATASET_ID]

g.OUTPUT_PROJECT_ID = f.create_output_project()
project_meta = sly.ProjectMeta.from_json(g.api.project.get_meta(g.PROJECT_ID))
sly.logger.debug("Retrieved project meta for input project")
if not project_meta.tag_metas.get(g.TAG_NAME):
    sly.logger.debug(f"Tag {g.TAG_NAME} was not found in project meta. Adding...")
    new_tag = sly.TagMeta(g.TAG_NAME, sly.TagValueType.ANY_STRING)
    project_meta = project_meta.add_tag_meta(new_tag)
    sly.logger.debug(f"Tag {g.TAG_NAME} was added to project meta.")

if not project_meta.obj_classes.get(g.OBJECT_NAME):
    sly.logger.debug(f"Object class {g.OBJECT_NAME} was not found in project meta. Adding...")
    project_meta = project_meta.add_obj_class(g.OBJECT_CLASS)
    sly.logger.debug(f"Object class {g.OBJECT_NAME} was added to project meta.")

g.OBJECT_CLASS = project_meta.obj_classes.get(g.OBJECT_NAME)
g.api.project.update_meta(g.OUTPUT_PROJECT_ID, project_meta)
sly.logger.debug(f"Updated project meta for output project with ID: {g.OUTPUT_PROJECT_ID}")

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

    output_dataset_id = f.create_output_dataset(dataset_name, g.OUTPUT_PROJECT_ID)

    inference.save_predictions_predictions(image_paths, output_dataset_id)


app.shutdown()
