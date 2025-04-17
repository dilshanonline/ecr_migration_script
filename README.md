# GCP to AWS ECR Image Migration Tool

Safely migrate container images from **Google Artifact Registry** to **Amazon Elastic Container Registry (ECR)** — with digest validation, dry-run mode, tag filtering, and full visibility. Built for platform migrations, DevOps teams, and engineers who want reliable and auditable image migration. This tool pulls Docker images from a GCP registry, verifies the digest, retags them optionally, and pushes them to AWS ECR — ensuring no data loss or tag mismatch.

Note: Google supports hierarchical image names (e.g. folder/app/image), but AWS ECR requires flat repository names. This tool can handle that transformation by retagging appropriately to maintain image identity.

---

## ✨ Features

- ✅ **Dry-run mode** to preview actions without making changes
- 🔍 **Tag prefix filtering** to migrate only what you need
- 🏷️ **Tag prefix replacement** (e.g., convert `v1.0.0` to `prod-1.0.0`)
- 🧪 **Digest validation** to ensure image integrity
- 🧀 **Safe cleanup** of pulled images (after digest match)
- 📜 **Readable logs** with timestamped file output
- 🔁 **Retry logic** for `docker pull` and `push`
- 👤 **Interactive confirmation** before migration
- ⚒️ Built using **Python + Typer** CLI framework
- 🔓 **Open-source** and team-friendly

---

## 🧠 Why This Exists

This tool was built as part of a **platform migration** from **GCP to AWS**. With over 20 image repositories to migrate, we faced challenges like:

- Risk of overwriting or pushing the wrong tags
- Potential for digest mismatches
- Fear of permanent data loss once GCP was decommissioned
- Manual effort needed for repetitive and error-prone tasks

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/dilshanonline/ecr_migration_script.git
cd ecr_migration_script
```

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Edit `config.py` to set your migration parameters:

```python
# config.py

# SOURCE CONFIGURATION
PROJECT_ID = "my-project-id"  # Replace with your actual project ID
LOCATION = "europe"  # Replace with your actual location
SOURCE_REPO = "eu.gcr.io" # Replace with your actual source repository
IMAGE_PATH = "repo_name/old_image_name"  # Replace with your actual image path
SOURCE_FULL_REPO = f"europe-docker.pkg.dev/{PROJECT_ID}/{SOURCE_REPO}/{IMAGE_PATH}" # Replace with your actual full source repository

# TARGET CONFIGURATION
TARGET_REGISTRY = "0123456789.dkr.ecr.eu-west-1.amazonaws.com" # Replace with your actual target registry
TARGET_PATH = "new_image_name"  # Replace with your actual target image path
AWS_REGION = "eu-west-1" # Replace with your actual AWS region
DEFAULT_LIMIT = 2  # Default limit for the number of images to process
RETAGGED_LIST_FILE = "retagged_images.txt" # File to store the list of retagged images
LOG_DIR = "logs" # Directory to store logs
SSO_PROFILE = "aws-sso-profile"  # Replace with your actual AWS SSO profile name
```

You can also export environment variables if preferred.

---

## 🚀 Usage

Run with `python -m main` from the project root:

```bash
# Show help
python -m main --help
```

```bash
# Dry run
python -m main --dry-run --filter-tag-prefix v --change-tag prod-
```
```bash
# Migration
python -m main --filter-tag-prefix v --change-tag prod-
```

### Options:

| Flag                 | Description                                      |
|----------------------|--------------------------------------------------|
| `--dry-run`          | Preview migration without pulling/pushing       |
| `--filter-tag-prefix`| Only migrate tags starting with a prefix (e.g., `v`) |
| `--change-tag`       | Change the tag prefix (e.g., `prod-`)           |

You'll be shown a list of available images and prompted to confirm how many to migrate.

---

## 🛡️ Safety Features

- Verifies image digests after retagging.
- Aborts if any mismatch is detected.
- Requires user confirmation before starting.
- Clears pulled images only after successful validation.

---

## 📝 Example Output

```bash
Dry-run mode: True
Filtering only tags starting with: v

Previewing available images:
- gcr.io/project/image:v1.2.3
- gcr.io/project/image:v1.2.2

Do you want to continue? (Y/y to proceed): y
How many images to migrate? (default: 2): 2
DRY-RUN: Would pull gcr.io/project/image:v1.2.3
DRY-RUN: Would tag 123456789.dkr.ecr.eu-west-1.amazonaws.com/image:prod-1.2.3
...
```

---

## 🗃️ Logs

All logs are saved in the `logs/` directory with a timestamped `.log` file.

---

## 🤝 Contributing

Pull requests, issues, and suggestions are welcome! Feel free to fork and enhance the tool for your use cases.

---

## 📜 License

This script is free to use and modify for your personal or professional use.  
Licensed under the [MIT License](LICENSE).

---


