#!/usr/bin/env python3
"""
Batch Processing Example
------------------------
This script demonstrates how to generate multiple scroll videos
from a list of URLs automatically.
"""

import subprocess
import sys
from typing import List, Tuple


def generate_videos(urls_with_config: List[Tuple[str, int, str, str]]) -> None:
    """
    Generate scroll videos for multiple URLs.

    Args:
        urls_with_config: List of tuples (url, duration, output_name, text_overlay)
    """
    total = len(urls_with_config)

    for idx, (url, duration, output_name, text_overlay) in enumerate(urls_with_config, 1):
        print(f"\n{'='*60}")
        print(f"Processing {idx}/{total}: {url}")
        print(f"{'='*60}\n")

        cmd = [
            "python",
            "../scroll_video_generator.py",
            "--url", url,
            "--duration", str(duration),
            "--output", output_name,
        ]

        if text_overlay:
            cmd.extend(["--text_overlay", text_overlay])

        try:
            result = subprocess.run(cmd, check=True)
            print(f"✓ Successfully created: {output_name}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to create video for {url}")
            print(f"  Error: {e}")
            continue

    print(f"\n{'='*60}")
    print(f"Batch processing complete! Created {total} videos.")
    print(f"{'='*60}\n")


def main():
    """Main entry point for batch processing."""

    # Define your URLs and configurations here
    urls_config = [
        # (url, duration_seconds, output_filename, text_overlay)
        ("https://example.com", 10, "example_com.mp4", "Example.com"),
        ("https://github.com", 20, "github.mp4", "GitHub Homepage"),
        ("https://stackoverflow.com", 15, "stackoverflow.mp4", "Stack Overflow"),
        ("https://news.ycombinator.com", 20, "hackernews.mp4", "Hacker News"),
    ]

    print("Batch Video Generator")
    print(f"Will process {len(urls_config)} URLs\n")

    for idx, (url, duration, output, text) in enumerate(urls_config, 1):
        print(f"{idx}. {url} -> {output} ({duration}s)")

    print("\nStarting in 3 seconds...")
    print("Press Ctrl+C to cancel\n")

    try:
        import time
        time.sleep(3)
    except KeyboardInterrupt:
        print("\nCancelled by user")
        sys.exit(0)

    generate_videos(urls_config)


if __name__ == "__main__":
    main()
