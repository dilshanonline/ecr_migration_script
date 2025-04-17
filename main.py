# migrate_images/main.py

import typer
import os
import config
from logger import log
from gcloud import list_versioned_images, set_tag_filter
from docker_utils import (
    docker_pull_with_retry, docker_tag, get_image_digest, docker_remove
)
from ecr_utils import ecr_login, push_images_to_ecr

app = typer.Typer()


def pull_and_retag_images(image_list, dry_run, tag_prefix_change):
    with open(config.RETAGGED_LIST_FILE, 'w') as retagged:
        for image, tag in image_list:
            original_tag = tag
            if tag_prefix_change:
                tag = f"{tag_prefix_change}{tag[1:]}"
                log.info(f"Changing tag prefix: {original_tag} -> {tag}")

            source_img = f"{image}:{original_tag}"
            target_img = f"{config.TARGET_REGISTRY}/{config.TARGET_PATH}:{tag}"

            if dry_run:
                log.info(f"DRY-RUN: Would pull {source_img}")
                log.info(f"DRY-RUN: Would tag {target_img}")
                retagged.write(f"{target_img}\n")
                continue

            docker_pull_with_retry(source_img)
            docker_tag(source_img, target_img)

            source_digest = get_image_digest(source_img)
            target_digest = get_image_digest(target_img)

            if source_digest != target_digest:
                log.error("Digest mismatch! Aborting.")
                raise RuntimeError("Digest mismatch")

            log.info("Digests match. Safe to delete source image.")
            docker_remove(source_img)
            retagged.write(f"{target_img}\n")


@app.command()
def migrate(
    dry_run: bool = typer.Option(False, help="Run in dry mode without pushing"),
    change_tag: str = typer.Option("", help="Change tag prefix (e.g. 'prod-')"),
    filter_tag_prefix: str = typer.Option("", help="Filter tags starting with this prefix")
):
    log.info(f"Dry-run mode: {dry_run}")
    if change_tag:
        log.info(f"Tag prefix override: v* -> {change_tag}*")
    if filter_tag_prefix:
        log.info(f"Filtering only tags starting with: {filter_tag_prefix}\n")
        set_tag_filter(filter_tag_prefix)
    else:
        log.info("No tag filter applied. Using all tags.")

    versioned_images = list_versioned_images()
    if not versioned_images:
        log.error("No matching tagged images found.")
        raise typer.Exit(code=1)

    print("\nPreviewing available images:")
    for img, tag in versioned_images:
        print(f"- {img}:{tag}")

    confirm = input("\nDo you want to continue? (Y/y to proceed): ")
    if confirm.lower() != 'y':
        print("Migration cancelled.")
        raise typer.Exit()

    try:
        limit = int(input(f"How many images to migrate? (default: {config.DEFAULT_LIMIT}): ") or config.DEFAULT_LIMIT)
    except ValueError:
        limit = config.DEFAULT_LIMIT

    selected_images = versioned_images[:limit]
    pull_and_retag_images(selected_images, dry_run, change_tag)

    if not dry_run:
        ecr_login()
        push_images_to_ecr()

    os.remove(config.RETAGGED_LIST_FILE)
    log.info("\n\nMigration completed.")


if __name__ == "__main__":
    app()
