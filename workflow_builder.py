#!/usr/bin/env python3
"""
Interactive Workflow Builder
-----------------------------
Creates an interactive interface for building video generation workflows
with checkbox selection and numbering/sequencing capabilities.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

import questionary
from questionary import Choice

from link_finder import LinkFinder


class WorkflowBuilder:
    """Interactive workflow builder for creating video generation sequences."""

    def __init__(self, base_url: str):
        """
        Initialize the WorkflowBuilder.

        Args:
            base_url: The base URL of the website
        """
        self.base_url = base_url
        self.workflow: List[Dict] = []
        self.link_finder = LinkFinder(base_url)

    def build_interactive(self) -> List[Dict]:
        """
        Build a workflow interactively using CLI prompts.

        Returns:
            List of workflow steps (dictionaries)
        """
        print("\n" + "=" * 70)
        print("🎬 INTERACTIVE WORKFLOW BUILDER")
        print("=" * 70 + "\n")

        # Step 1: Discovery method
        discovery_method = questionary.select(
            "How would you like to discover pages?",
            choices=[
                Choice("🗺️  Try sitemap.xml first (recommended)", value="sitemap"),
                Choice("🔍 Scrape from homepage", value="scrape"),
                Choice("✍️  Manual entry (enter URLs manually)", value="manual"),
            ],
        ).ask()

        if discovery_method in ["sitemap", "scrape"]:
            # Discover links
            print("\n🔎 Discovering links...")
            use_sitemap = discovery_method == "sitemap"
            categorized_links = self.link_finder.discover_all_links(use_sitemap=use_sitemap)

            if not categorized_links:
                print("\n⚠️  No links found! Falling back to manual entry.")
                return self._manual_entry()

            # Show summary
            total_links = sum(len(links) for links in categorized_links.values())
            print(f"\n✓ Found {total_links} links in {len(categorized_links)} categories\n")

            # Step 2: Category selection
            selected_links = self._select_from_categories(categorized_links)

            if not selected_links:
                print("\n⚠️  No links selected!")
                return []

        else:  # manual
            selected_links = self._manual_entry()

        # Step 3: Configure each selected link
        workflow = self._configure_workflow_steps(selected_links)

        # Step 4: Reorder if needed
        if len(workflow) > 1:
            reorder = questionary.confirm(
                "Would you like to reorder the sequence?", default=False
            ).ask()

            if reorder:
                workflow = self._reorder_workflow(workflow)

        # Step 5: Save workflow
        self._display_workflow_summary(workflow)

        save = questionary.confirm("Save this workflow to a file?", default=True).ask()
        if save:
            self._save_workflow(workflow)

        self.workflow = workflow
        return workflow

    def _select_from_categories(
        self, categorized_links: Dict[str, List[Dict[str, str]]]
    ) -> List[Dict[str, str]]:
        """
        Allow user to select links from discovered categories.

        Args:
            categorized_links: Dictionary of categorized links

        Returns:
            List of selected link dictionaries
        """
        selected_links = []

        # First, let user choose categories
        category_choices = [
            Choice(f"📁 {cat} ({len(links)} links)", value=cat)
            for cat, links in sorted(categorized_links.items())
        ]

        selected_categories = questionary.checkbox(
            "Select categories to include:",
            choices=category_choices,
        ).ask()

        if not selected_categories:
            return []

        # Then, for each category, let user select specific links
        for category in selected_categories:
            links = categorized_links[category]

            print(f"\n📁 Category: {category}")

            # Create choices with numbering
            link_choices = [
                Choice(
                    f"{i:3}. {link['text'][:50]}... - {link['url']}"
                    if len(link['text']) > 50
                    else f"{i:3}. {link['text']} - {link['url']}",
                    value=link,
                )
                for i, link in enumerate(links, 1)
            ]

            # Option to select all
            select_all = questionary.confirm(
                f"Select all {len(links)} links from '{category}'?", default=False
            ).ask()

            if select_all:
                selected_links.extend(links)
            else:
                selected = questionary.checkbox(
                    f"Select links from '{category}':",
                    choices=link_choices,
                ).ask()

                selected_links.extend(selected)

        return selected_links

    def _manual_entry(self) -> List[Dict[str, str]]:
        """
        Allow manual URL entry.

        Returns:
            List of manually entered link dictionaries
        """
        links = []
        print("\n✍️  Manual URL Entry")
        print("Enter URLs one by one (empty to finish)\n")

        while True:
            url = questionary.text(
                f"Enter URL #{len(links) + 1} (or press Enter to finish):"
            ).ask()

            if not url or url.strip() == "":
                break

            # Ask for a description
            text = questionary.text(
                "Enter description for this URL:", default=url
            ).ask()

            links.append({
                "url": url.strip(),
                "text": text or url,
                "category": "Manual",
            })

            print(f"✓ Added: {text}\n")

        return links

    def _configure_workflow_steps(
        self, selected_links: List[Dict[str, str]]
    ) -> List[Dict]:
        """
        Configure video generation parameters for each selected link.

        Args:
            selected_links: List of selected link dictionaries

        Returns:
            List of workflow step dictionaries
        """
        workflow = []

        print("\n" + "=" * 70)
        print("⚙️  CONFIGURE VIDEO SETTINGS")
        print("=" * 70 + "\n")

        # Ask for default settings
        use_defaults = questionary.confirm(
            "Use default settings for all videos? (duration: 15s, 1920x1080)",
            default=True,
        ).ask()

        if use_defaults:
            default_duration = 15
            default_width = 1920
            default_height = 1080
            default_logo = None
            default_text = None

            # Ask for optional overlays
            add_logo = questionary.confirm(
                "Add logo overlay to all videos?", default=False
            ).ask()

            if add_logo:
                default_logo = questionary.path(
                    "Path to logo file (PNG):"
                ).ask()

            add_text = questionary.confirm(
                "Add text overlay to all videos?", default=False
            ).ask()

            if add_text:
                use_auto_text = questionary.confirm(
                    "Use page title as text overlay?", default=True
                ).ask()

                if not use_auto_text:
                    default_text = questionary.text(
                        "Enter text overlay:"
                    ).ask()
        else:
            default_duration = None
            default_width = None
            default_height = None
            default_logo = None
            default_text = None

        # Configure each link
        for i, link in enumerate(selected_links, 1):
            print(f"\n{'─' * 70}")
            print(f"Video {i}/{len(selected_links)}: {link['text']}")
            print(f"URL: {link['url']}")
            print(f"{'─' * 70}")

            if use_defaults:
                duration = default_duration
                width = default_width
                height = default_height
                logo = default_logo
                text = default_text if default_text else link['text']
            else:
                duration = int(
                    questionary.text(
                        "Duration (seconds):", default="15"
                    ).ask()
                )

                width = int(
                    questionary.text(
                        "Width (pixels):", default="1920"
                    ).ask()
                )

                height = int(
                    questionary.text(
                        "Height (pixels):", default="1080"
                    ).ask()
                )

                add_logo = questionary.confirm(
                    "Add logo overlay?", default=False
                ).ask()
                logo = questionary.path("Path to logo file:").ask() if add_logo else None

                add_text = questionary.confirm(
                    "Add text overlay?", default=True
                ).ask()
                text = (
                    questionary.text("Text overlay:", default=link['text']).ask()
                    if add_text
                    else None
                )

            # Generate output filename
            safe_name = "".join(
                c if c.isalnum() or c in ("-", "_") else "_" for c in link['text']
            )[:50]
            output = f"{i:03d}_{safe_name}.mp4"

            step = {
                "number": i,
                "url": link["url"],
                "description": link["text"],
                "duration": duration,
                "width": width,
                "height": height,
                "output": output,
                "logo_path": logo,
                "text_overlay": text,
            }

            workflow.append(step)
            print(f"✓ Configured: {output}")

        return workflow

    def _reorder_workflow(self, workflow: List[Dict]) -> List[Dict]:
        """
        Allow user to reorder workflow steps.

        Args:
            workflow: List of workflow steps

        Returns:
            Reordered workflow
        """
        print("\n" + "=" * 70)
        print("🔢 REORDER WORKFLOW")
        print("=" * 70 + "\n")

        # Show current order
        print("Current order:")
        for step in workflow:
            print(f"  {step['number']:3}. {step['description']}")

        # Create choices
        choices = [
            Choice(
                f"{step['number']:3}. {step['description']}", value=step
            )
            for step in workflow
        ]

        # Let user select new order
        print("\nSelect items in the desired order:")
        reordered = questionary.checkbox(
            "Reorder (select in sequence):",
            choices=choices,
        ).ask()

        # Update numbers
        for i, step in enumerate(reordered, 1):
            step["number"] = i
            # Update output filename with new number
            old_output = step["output"]
            step["output"] = f"{i:03d}_{old_output[4:]}"

        return reordered

    def _display_workflow_summary(self, workflow: List[Dict]) -> None:
        """Display a summary of the workflow."""
        print("\n" + "=" * 70)
        print("📋 WORKFLOW SUMMARY")
        print("=" * 70 + "\n")

        for step in workflow:
            print(f"Step {step['number']:3}: {step['description']}")
            print(f"  URL:      {step['url']}")
            print(f"  Duration: {step['duration']}s")
            print(f"  Output:   {step['output']}")
            if step.get('logo_path'):
                print(f"  Logo:     {step['logo_path']}")
            if step.get('text_overlay'):
                print(f"  Text:     {step['text_overlay']}")
            print()

        print(f"Total videos: {len(workflow)}")
        total_duration = sum(step['duration'] for step in workflow)
        print(f"Total duration: {total_duration}s (~{total_duration // 60}m {total_duration % 60}s)")

    def _save_workflow(self, workflow: List[Dict]) -> None:
        """
        Save workflow to a JSON file.

        Args:
            workflow: List of workflow steps
        """
        # Create workflows directory if it doesn't exist
        workflows_dir = Path("workflows")
        workflows_dir.mkdir(exist_ok=True)

        # Ask for filename
        default_name = "workflow.json"
        filename = questionary.text(
            "Workflow filename:",
            default=default_name,
        ).ask()

        if not filename.endswith(".json"):
            filename += ".json"

        filepath = workflows_dir / filename

        # Save to JSON
        workflow_data = {
            "base_url": self.base_url,
            "steps": workflow,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(workflow_data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Workflow saved to: {filepath}")

    @staticmethod
    def load_workflow(filepath: str) -> Dict:
        """
        Load workflow from a JSON file.

        Args:
            filepath: Path to workflow JSON file

        Returns:
            Workflow dictionary
        """
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)


def main():
    """Interactive workflow builder main entry point."""
    print("\n🎬 Welcome to the Workflow Builder!")

    # Get base URL
    base_url = questionary.text(
        "Enter the base URL of the website:",
        default="https://example.com",
    ).ask()

    if not base_url:
        print("No URL provided. Exiting.")
        return

    # Build workflow
    builder = WorkflowBuilder(base_url)
    workflow = builder.build_interactive()

    if workflow:
        print(f"\n✓ Workflow created with {len(workflow)} steps!")
        print("\nTo execute this workflow, run:")
        print("  python workflow_runner.py workflows/<your-workflow>.json")
    else:
        print("\n⚠️  No workflow created.")


if __name__ == "__main__":
    main()
