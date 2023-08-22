import os
import supervisely as sly

import globals as g
import functions as f
import inference as inference

if not g.DATASET_ID:
    datasets_ids = [dataset_info.id for dataset_info in g.api.dataset.get_list(g.PROJECT_ID)]
else:
    datasets_ids = [g.DATASET_ID]

sly.logger.debug(f"The app will working with following dataset IDs: {datasets_ids}")


@sly.handle_exceptions
def prepare_output_project() -> None:
    """Creates output project and adds tag meta and object class to it if they don't exist.
    Saves tag meta and object class to global variables to access them from inference.

    :return: None
    :rtype: None
    """
    g.OUTPUT_PROJECT_ID = f.create_output_project()
    project_meta = sly.ProjectMeta.from_json(g.api.project.get_meta(g.PROJECT_ID))
    sly.logger.debug("Retrieved project meta for input project")

    # Checking if tag meta exists in project meta, if not - adding it.
    if not project_meta.tag_metas.get(g.TAG_NAME):
        sly.logger.debug(f"Tag {g.TAG_NAME} was not found in project meta. Adding...")
        new_tag = sly.TagMeta(g.TAG_NAME, sly.TagValueType.ANY_STRING)
        project_meta = project_meta.add_tag_meta(new_tag)
        sly.logger.debug(f"Tag {g.TAG_NAME} was added to project meta.")

    # Saving tag meta to global variable to access it from inference.
    g.TAG_META = project_meta.tag_metas.get(g.TAG_NAME)
    sly.logger.debug(f"Saved tag meta for tag {g.TAG_NAME}")

    # Checking if object class exists in project meta, if not - adding it.
    if not project_meta.obj_classes.get(g.OBJECT_NAME):
        sly.logger.debug(f"Object class {g.OBJECT_NAME} was not found in project meta. Adding...")
        project_meta = project_meta.add_obj_class(g.OBJECT_CLASS)
        sly.logger.debug(f"Object class {g.OBJECT_NAME} was added to project meta.")

    # Saving object class to global variable to access it from inference.
    g.OBJECT_CLASS = project_meta.obj_classes.get(g.OBJECT_NAME)

    # Updating output project meta with new tag meta and object class.
    g.api.project.update_meta(g.OUTPUT_PROJECT_ID, project_meta)
    sly.logger.debug(f"Updated project meta for output project with ID: {g.OUTPUT_PROJECT_ID}")


@sly.handle_exceptions
def main() -> None:
    """Iterates over datasets, downloads images from them, runs inference on them and uploads images with annotations
    to output project. Deletes temporary directory after finishing.

    :return: None
    :rtype: None
    """

    for dataset_id in datasets_ids:
        dataset_name = g.api.dataset.get_info_by_id(dataset_id).name
        dataset_dir = os.path.join(g.TMP_PROJECT_DIR, dataset_name)
        os.makedirs(dataset_dir, exist_ok=True)
        sly.logger.info(f"Processing dataset: {dataset_name} with ID: {dataset_id}")

        image_infos = g.api.image.get_list(dataset_id)
        sly.logger.debug(f"Found {len(image_infos)} images in dataset {dataset_name}")

        output_dataset_id = f.create_output_dataset(dataset_name, g.OUTPUT_PROJECT_ID)

        image_ids = [image_info.id for image_info in image_infos]
        image_names = [image_info.name for image_info in image_infos]
        image_paths = [os.path.join(dataset_dir, image_name) for image_name in image_names]

        anns = []

        sly.logger.debug(f"Starting download images from dataset {dataset_name} by batches...")

        with sly.tqdm_sly(
            total=len(image_paths),
            message=f"Running inference on images from dataset {dataset_name}",
        ) as pbar:
            for batched_image_ids, batched_image_paths in zip(
                sly.batched(image_ids), sly.batched(image_paths)
            ):
                g.api.image.download_paths(dataset_id, batched_image_ids, batched_image_paths)
                sly.logger.debug(
                    f"Downloaded batch of {len(batched_image_ids)} images to {dataset_dir}"
                )

                for image_path in batched_image_paths:
                    ann = inference.get_ann(image_path)
                    anns.append(ann)
                    pbar.update(1)

                sly.logger.debug(f"Processed batch of {len(batched_image_ids)} images")

        sly.logger.debug(f"Finished inference on {len(image_paths)} images")

        f.upload_images_with_anns(image_ids, image_names, anns, output_dataset_id)

        sly.logger.info(f"Finished processing dataset: {dataset_name} with ID: {dataset_id}")

    sly.logger.info("The app finished processing datasets and will be stopped now.")
    sly.fs.remove_dir(g.TMP_DIR)
    sly.logger.debug(f"Removed temporary directory: {g.TMP_DIR}")


if __name__ == "__main__":
    prepare_output_project()
    main()
