import os

from dotenv import load_dotenv

import supervisely as sly


ABSOLUTE_PATH = os.path.dirname(__file__)

# Reading .env files and creting an example of Supervisely API.
if sly.is_development:
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))
api: sly.Api = sly.Api.from_env()

TEAM_ID = sly.io.env.team_id()
WORKSPACE_ID = sly.io.env.workspace_id()
PROJECT_ID = sly.io.env.project_id()
DATASET_ID = sly.io.env.dataset_id(raise_not_found=False)

sly.logger.info(
    f"Team ID: {TEAM_ID}, Workspace ID: {WORKSPACE_ID}, "
    f"Project ID: {PROJECT_ID}, Dataset ID: {DATASET_ID}"
)

PROJECT_NAME = api.project.get_info_by_id(PROJECT_ID).name

TMP_DIR = os.path.join(ABSOLUTE_PATH, "tmp")
TMP_PROJECT_DIR = os.path.join(TMP_DIR, PROJECT_NAME)
os.makedirs(TMP_PROJECT_DIR, exist_ok=True)
sly.logger.debug(f"Temporary project directory was created: {TMP_PROJECT_DIR}")

OUTPUT_DIR = os.path.join(ABSOLUTE_PATH, "output")
PROJECT_DIR = os.path.join(OUTPUT_DIR, PROJECT_NAME)
os.makedirs(PROJECT_DIR, exist_ok=True)
sly.logger.debug(f"Project directory was created: {PROJECT_DIR}")

ARCHIVE_PATH = os.path.join(OUTPUT_DIR, f"{PROJECT_NAME}.tar.gz")

DEVICE = "cuda"
BATCH_SIZE = 2

sly.logger.info(f"Device: {DEVICE}, batch size: {BATCH_SIZE}")
