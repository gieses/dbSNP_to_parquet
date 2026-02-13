#!/usr/bin/env python3
"""Download utilities for dbSNP to Parquet conversion."""

import subprocess
from pathlib import Path
from loguru import logger
from pyvariantdb.const import get_cache_dir


def download_with_aria2(url: str, output_dir: Path, filename: str = None):
    """
    Download a file using aria2c.

    Args:
        url: The URL to download from
        output_dir: Directory where the file should be saved
        filename: Optional custom filename (defaults to name from URL)

    Returns:
        Path: Path to the downloaded file

    Raises:
        RuntimeError: If aria2c is not installed or download fails
    """
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build aria2c command
    cmd = [
        "aria2c",
        "--dir",
        str(output_dir),
        "--max-connection-per-server=16",  # Use up to 16 connections per server
        "--split=16",  # Split file into 16 pieces for parallel download
        "--min-split-size=1M",  # Minimum size for splitting
        "--continue=true",  # Continue partial downloads
        "--allow-overwrite=true",  # Allow overwriting existing files
        "--auto-file-renaming=false",  # Don't auto-rename files
    ]

    if filename:
        cmd.extend(["--out", filename])

    cmd.append(url)

    # Run aria2c
    logger.info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        logger.error(f"aria2c stderr: {result.stderr}")
        raise RuntimeError(f"Failed to download {url}: {result.stderr}")

    # Determine output path
    if filename:
        output_path = output_dir / filename
    else:
        output_path = output_dir / url.split("/")[-1]

    return output_path


def download_dbsnp():
    """
    Download dbSNP VCF file and its index from NCBI's FTP server using aria2.

    Downloads:
    - GCF_000001405.40.gz (main VCF file)
    - GCF_000001405.40.gz.tbi (index file)

    Uses aria2c for fast multi-connection downloads.
    """
    logger.info("Starting dbSNP download with aria2...")

    urls = [
        "https://ftp.ncbi.nih.gov/snp/latest_release/VCF/GCF_000001405.40.gz",
        "https://ftp.ncbi.nih.gov/snp/latest_release/VCF/GCF_000001405.40.gz.tbi",
    ]
    destination_dir = get_cache_dir()
    logger.info(f"Destination directory: {destination_dir}")

    for url in urls:
        try:
            filename = url.split("/")[-1]
            logger.info(f"Downloading {url}...")
            output_path = download_with_aria2(url, destination_dir, filename)
            logger.info(f"✓ Successfully downloaded to {output_path}")
        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")
            raise

    logger.info("Download completed successfully!")


if __name__ == "__main__":
    download_dbsnp()
