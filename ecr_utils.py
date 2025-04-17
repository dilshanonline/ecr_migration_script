import subprocess
from concurrent.futures import ThreadPoolExecutor
from logger import log
from docker_utils import docker_push_with_retry
from config import AWS_REGION, TARGET_REGISTRY, RETAGGED_LIST_FILE, SSO_PROFILE


def run_cmd(cmd, capture_output=False):
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout.strip() if capture_output else None


def ecr_login():
    run_cmd(f"aws ecr get-login-password --region {AWS_REGION} --profile {SSO_PROFILE} | docker login --username AWS --password-stdin {TARGET_REGISTRY}")
    log.info("Login Succeeded")


def push_images_to_ecr():
    with open(RETAGGED_LIST_FILE) as f:
        images = [line.strip() for line in f if line.strip()]

    with ThreadPoolExecutor(max_workers=4) as executor:
        for image in images:
            executor.submit(docker_push_with_retry, image)
