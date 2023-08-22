import supervisely as sly

import globals as g


def create_output_project() -> int:
    output_project_name = f"{g.PROJECT_NAME}_with_{g.TAG_NAME}_tags"
    output_project = g.api.project.create(
        g.WORKSPACE_ID,
        output_project_name,
        change_name_if_conflict=True,
    )
    sly.logger.info(f"Output project {output_project.name} was created.")
    return output_project.id


def create_output_dataset(dataset_name: str, output_project_id: int) -> int:
    output_dataset = g.api.dataset.create(
        output_project_id,
        dataset_name,
        change_name_if_conflict=True,
    )
    sly.logger.info(f"Output dataset {output_dataset.name} was created.")
    return output_dataset.id


def det_polygon_2_label(rect):
    rect = list(map(int, rect))
    x, y = rect[::2], rect[1::2]
    xmin, ymin, xmax, ymax = min(x), min(y), max(x), max(y)
    rect = sly.Rectangle(ymin, xmin, ymax, xmax)
    label = sly.Label(rect, g.OBJECT_CLASS)
    return label
