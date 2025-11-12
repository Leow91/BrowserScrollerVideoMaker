#!/usr/bin/env python3
"""
Automated Web Scroll Video Creator
-----------------------------------
This script automatically scrolls through a webpage, records the scrolling process,
and optionally adds logo and text overlays to the final video using FFmpeg.

Requirements:
    - Python 3.x
    - playwright
    - FFmpeg (system-installed)

Usage:
    python scroll_video_generator.py --url https://example.com --duration 15 --output video.mp4
"""

import argparse
import asyncio
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from playwright.async_api import async_playwright


class ScrollVideoGenerator:
    """Main class for generating scroll videos from web pages."""

    def __init__(
        self,
        url: str,
        duration: int,
        output: str,
        logo_path: Optional[str] = None,
        text_overlay: Optional[str] = None,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
    ):
        """
        Initialize the ScrollVideoGenerator.

        Args:
            url: The URL of the webpage to scroll
            duration: Duration of the scroll in seconds
            output: Output video filename
            logo_path: Optional path to logo PNG file
            text_overlay: Optional text to overlay on video
            viewport_width: Browser viewport width
            viewport_height: Browser viewport height
        """
        self.url = url
        self.duration = duration
        self.output = output
        self.logo_path = logo_path
        self.text_overlay = text_overlay
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.temp_video = "temp_raw_scroll.webm"

    def validate_inputs(self) -> None:
        """Validate input parameters and check dependencies."""
        # Check if FFmpeg is installed
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: FFmpeg is not installed or not in PATH.")
            print("Please install FFmpeg: https://ffmpeg.org/download.html")
            sys.exit(1)

        # Check if logo file exists
        if self.logo_path and not os.path.exists(self.logo_path):
            print(f"Error: Logo file not found: {self.logo_path}")
            sys.exit(1)

        # Validate URL
        if not self.url.startswith(("http://", "https://")):
            print("Error: URL must start with http:// or https://")
            sys.exit(1)

    async def record_scroll_video(self) -> None:
        """
        Use Playwright to open the webpage, scroll it smoothly,
        and record the process as a video.
        """
        print(f"Starting browser and loading {self.url}...")

        async with async_playwright() as p:
            # Launch browser with video recording enabled
            browser = await p.chromium.launch(headless=True)

            # Create a context with video recording
            context = await browser.new_context(
                viewport={"width": self.viewport_width, "height": self.viewport_height},
                record_video_dir=".",
                record_video_size={"width": self.viewport_width, "height": self.viewport_height},
            )

            page = await context.new_page()

            try:
                # Navigate to the URL and wait for the page to load
                print("Loading page...")
                await page.goto(self.url, wait_until="networkidle", timeout=60000)

                # Wait a bit for any dynamic content to load
                await page.wait_for_timeout(2000)

                # Get the total scrollable height
                scroll_height = await page.evaluate("document.body.scrollHeight")
                viewport_height = self.viewport_height

                print(f"Page height: {scroll_height}px")
                print(f"Viewport height: {viewport_height}px")

                # Calculate scroll parameters
                total_scroll_distance = scroll_height - viewport_height

                if total_scroll_distance <= 0:
                    print("Warning: Page is shorter than viewport. Recording static view...")
                    await page.wait_for_timeout(self.duration * 1000)
                else:
                    # Calculate smooth scrolling parameters
                    # We want to scroll smoothly, so we use small steps
                    fps = 30  # Assume 30 fps for smooth scrolling
                    total_frames = self.duration * fps
                    pixels_per_frame = total_scroll_distance / total_frames
                    frame_delay_ms = 1000 / fps

                    print(f"Scrolling {total_scroll_distance}px over {self.duration} seconds...")
                    print(f"Scroll speed: {pixels_per_frame:.2f} pixels per frame")

                    # Perform smooth scrolling
                    await page.evaluate(
                        """
                        async ({ duration, scrollHeight, viewportHeight }) => {
                            const totalDistance = scrollHeight - viewportHeight;
                            const fps = 30;
                            const totalFrames = duration * fps;
                            const pixelsPerFrame = totalDistance / totalFrames;
                            const frameDelay = 1000 / fps;

                            let currentPosition = 0;

                            for (let frame = 0; frame < totalFrames; frame++) {
                                currentPosition += pixelsPerFrame;
                                window.scrollTo(0, currentPosition);
                                await new Promise(resolve => setTimeout(resolve, frameDelay));
                            }

                            // Ensure we're at the bottom
                            window.scrollTo(0, totalDistance);
                        }
                        """,
                        {
                            "duration": self.duration,
                            "scrollHeight": scroll_height,
                            "viewportHeight": viewport_height,
                        },
                    )

                print("Scroll complete. Finalizing recording...")

                # Wait a moment before closing to ensure last frames are captured
                await page.wait_for_timeout(1000)

            except Exception as e:
                print(f"Error during recording: {e}")
                raise
            finally:
                # Close the page and context to save the video
                await page.close()
                await context.close()
                await browser.close()

                # Get the video file path
                video_path = await context.video_path() if hasattr(context, 'video_path') else None

                # The video is saved in the record_video_dir with a unique name
                # We need to find and rename it
                video_files = list(Path(".").glob("*.webm"))
                if video_files:
                    # Get the most recent video file
                    latest_video = max(video_files, key=lambda p: p.stat().st_mtime)
                    latest_video.rename(self.temp_video)
                    print(f"Raw video saved as {self.temp_video}")
                else:
                    print("Warning: No video file found!")

    def apply_ffmpeg_overlays(self) -> None:
        """
        Use FFmpeg to add logo and/or text overlays to the raw video.
        """
        if not os.path.exists(self.temp_video):
            print(f"Error: Temporary video file {self.temp_video} not found!")
            sys.exit(1)

        print("Applying overlays with FFmpeg...")

        # Build FFmpeg filter chain
        filters = []

        # Add logo overlay if specified
        if self.logo_path:
            # Position logo in top-right corner with 10px padding
            logo_filter = f"movie={self.logo_path}[logo];[in][logo]overlay=W-w-10:10[out]"
            filters.append(logo_filter)

        # Add text overlay if specified
        if self.text_overlay:
            # Escape special characters in text
            text_escaped = self.text_overlay.replace(":", r"\:")
            text_escaped = text_escaped.replace("'", r"\'")

            # Create text overlay filter
            # Position text at bottom center
            text_filter = (
                f"drawtext=text='{text_escaped}':"
                f"fontsize=48:"
                f"fontcolor=white:"
                f"borderw=2:"
                f"bordercolor=black:"
                f"x=(w-text_w)/2:"
                f"y=h-th-20"
            )
            filters.append(text_filter)

        # Build FFmpeg command
        ffmpeg_cmd = ["ffmpeg", "-i", self.temp_video]

        if filters:
            # Apply video filters
            if self.logo_path and self.text_overlay:
                # Both logo and text
                filter_complex = f"movie={self.logo_path}[logo];[0:v][logo]overlay=W-w-10:10[v1];[v1]drawtext=text='{self.text_overlay.replace(':', r'\:')}':fontsize=48:fontcolor=white:borderw=2:bordercolor=black:x=(w-text_w)/2:y=h-th-20[outv]"
                ffmpeg_cmd.extend(["-filter_complex", filter_complex, "-map", "[outv]"])
            elif self.logo_path:
                # Logo only
                filter_complex = f"movie={self.logo_path}[logo];[0:v][logo]overlay=W-w-10:10"
                ffmpeg_cmd.extend(["-filter_complex", filter_complex])
            elif self.text_overlay:
                # Text only
                text_escaped = self.text_overlay.replace(":", r"\:").replace("'", r"\'")
                vf = f"drawtext=text='{text_escaped}':fontsize=48:fontcolor=white:borderw=2:bordercolor=black:x=(w-text_w)/2:y=h-th-20"
                ffmpeg_cmd.extend(["-vf", vf])

        # Add output settings
        ffmpeg_cmd.extend(
            [
                "-c:v", "libx264",  # Video codec
                "-preset", "medium",  # Encoding preset
                "-crf", "23",  # Quality (lower = better, 18-28 is good range)
                "-pix_fmt", "yuv420p",  # Pixel format for compatibility
                "-y",  # Overwrite output file
                self.output,
            ]
        )

        # Execute FFmpeg command
        print(f"FFmpeg command: {' '.join(ffmpeg_cmd)}")

        try:
            result = subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            print(f"Video successfully created: {self.output}")
        except subprocess.CalledProcessError as e:
            print("FFmpeg error:")
            print(e.stderr)
            sys.exit(1)

    def cleanup(self) -> None:
        """Remove temporary files."""
        if os.path.exists(self.temp_video):
            os.remove(self.temp_video)
            print(f"Cleaned up temporary file: {self.temp_video}")

    async def generate(self) -> None:
        """
        Main method to orchestrate the entire video generation process.
        """
        self.validate_inputs()
        await self.record_scroll_video()
        self.apply_ffmpeg_overlays()
        self.cleanup()
        print(f"\n✓ Video generation complete: {self.output}")


