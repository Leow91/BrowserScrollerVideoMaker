#!/usr/bin/env python3
"""
Configuration Management
------------------------
Centralized configuration using Pydantic for validation and type safety.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Application configuration with validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application Settings
    app_name: str = Field(default="Scroll Video Generator", description="Application name")
    app_version: str = Field(default="1.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")

    # Video Generation Settings
    default_duration: int = Field(default=15, ge=1, le=300, description="Default video duration in seconds")
    default_width: int = Field(default=1920, ge=640, le=3840, description="Default viewport width")
    default_height: int = Field(default=1080, ge=480, le=2160, description="Default viewport height")
    default_fps: int = Field(default=30, ge=15, le=60, description="Frames per second")

    # FFmpeg Settings
    ffmpeg_crf: int = Field(default=23, ge=0, le=51, description="FFmpeg CRF quality (lower = better)")
    ffmpeg_preset: str = Field(default="medium", description="FFmpeg encoding preset")

    # Browser Settings
    browser_headless: bool = Field(default=True, description="Run browser in headless mode")
    browser_timeout: int = Field(default=60000, description="Browser page load timeout (ms)")
    page_wait_time: int = Field(default=2000, description="Time to wait after page load (ms)")

    # Workflow Settings
    max_concurrent_jobs: int = Field(default=3, ge=1, le=10, description="Maximum concurrent video jobs")
    workflow_dir: Path = Field(default=Path("workflows"), description="Directory for workflow files")
    output_dir: Path = Field(default=Path("output"), description="Directory for output videos")
    temp_dir: Path = Field(default=Path("temp"), description="Directory for temporary files")

    # Link Discovery Settings
    max_links_per_category: int = Field(default=100, ge=1, le=1000, description="Max links per category")
    link_discovery_timeout: int = Field(default=30, ge=5, le=120, description="Link discovery timeout (seconds)")

    # Logging Settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[Path] = Field(default=None, description="Log file path")
    log_rotation: str = Field(default="10 MB", description="Log rotation size")

    # GUI Settings
    gui_host: str = Field(default="127.0.0.1", description="GUI server host")
    gui_port: int = Field(default=7860, ge=1024, le=65535, description="GUI server port")
    gui_share: bool = Field(default=False, description="Create public share link")

    # Security Settings
    allowed_domains: list[str] = Field(default_factory=list, description="Allowed domains (empty = all)")
    blocked_domains: list[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1", "0.0.0.0"],
        description="Blocked domains for SSRF protection"
    )

    # Performance Settings
    enable_caching: bool = Field(default=True, description="Enable page content caching")
    cache_ttl: int = Field(default=3600, ge=0, description="Cache TTL in seconds")

    @field_validator("workflow_dir", "output_dir", "temp_dir", mode="before")
    @classmethod
    def create_directories(cls, v):
        """Create directories if they don't exist."""
        path = Path(v) if not isinstance(v, Path) else v
        path.mkdir(parents=True, exist_ok=True)
        return path

    @field_validator("ffmpeg_preset")
    @classmethod
    def validate_preset(cls, v):
        """Validate FFmpeg preset."""
        valid_presets = ["ultrafast", "superfast", "veryfast", "faster", "fast",
                        "medium", "slow", "slower", "veryslow"]
        if v not in valid_presets:
            raise ValueError(f"Invalid preset. Must be one of: {', '.join(valid_presets)}")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Invalid log level. Must be one of: {', '.join(valid_levels)}")
        return v_upper

    def get_temp_video_path(self, job_id: str = "temp") -> Path:
        """Get temporary video path for a job."""
        return self.temp_dir / f"{job_id}_raw.webm"

    def get_output_video_path(self, filename: str) -> Path:
        """Get output video path."""
        return self.output_dir / filename

    def is_domain_allowed(self, domain: str) -> bool:
        """Check if domain is allowed."""
        # If no allowed domains specified, all are allowed (except blocked)
        if not self.allowed_domains:
            return domain not in self.blocked_domains

        # Check if domain is in allowed list and not in blocked list
        return domain in self.allowed_domains and domain not in self.blocked_domains


# Global configuration instance
config = AppConfig()


def load_config(env_file: Optional[str] = None) -> AppConfig:
    """
    Load configuration from environment or .env file.

    Args:
        env_file: Path to .env file (optional)

    Returns:
        AppConfig instance
    """
    if env_file and os.path.exists(env_file):
        return AppConfig(_env_file=env_file)
    return AppConfig()


def save_default_env_file(path: str = ".env.example"):
    """
    Save an example .env file with all available settings.

    Args:
        path: Path to save the file
    """
    example_content = """# Scroll Video Generator Configuration
# Copy this file to .env and customize as needed

# Application Settings
APP_NAME=Scroll Video Generator
APP_VERSION=1.1.0
DEBUG=false

# Video Generation Settings
DEFAULT_DURATION=15
DEFAULT_WIDTH=1920
DEFAULT_HEIGHT=1080
DEFAULT_FPS=30

# FFmpeg Settings
FFMPEG_CRF=23
FFMPEG_PRESET=medium

# Browser Settings
BROWSER_HEADLESS=true
BROWSER_TIMEOUT=60000
PAGE_WAIT_TIME=2000

# Workflow Settings
MAX_CONCURRENT_JOBS=3
WORKFLOW_DIR=workflows
OUTPUT_DIR=output
TEMP_DIR=temp

# Link Discovery
MAX_LINKS_PER_CATEGORY=100
LINK_DISCOVERY_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_ROTATION=10 MB

# GUI Settings
GUI_HOST=127.0.0.1
GUI_PORT=7860
GUI_SHARE=false

# Security
# ALLOWED_DOMAINS=example.com,mysite.com
BLOCKED_DOMAINS=localhost,127.0.0.1,0.0.0.0

# Performance
ENABLE_CACHING=true
CACHE_TTL=3600
"""

    with open(path, "w") as f:
        f.write(example_content)

    print(f"Example configuration saved to: {path}")


if __name__ == "__main__":
    # Generate example .env file
    save_default_env_file()

    # Display current configuration
    print("\nCurrent Configuration:")
    print("=" * 50)
    cfg = load_config()
    for field_name, field_info in cfg.model_fields.items():
        value = getattr(cfg, field_name)
        print(f"{field_name}: {value}")
