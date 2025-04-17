import time
import subprocess
from logger import log

def run_cmd(cmd, capture_output=False):
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout.strip() if capture_output else None


def docker_pull_with_retry(image):
    for attempt in range(3):
        try:
            run_cmd(f"docker pull {image}")
            log.info(f"Successfully pulled {image}")
            return
        except Exception as e:
            log.warning(f"Pull failed for {image} (attempt {attempt + 1}/3)\n{e}")
            if attempt == 2:
                raise
            log.info("Retrying...")
            time.sleep(5)


def docker_push_with_retry(image):
    for attempt in range(3):
        try:
            run_cmd(f"docker push {image}")
            log.info(f"Successfully pushed {image}")
            run_cmd(f"docker rmi {image}")
            return
        except Exception as e:
            log.warning(f"Push failed for {image} (attempt {attempt + 1}/3)\n{e}")
            if attempt == 2:
                raise
            log.info("Retrying...")
            time.sleep(5)


def docker_tag(source_img, target_img):
    run_cmd(f"docker tag {source_img} {target_img}")


def get_image_digest(image):
    return run_cmd(f"docker inspect --format='{{{{index .RepoDigests 0}}}}' {image}", capture_output=True).split('@')[1]


def docker_remove(image):
    try:
        run_cmd(f"docker rmi {image}")
    except Exception as e:
        log.warning(f"Failed to remove {image}: {e}")
