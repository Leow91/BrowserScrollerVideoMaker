#!/usr/bin/env python3
"""
Social Media Platform Presets
------------------------------
Pre-configured video settings optimized for different social media platforms.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


@dataclass
class VideoPreset:
    """Video preset configuration for a platform."""

    name: str
    display_name: str
    width: int
    height: int
    min_duration: int
    max_duration: int
    recommended_duration: int
    aspect_ratio: str
    fps: int = 30
    description: str = ""
    orientation: str = ""  # portrait, landscape, square


class SocialPlatform(str, Enum):
    """Supported social media platforms."""

    CUSTOM = "custom"
    INSTAGRAM_FEED = "instagram_feed"
    INSTAGRAM_STORY = "instagram_story"
    INSTAGRAM_REEL = "instagram_reel"
    FACEBOOK_FEED = "facebook_feed"
    FACEBOOK_STORY = "facebook_story"
    WHATSAPP_STATUS = "whatsapp_status"
    TIKTOK = "tiktok"
    YOUTUBE_SHORT = "youtube_short"
    YOUTUBE_VIDEO = "youtube_video"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    PINTEREST = "pinterest"
    SNAPCHAT = "snapchat"


# Platform presets database
PLATFORM_PRESETS: Dict[SocialPlatform, VideoPreset] = {
    SocialPlatform.CUSTOM: VideoPreset(
        name="custom",
        display_name="🎨 Custom Settings",
        width=1920,
        height=1080,
        min_duration=5,
        max_duration=300,
        recommended_duration=15,
        aspect_ratio="16:9",
        orientation="landscape",
        description="Custom video settings - configure manually",
    ),
    SocialPlatform.INSTAGRAM_FEED: VideoPreset(
        name="instagram_feed",
        display_name="📷 Instagram Feed Post",
        width=1080,
        height=1080,
        min_duration=3,
        max_duration=60,
        recommended_duration=15,
        aspect_ratio="1:1",
        orientation="square",
        description="Square format for Instagram feed posts (max 60s)",
    ),
    SocialPlatform.INSTAGRAM_STORY: VideoPreset(
        name="instagram_story",
        display_name="📱 Instagram Story",
        width=1080,
        height=1920,
        min_duration=3,
        max_duration=15,
        recommended_duration=10,
        aspect_ratio="9:16",
        orientation="portrait",
        description="Vertical format for Instagram Stories (max 15s)",
    ),
    SocialPlatform.INSTAGRAM_REEL: VideoPreset(
        name="instagram_reel",
        display_name="🎬 Instagram Reel",
        width=1080,
        height=1920,
        min_duration=3,
        max_duration=90,
        recommended_duration=30,
        aspect_ratio="9:16",
        orientation="portrait",
        description="Vertical format for Instagram Reels (max 90s)",
    ),
    SocialPlatform.FACEBOOK_FEED: VideoPreset(
        name="facebook_feed",
        display_name="📘 Facebook Feed Post",
        width=1280,
        height=720,
        min_duration=3,
        max_duration=240,
        recommended_duration=30,
        aspect_ratio="16:9",
        orientation="landscape",
        description="Landscape format for Facebook feed (max 240s)",
    ),
    SocialPlatform.FACEBOOK_STORY: VideoPreset(
        name="facebook_story",
        display_name="📱 Facebook Story",
        width=1080,
        height=1920,
        min_duration=3,
        max_duration=20,
        recommended_duration=10,
        aspect_ratio="9:16",
        orientation="portrait",
        description="Vertical format for Facebook Stories (max 20s)",
    ),
    SocialPlatform.WHATSAPP_STATUS: VideoPreset(
        name="whatsapp_status",
        display_name="💬 WhatsApp Status",
        width=1080,
        height=1920,
        min_duration=3,
        max_duration=30,
        recommended_duration=15,
        aspect_ratio="9:16",
        orientation="portrait",
        description="Vertical format for WhatsApp Status (max 30s)",
    ),
    SocialPlatform.TIKTOK: VideoPreset(
        name="tiktok",
        display_name="🎵 TikTok",
        width=1080,
        height=1920,
        min_duration=3,
        max_duration=180,
        recommended_duration=30,
        aspect_ratio="9:16",
        orientation="portrait",
        description="Vertical format for TikTok videos (max 3min)",
    ),
    SocialPlatform.YOUTUBE_SHORT: VideoPreset(
        name="youtube_short",
        display_name="▶️ YouTube Shorts",
        width=1080,
        height=1920,
        min_duration=3,
        max_duration=60,
        recommended_duration=30,
        aspect_ratio="9:16",
        orientation="portrait",
        description="Vertical format for YouTube Shorts (max 60s)",
    ),
    SocialPlatform.YOUTUBE_VIDEO: VideoPreset(
        name="youtube_video",
        display_name="▶️ YouTube Video",
        width=1920,
        height=1080,
        min_duration=10,
        max_duration=300,
        recommended_duration=60,
        aspect_ratio="16:9",
        orientation="landscape",
        description="Landscape format for YouTube videos (standard)",
    ),
    SocialPlatform.TWITTER: VideoPreset(
        name="twitter",
        display_name="🐦 Twitter/X",
        width=1280,
        height=720,
        min_duration=3,
        max_duration=140,
        recommended_duration=30,
        aspect_ratio="16:9",
        orientation="landscape",
        description="Landscape format for Twitter/X (max 2:20)",
    ),
    SocialPlatform.LINKEDIN: VideoPreset(
        name="linkedin",
        display_name="💼 LinkedIn",
        width=1280,
        height=720,
        min_duration=3,
        max_duration=600,
        recommended_duration=60,
        aspect_ratio="16:9",
        orientation="landscape",
        description="Landscape format for LinkedIn posts (max 10min)",
    ),
    SocialPlatform.PINTEREST: VideoPreset(
        name="pinterest",
        display_name="📌 Pinterest Pin",
        width=1080,
        height=1920,
        min_duration=4,
        max_duration=60,
        recommended_duration=15,
        aspect_ratio="9:16",
        orientation="portrait",
        description="Vertical format for Pinterest Video Pins (max 60s)",
    ),
    SocialPlatform.SNAPCHAT: VideoPreset(
        name="snapchat",
        display_name="👻 Snapchat",
        width=1080,
        height=1920,
        min_duration=3,
        max_duration=60,
        recommended_duration=10,
        aspect_ratio="9:16",
        orientation="portrait",
        description="Vertical format for Snapchat (max 60s)",
    ),
}


def get_preset(platform: SocialPlatform) -> VideoPreset:
    """
    Get video preset for a platform.

    Args:
        platform: Social media platform

    Returns:
        VideoPreset configuration
    """
    return PLATFORM_PRESETS.get(platform, PLATFORM_PRESETS[SocialPlatform.CUSTOM])


def get_all_platforms() -> list[tuple[str, str]]:
    """
    Get all available platforms for dropdown.

    Returns:
        List of (value, display_name) tuples
    """
    return [
        (platform.value, preset.display_name)
        for platform, preset in PLATFORM_PRESETS.items()
    ]


def get_platform_choices() -> list[str]:
    """
    Get platform choices for Gradio dropdown.

    Returns:
        List of display names
    """
    return [preset.display_name for preset in PLATFORM_PRESETS.values()]


def get_platform_from_display_name(display_name: str) -> SocialPlatform:
    """
    Get platform enum from display name.

    Args:
        display_name: Display name from dropdown

    Returns:
        SocialPlatform enum
    """
    for platform, preset in PLATFORM_PRESETS.items():
        if preset.display_name == display_name:
            return platform
    return SocialPlatform.CUSTOM


def validate_duration(platform: SocialPlatform, duration: int) -> tuple[bool, Optional[str]]:
    """
    Validate duration for a platform.

    Args:
        platform: Social media platform
        duration: Video duration in seconds

    Returns:
        Tuple of (is_valid, error_message)
    """
    preset = get_preset(platform)

    if duration < preset.min_duration:
        return False, f"Duration too short for {preset.display_name}. Minimum: {preset.min_duration}s"

    if duration > preset.max_duration:
        return False, f"Duration too long for {preset.display_name}. Maximum: {preset.max_duration}s"

    return True, None


def get_platform_info(platform: SocialPlatform) -> str:
    """
    Get formatted information about a platform.

    Args:
        platform: Social media platform

    Returns:
        Formatted info string
    """
    preset = get_preset(platform)

    info = f"""
