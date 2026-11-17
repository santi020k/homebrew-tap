"""Validate packaging source without loading or installing formulae/casks."""
import argparse
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def sources(root):
    return sorted(str(path.relative_to(root)) for folder in ("Formula", "Casks")
                  for path in (root / folder).rglob("*.rb"))


def select(root, base=None, head="HEAD"):
    available = sources(root)
    if not base:
        return available
    environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    try:
        ancestor = subprocess.check_output(
            ["git", "merge-base", "--", base, head], cwd=root, env=environment, text=True, stderr=subprocess.PIPE).strip()
        changed = subprocess.check_output(
            ["git", "diff", "--no-renames", "--name-only", "-z", ancestor, head],
            cwd=root, env=environment, stderr=subprocess.PIPE).decode().split("\0")
    except subprocess.CalledProcessError:
        return available
    selected = []
    for path in filter(None, changed):
        if path in ("README.md", "LICENSE"):
            continue
        if path not in available:
            return available
        selected.append(path)
    return sorted(selected)


def validate_identity(text):
    checksums = re.findall(r'^\s*sha256 "([^"]+)"\s*$', text, re.MULTILINE)
    urls = re.findall(r'^\s*url "([^"]+)"\s*$', text, re.MULTILINE)
    if len(checksums) != 1 or not re.fullmatch(r"[a-f0-9]{64}", checksums[0]):
        raise ValueError("Expected one literal SHA-256 digest")
    if len(urls) != 1:
        raise ValueError("Expected one versioned upstream URL")
    url = urls[0]
    if "#{version}" in url:
        versions = re.findall(r'^\s*version "([0-9]+\.[0-9]+\.[0-9]+)"\s*$', text, re.MULTILINE)
        if len(versions) != 1:
            raise ValueError("Interpolated URL requires one literal stable version")
        url = url.replace("#{version}", versions[0])
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.query or parsed.fragment
            or not re.fullmatch(r"/santi020k/[a-zA-Z0-9_.-]+/releases/download/[^/]*[0-9]+\.[0-9]+\.[0-9]+/[^/]+", parsed.path)
            or "#{" in url):
        raise ValueError("Expected an immutable versioned santi020k GitHub release asset URL")
    version = re.search(r"([0-9]+\.[0-9]+\.[0-9]+)/", parsed.path).group(1)
    if version not in parsed.path.rsplit("/", 1)[1]:
        raise ValueError("Asset filename must identify the same release version")


def check(root, path):
    file = root / path
    if file.is_symlink():
        raise ValueError("Packaging sources must not be symlinks")
    validate_identity(file.read_text())
    subprocess.run(["ruby", "-c", str(file)], check=True)
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--kind", choices=["Formula", "Casks"])
    args = parser.parse_args()
    paths = select(ROOT, args.base, args.head)
    if args.kind:
        paths = [path for path in paths if path.startswith(args.kind + "/")]
    if not sources(ROOT):
        raise ValueError("Tap contains no packaging sources")
    with ThreadPoolExecutor(max_workers=2) as executor:
        for path in executor.map(lambda path: check(ROOT, path), paths):
            print("Validated " + path)
    print(f"Validated {len(paths)} packaging source(s); no packages installed")


if __name__ == "__main__":
    main()
