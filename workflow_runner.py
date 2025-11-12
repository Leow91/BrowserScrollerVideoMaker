#!/usr/bin/env python3
"""
Workflow Runner
---------------
Executes saved video generation workflows.
"""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Dict, List

from scroll_video_generator import ScrollVideoGenerator


class WorkflowRunner:
    """Executes video generation workflows."""

    def __init__(self, workflow_file: str, output_dir: str = "output"):
        """
        Initialize the WorkflowRunner.

        Args:
            workflow_file: Path to workflow JSON file
            output_dir: Directory for output videos
        """
        self.workflow_file = workflow_file
        self.output_dir = Path(output_dir)
        self.workflow_data: Dict = {}
        self.steps: List[Dict] = []

    def load_workflow(self) -> None:
        """Load workflow from JSON file."""
        print(f"Loading workflow from: {self.workflow_file}")

        with open(self.workflow_file, "r", encoding="utf-8") as f:
            self.workflow_data = json.load(f)

        self.steps = self.workflow_data.get("steps", [])

        if not self.steps:
            print("Error: Workflow has no steps!")
            sys.exit(1)

        print(f"✓ Loaded workflow with {len(self.steps)} steps")
        print(f"  Base URL: {self.workflow_data.get('base_url', 'N/A')}\n")

    def prepare_output_directory(self) -> None:
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {self.output_dir.absolute()}\n")

    async def execute_workflow(self, start_from: int = 1, end_at: int = None) -> None:
        """
        Execute the workflow.

        Args:
            start_from: Step number to start from (1-indexed)
            end_at: Step number to end at (inclusive, None = all)
        """
        self.prepare_output_directory()

        # Filter steps based on range
        steps_to_execute = [
            step for step in self.steps
            if step["number"] >= start_from and (end_at is None or step["number"] <= end_at)
        ]

        if not steps_to_execute:
            print(f"No steps to execute in range {start_from}-{end_at or 'end'}")
            return

        total_steps = len(steps_to_execute)
        print("=" * 70)
        print(f"🎬 EXECUTING WORKFLOW ({total_steps} steps)")
        print("=" * 70 + "\n")

        start_time = time.time()
        successful = 0
        failed = 0

        for idx, step in enumerate(steps_to_execute, 1):
            step_number = step["number"]
            print(f"\n{'=' * 70}")
            print(f"Step {idx}/{total_steps} (#{step_number}): {step['description']}")
            print(f"{'=' * 70}\n")

            # Prepare output path
            output_path = self.output_dir / step["output"]

            # Create generator
            generator = ScrollVideoGenerator(
                url=step["url"],
                duration=step["duration"],
                output=str(output_path),
                logo_path=step.get("logo_path"),
                text_overlay=step.get("text_overlay"),
                viewport_width=step.get("width", 1920),
                viewport_height=step.get("height", 1080),
            )

            try:
                # Execute step
                await generator.generate()
                successful += 1
                print(f"\n✓ Step {step_number} completed successfully!")

            except Exception as e:
                failed += 1
                print(f"\n✗ Step {step_number} failed: {e}")

                # Ask if we should continue
                if idx < total_steps:
                    print("\nError occurred. Continue with next step? (Ctrl+C to abort)")
                    try:
                        # Give user 5 seconds to abort
                        await asyncio.sleep(5)
                        print("Continuing...")
                    except KeyboardInterrupt:
                        print("\n\nWorkflow aborted by user.")
                        break

        # Summary
        elapsed_time = time.time() - start_time
        print("\n" + "=" * 70)
        print("📊 WORKFLOW EXECUTION SUMMARY")
        print("=" * 70)
        print(f"Total steps:      {total_steps}")
        print(f"Successful:       {successful} ✓")
        print(f"Failed:           {failed} ✗")
        print(f"Execution time:   {elapsed_time:.1f}s (~{int(elapsed_time // 60)}m {int(elapsed_time % 60)}s)")
        print(f"Output directory: {self.output_dir.absolute()}")
        print("=" * 70 + "\n")

    def display_workflow_info(self) -> None:
        """Display workflow information without executing."""
        print("\n" + "=" * 70)
        print("📋 WORKFLOW INFORMATION")
        print("=" * 70 + "\n")

        print(f"File: {self.workflow_file}")
        print(f"Base URL: {self.workflow_data.get('base_url', 'N/A')}")
        print(f"Total steps: {len(self.steps)}\n")

        for step in self.steps:
            print(f"Step {step['number']:3}: {step['description']}")
            print(f"  URL:      {step['url']}")
            print(f"  Duration: {step['duration']}s")
            print(f"  Output:   {step['output']}")
            if step.get('logo_path'):
                print(f"  Logo:     {step['logo_path']}")
            if step.get('text_overlay'):
                print(f"  Text:     {step['text_overlay'][:50]}{'...' if len(step.get('text_overlay', '')) > 50 else ''}")
            print()

        total_duration = sum(step['duration'] for step in self.steps)
        print(f"Estimated total scroll time: {total_duration}s (~{total_duration // 60}m {total_duration % 60}s)")
        print("(Note: Actual execution time will be longer due to page loading, processing, etc.)")


def main():
    """Main entry point for workflow runner."""
    parser = argparse.ArgumentParser(
        description="Execute video generation workflows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute entire workflow
  python workflow_runner.py workflows/my_workflow.json

  # Execute specific range
  python workflow_runner.py workflows/my_workflow.json --start 3 --end 5

  # Display workflow info without executing
  python workflow_runner.py workflows/my_workflow.json --info

  # Custom output directory
  python workflow_runner.py workflows/my_workflow.json --output-dir my_videos
        """,
    )

    parser.add_argument(
        "workflow_file",
        type=str,
        help="Path to workflow JSON file",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Output directory for videos (default: output)",
    )

    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Start from step number (default: 1)",
    )

    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="End at step number (default: all)",
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Display workflow info without executing",
    )

    args = parser.parse_args()

    # Check if workflow file exists
    if not Path(args.workflow_file).exists():
        print(f"Error: Workflow file not found: {args.workflow_file}")
        sys.exit(1)

    # Create runner
    runner = WorkflowRunner(args.workflow_file, args.output_dir)
    runner.load_workflow()

    # Info mode or execute mode
    if args.info:
        runner.display_workflow_info()
    else:
        asyncio.run(runner.execute_workflow(args.start, args.end))


if __name__ == "__main__":
    main()
