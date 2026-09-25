import os
import re
from pathlib import Path

import requests
from PIL import Image
from io import BytesIO

from logger import logger


# --------------------------------------------------
# Configuration
# --------------------------------------------------

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

PHOTO_FOLDER = Path("assets/holiday_photos")

PHOTO_SIZE = (100, 150)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def safe_filename(location):
    """
    Convert a location into a safe filename.
    """

    filename = location.replace(" ", "_")
    filename = re.sub(r"[^a-zA-Z0-9_-]", "", filename)

    return filename + ".jpg"


# --------------------------------------------------
# Search Unsplash
# --------------------------------------------------

def search_unsplash(location):
    """
    Search Unsplash for a landscape photo of the location.
    """

    if not UNSPLASH_ACCESS_KEY:
        logger.error("UNSPLASH_ACCESS_KEY is not set")
        return None

    url = "https://api.unsplash.com/search/photos"

    params = {
        "query": location,
        "orientation": "landscape",
        "per_page": 5,
        "content_filter": "high",
        "client_id": UNSPLASH_ACCESS_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            logger.warning(
                f"No Unsplash photo found for {location}"
            )
            return None

        # First result is normally the most relevant
        photo = results[0]

        logger.info(
            f"Found photo for {location}: "
            f"{photo['user']['name']}"
        )

        return photo

    except requests.RequestException as e:

        logger.error(
            f"Unsplash search failed for {location}: {e}"
        )

        return None


# --------------------------------------------------
# Download photo
# --------------------------------------------------

def download_photo(photo):
    """
    Download and resize an Unsplash photo.
    """

    location = photo.get("alt_description") or "unknown"

    image_url = photo["urls"]["regular"]

    try:

        response = requests.get(
            image_url,
            timeout=30
        )

        response.raise_for_status()

        image = Image.open(
            BytesIO(response.content)
        )

        # Convert to RGB because we save as JPEG
        image = image.convert("RGB")

        # Crop/resize to exactly 800x533
        image = image.resize(
            PHOTO_SIZE,
            Image.Resampling.LANCZOS
        )

        return image

    except Exception as e:

        logger.error(
            f"Could not download photo: {e}"
        )

        return None


# --------------------------------------------------
# Track Unsplash download
# --------------------------------------------------

def track_download(photo):
    """
    Tell Unsplash that the photo was downloaded.
    """

    try:

        download_location = (
            photo["links"]["download_location"]
        )

        response = requests.get(
            download_location,
            params={
                "client_id": UNSPLASH_ACCESS_KEY
            },
            timeout=15
        )

        response.raise_for_status()

        logger.info(
            f"Unsplash download tracked: {photo['id']}"
        )

    except Exception as e:

        logger.warning(
            f"Could not track Unsplash download: {e}"
        )


# --------------------------------------------------
# Save metadata
# --------------------------------------------------

def save_metadata(location, photo):
    """
    Save photographer information next to the image.
    """

    filename = safe_filename(location)

    metadata_path = (
        PHOTO_FOLDER /
        filename.replace(".jpg", ".txt")
    )

    try:

        photographer = photo["user"]["name"]

        photographer_url = (
            photo["user"]["links"]["html"]
        )

        photo_url = photo["links"]["html"]

        with open(
            metadata_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                f"Photo by {photographer}\n"
            )

            file.write(
                f"Photographer: {photographer_url}\n"
            )

            file.write(
                f"Photo: {photo_url}\n"
            )

            file.write(
                "Source: Unsplash\n"
            )

        logger.info(
            f"Saved photo metadata: {metadata_path}"
        )

    except Exception as e:

        logger.warning(
            f"Could not save photo metadata: {e}"
        )


# --------------------------------------------------
# Prepare one holiday photo
# --------------------------------------------------

def prepare_holiday_photo(location):

    PHOTO_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = safe_filename(location)

    photo_path = PHOTO_FOLDER / filename

    # ----------------------------------------------
    # Already exists?
    # ----------------------------------------------

    if photo_path.exists():

        logger.info(
            f"Holiday photo already exists: {location}"
        )

        return photo_path


    logger.info(
        f"No holiday photo found for {location}"
    )

    logger.info(
        f"Searching Unsplash for {location}"
    )


    # ----------------------------------------------
    # Search
    # ----------------------------------------------

    photo = search_unsplash(location)

    if photo is None:
        return None


    # ----------------------------------------------
    # Download
    # ----------------------------------------------

    image = download_photo(photo)

    if image is None:
        return None


    # ----------------------------------------------
    # Track download
    # ----------------------------------------------

    track_download(photo)


    # ----------------------------------------------
    # Save
    # ----------------------------------------------

    try:

        image.save(
            photo_path,
            format="JPEG",
            quality=85,
            optimize=True
        )

        logger.info(
            f"Saved holiday photo: {photo_path}"
        )

    except Exception as e:

        logger.error(
            f"Could not save photo: {e}"
        )

        return None


    # ----------------------------------------------
    # Save photographer information
    # ----------------------------------------------

    save_metadata(
        location,
        photo
    )


    return photo_path


# --------------------------------------------------
# Prepare all holiday photos
# --------------------------------------------------

def prepare_holiday_photos(holidays):

    logger.info("Checking holiday photos...")

    locations = holidays["location"].unique()

    for location in locations:
        prepare_holiday_photo(location)

    logger.info("Holiday photo check finished")