**{preset.display_name}**

📐 Resolution: {preset.width}x{preset.height} ({preset.aspect_ratio})
⏱️ Duration: {preset.min_duration}-{preset.max_duration}s (recommended: {preset.recommended_duration}s)
📱 Orientation: {preset.orientation.capitalize()}
🎥 FPS: {preset.fps}

{preset.description}
    """

    return info.strip()


def get_all_platforms_info() -> str:
    """
    Get information about all platforms.

    Returns:
        Formatted string with all platform info
    """
    info_list = []

    for platform in SocialPlatform:
        if platform == SocialPlatform.CUSTOM:
            continue
        preset = get_preset(platform)
        info_list.append(
            f"{preset.display_name}: {preset.width}x{preset.height} "
            f"({preset.aspect_ratio}), {preset.recommended_duration}s"
        )

    return "\n".join(info_list)


# Quick reference guide
PLATFORM_QUICK_REFERENCE = """
# Social Media Video Specifications Quick Reference

## Vertical Formats (9:16 - Portrait)
- 📱 Instagram Story: 1080x1920, max 15s
- 🎬 Instagram Reel: 1080x1920, max 90s
- 📱 Facebook Story: 1080x1920, max 20s
- 💬 WhatsApp Status: 1080x1920, max 30s
- 🎵 TikTok: 1080x1920, max 180s
- ▶️ YouTube Shorts: 1080x1920, max 60s
- 📌 Pinterest Pin: 1080x1920, max 60s
- 👻 Snapchat: 1080x1920, max 60s

## Square Format (1:1)
- 📷 Instagram Feed: 1080x1080, max 60s

## Landscape Formats (16:9)
- 📘 Facebook Feed: 1280x720, max 240s
- ▶️ YouTube Video: 1920x1080, max 300s
- 🐦 Twitter/X: 1280x720, max 140s
- 💼 LinkedIn: 1280x720, max 600s

## Recommendations
- Use vertical (9:16) for mobile-first content
- Use square (1:1) for Instagram feed for best compatibility
- Use landscape (16:9) for traditional/desktop viewing
- Keep videos under 30s for maximum engagement
- Use 30 FPS for smooth scrolling videos
"""


if __name__ == "__main__":
    # Display quick reference
    print(PLATFORM_QUICK_REFERENCE)

    # Show all platform details
    print("\n" + "=" * 60)
    print("DETAILED PLATFORM SPECIFICATIONS")
    print("=" * 60 + "\n")

    for platform in SocialPlatform:
        if platform == SocialPlatform.CUSTOM:
            continue
        print(get_platform_info(platform))
        print("-" * 60)