def main():
    """Parse command-line arguments and run the generator."""
    parser = argparse.ArgumentParser(
        description="Automated Web Scroll Video Creator - Record scrolling through a webpage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic usage:
    python scroll_video_generator.py --url https://example.com --duration 15 --output scroll.mp4

  With logo overlay:
    python scroll_video_generator.py --url https://example.com --duration 20 --output scroll.mp4 --logo_path logo.png

  With text overlay:
    python scroll_video_generator.py --url https://example.com --duration 10 --output scroll.mp4 --text_overlay "My Website Tour"

  With both overlays:
    python scroll_video_generator.py --url https://example.com --duration 30 --output scroll.mp4 --logo_path logo.png --text_overlay "Website Demo"
        """,
    )

    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="URL of the webpage to scroll and record",
    )

    parser.add_argument(
        "--duration",
        type=int,
        required=True,
        help="Duration of the scroll in seconds (e.g., 15)",
    )

    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output video filename (e.g., output.mp4)",
    )

    parser.add_argument(
        "--logo_path",
        type=str,
        default=None,
        help="Optional: Path to logo PNG file for overlay (top-right corner)",
    )

    parser.add_argument(
        "--text_overlay",
        type=str,
        default=None,
        help="Optional: Text to overlay on video (bottom center)",
    )

    parser.add_argument(
        "--width",
        type=int,
        default=1920,
        help="Browser viewport width in pixels (default: 1920)",
    )

    parser.add_argument(
        "--height",
        type=int,
        default=1080,
        help="Browser viewport height in pixels (default: 1080)",
    )

    args = parser.parse_args()

    # Create generator instance
    generator = ScrollVideoGenerator(
        url=args.url,
        duration=args.duration,
        output=args.output,
        logo_path=args.logo_path,
        text_overlay=args.text_overlay,
        viewport_width=args.width,
        viewport_height=args.height,
    )

    # Run the async generator
    asyncio.run(generator.generate())


if __name__ == "__main__":
    main()
