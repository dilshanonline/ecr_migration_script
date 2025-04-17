# migrate_images/gcloud.py

import json
import re
import subprocess
from packaging.version import Version, InvalidVersion
from config import SOURCE_FULL_REPO
from logger import log

TAG_FILTER = None


def set_tag_filter(prefix):
    global TAG_FILTER
    TAG_FILTER = prefix


def run_cmd(cmd, capture_output=False):
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout.strip() if capture_output else None


def list_versioned_images():
    cmd = f"gcloud artifacts docker images list {SOURCE_FULL_REPO} --include-tags --format=json"
    raw_output = run_cmd(cmd, capture_output=True)
    parsed = json.loads(raw_output)
    versioned = []

    def tag_sort_key(tag):
        try:
            normalized = tag.lstrip('vV')
            return (0, Version(normalized))
        except InvalidVersion:
            return (1, tag.lower())

    for entry in parsed:
        tags = entry.get("tags", [])
        for tag in tags:
            log.debug(f"Found tag → '{tag}'")
            if TAG_FILTER and not tag.startswith(TAG_FILTER):
                continue
            versioned.append((entry['package'], tag))

    versioned.sort(key=lambda x: tag_sort_key(x[1]), reverse=True)
    return versioned
