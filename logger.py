#!/usr/bin/env python3
"""
Logging Configuration
---------------------
Centralized logging setup with file rotation and structured output.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

from config import config


class Logger:
    """Centralized logger configuration."""

    _instance: Optional[logging.Logger] = None
    _console: Optional[Console] = None

    @classmethod
    def get_logger(cls, name: str = "scroll_video_gen") -> logging.Logger:
        """
        Get or create a logger instance.

        Args:
            name: Logger name

        Returns:
            Configured logger instance
        """
        if cls._instance is None:
            cls._instance = cls._setup_logger(name)

        return cls._instance

    @classmethod
    def _setup_logger(cls, name: str) -> logging.Logger:
        """
        Set up logger with file and console handlers.

        Args:
            name: Logger name

        Returns:
            Configured logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, config.log_level))

        # Remove existing handlers
        logger.handlers.clear()

        # Console handler with Rich formatting
        console_handler = RichHandler(
            console=cls._get_console(),
            show_time=True,
            show_path=False,
            markup=True,
            rich_tracebacks=True,
        )
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            "%(message)s",
            datefmt="[%X]"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File handler with rotation (if log file configured)
        if config.log_file:
            log_path = Path(config.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            # Parse rotation size (e.g., "10 MB")
            max_bytes = cls._parse_size(config.log_rotation)

            file_handler = RotatingFileHandler(
                filename=str(log_path),
                maxBytes=max_bytes,
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        return logger

    @classmethod
    def _get_console(cls) -> Console:
        """Get or create Rich console instance."""
        if cls._console is None:
            cls._console = Console()
        return cls._console

    @staticmethod
    def _parse_size(size_str: str) -> int:
        """
        Parse size string to bytes.

        Args:
            size_str: Size string (e.g., "10 MB", "500 KB")

        Returns:
            Size in bytes
        """
        size_str = size_str.strip().upper()

        units = {
            "B": 1,
            "KB": 1024,
            "MB": 1024 ** 2,
            "GB": 1024 ** 3,
        }

        for unit, multiplier in units.items():
            if unit in size_str:
                size = float(size_str.replace(unit, "").strip())
                return int(size * multiplier)

        # Default to bytes if no unit
        return int(size_str)


# Create global logger instance
logger = Logger.get_logger()


def log_exception(exc: Exception, context: str = ""):
    """
    Log an exception with context.

    Args:
        exc: Exception to log
        context: Additional context information
    """
    if context:
        logger.error(f"{context}: {type(exc).__name__}: {str(exc)}", exc_info=True)
    else:
        logger.error(f"{type(exc).__name__}: {str(exc)}", exc_info=True)


def log_video_generation_start(url: str, duration: int, output: str):
    """Log video generation start."""
    logger.info(f"[bold cyan]Starting video generation[/bold cyan]")
    logger.info(f"  URL: {url}")
    logger.info(f"  Duration: {duration}s")
    logger.info(f"  Output: {output}")


def log_video_generation_complete(output: str, elapsed_time: float):
    """Log video generation completion."""
    logger.info(f"[bold green]✓ Video generated successfully[/bold green]")
    logger.info(f"  Output: {output}")
    logger.info(f"  Time: {elapsed_time:.1f}s")


def log_workflow_start(workflow_name: str, total_steps: int):
    """Log workflow execution start."""
    logger.info(f"[bold cyan]Starting workflow: {workflow_name}[/bold cyan]")
    logger.info(f"  Total steps: {total_steps}")


def log_workflow_step(step_num: int, total: int, description: str):
    """Log workflow step."""
    logger.info(f"[bold]Step {step_num}/{total}:[/bold] {description}")


def log_workflow_complete(successful: int, failed: int, elapsed_time: float):
    """Log workflow completion."""
    logger.info(f"[bold green]✓ Workflow completed[/bold green]")
    logger.info(f"  Successful: {successful}")
    logger.info(f"  Failed: {failed}")
    logger.info(f"  Time: {elapsed_time:.1f}s")


# Example usage
if __name__ == "__main__":
    # Test logging
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    # Test structured logs
    log_video_generation_start("https://example.com", 15, "output.mp4")
    log_video_generation_complete("output.mp4", 45.3)

    log_workflow_start("my_workflow.json", 5)
    log_workflow_step(1, 5, "Homepage")
    log_workflow_complete(5, 0, 123.4)

    # Test exception logging
    try:
        raise ValueError("Test exception")
    except Exception as e:
        log_exception(e, "Test context")
