from typing import List

import supervisely as sly

import globals as g


def create_output_project() -> int:
    """Creates output project with name using input project name and tag name.

    :return: ID of the created output project.
    :rtype: int
    """
    output_project_name = f"{g.PROJECT_NAME}_with_{g.TAG_NAME}_tags"
    output_project = g.api.project.create(
        g.WORKSPACE_ID,
        output_project_name,
        change_name_if_conflict=True,
    )
    sly.logger.info(f"Output project {output_project.name} was created.")
    return output_project.id


def create_output_dataset(dataset_name: str, output_project_id: int) -> int:
    """Creates output dataset with name using input dataset name.

    :param dataset_name: input dataset name, which will be used to create output dataset name.
    :type dataset_name: str
    :param output_project_id: ID of the output project to create dataset in.
    :type output_project_id: int
    :return: ID of the created output dataset.
    :rtype: int
    """
    output_dataset = g.api.dataset.create(
        output_project_id,
        dataset_name,
        change_name_if_conflict=True,
    )
    sly.logger.info(f"Output dataset {output_dataset.name} was created.")
    return output_dataset.id


def det_polygon_2_label(rect: List) -> sly.Label:
    """Converts predicted polygon to Supervisely label rectangle.

    :param rect: predicted polygon.
    :type rect: List
    :return: Supervisely label rectangle.
    :rtype: sly.Label
    """
    rect = list(map(int, rect))
    x, y = rect[::2], rect[1::2]
    xmin, ymin, xmax, ymax = min(x), min(y), max(x), max(y)
    rect = sly.Rectangle(ymin, xmin, ymax, xmax)
    label = sly.Label(rect, g.OBJECT_CLASS)
    return label


def upload_images_with_anns(
    image_paths: List[str],
    image_names: List[str],
    anns: List[sly.Annotation],
    output_dataset_id: int,
) -> None:
    """Uploads images with annotations to Supervisely.

    :param image_paths: list of local paths to the images.
    :type image_paths: List[str]
    :param image_names: list of image names (filenames).
    :type image_names: List[str]
    :param anns: list of Supervisely annotations.
    :type anns: List[sly.Annotation]
    :param output_dataset_id: ID of the dataset to upload images with annotations to.
    :type output_dataset_id: int
    :return: None
    :rtype: None
    """
    sly.logger.debug(f"Uploading {len(image_paths)} images to dataset with ID: {output_dataset_id}")

    with sly.tqdm_sly(total=len(image_paths), message="Uploading images") as pbar:
        for batched_img_paths, batched_img_names, batched_anns in zip(
            sly.batched(image_paths), sly.batched(image_names), sly.batched(anns)
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

    sly.logger.debug(
        f"Finished uploading {len(image_paths)} images to dataset with ID: {output_dataset_id}"
    )
