#!/usr/bin/env python3
"""
Web GUI for Scroll Video Generator
-----------------------------------
Modern web interface built with Gradio for easy video generation.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Optional, Tuple

import gradio as gr

from config import config
from link_finder import LinkFinder
from scroll_video_generator import ScrollVideoGenerator
from workflow_runner import WorkflowRunner


class WebGUI:
    """Web-based GUI for the Scroll Video Generator."""

    def __init__(self):
        """Initialize the Web GUI."""
        self.config = config
        self.current_workflow = None

    def generate_single_video(
        self,
        url: str,
        duration: int,
        width: int,
        height: int,
        logo: Optional[gr.File],
        text_overlay: Optional[str],
        progress=gr.Progress()
    ) -> Tuple[str, Optional[str]]:
        """
        Generate a single scroll video.

        Args:
            url: URL to scroll
            duration: Duration in seconds
            width: Viewport width
            height: Viewport height
            logo: Logo file
            text_overlay: Text overlay
            progress: Gradio progress tracker

        Returns:
            Tuple of (status_message, video_path)
        """
        try:
            progress(0, desc="Validating inputs...")

            # Validate URL
            if not url or not url.startswith(("http://", "https://")):
                return "❌ Error: Invalid URL. Must start with http:// or https://", None

            # Generate output filename
            from urllib.parse import urlparse
            domain = urlparse(url).netloc.replace(".", "_")
            output_filename = f"{domain}_{duration}s.mp4"
            output_path = self.config.get_output_video_path(output_filename)

            # Get logo path if provided
            logo_path = logo.name if logo else None

            progress(0.1, desc="Initializing video generator...")

            # Create generator
            generator = ScrollVideoGenerator(
                url=url,
                duration=duration,
                output=str(output_path),
                logo_path=logo_path,
                text_overlay=text_overlay,
                viewport_width=width,
                viewport_height=height,
            )

            progress(0.2, desc="Recording scroll video...")

            # Run async generator
            asyncio.run(generator.generate())

            progress(1.0, desc="Complete!")

            return f"✅ Video generated successfully: {output_path.name}", str(output_path)

        except Exception as e:
            return f"❌ Error: {str(e)}", None

    def discover_links(
        self,
        url: str,
        use_sitemap: bool,
        progress=gr.Progress()
    ) -> Tuple[str, str]:
        """
        Discover links on a website.

        Args:
            url: Base URL
            use_sitemap: Whether to use sitemap.xml
            progress: Gradio progress tracker

        Returns:
            Tuple of (status_message, links_json)
        """
        try:
            progress(0, desc="Initializing link finder...")

            if not url or not url.startswith(("http://", "https://")):
                return "❌ Error: Invalid URL", "[]"

            progress(0.2, desc="Discovering links...")

            finder = LinkFinder(url)
            categorized_links = finder.discover_all_links(use_sitemap=use_sitemap)

            progress(0.8, desc="Organizing results...")

            # Convert to JSON for display
            links_data = []
            for category, links in categorized_links.items():
                for link in links:
                    links_data.append({
                        "category": category,
                        "text": link["text"],
                        "url": link["url"]
                    })

            total_links = len(links_data)
            total_categories = len(categorized_links)

            progress(1.0, desc="Complete!")

            status = f"✅ Found {total_links} links in {total_categories} categories"
            return status, json.dumps(links_data, indent=2)

        except Exception as e:
            return f"❌ Error: {str(e)}", "[]"

    def create_workflow_from_links(
        self,
        links_json: str,
        selected_indices: str,
        base_url: str,
        default_duration: int,
        default_width: int,
        default_height: int,
        logo: Optional[gr.File],
        use_auto_text: bool,
        workflow_name: str,
        progress=gr.Progress()
    ) -> str:
        """
        Create a workflow from selected links.

        Args:
            links_json: JSON string of discovered links
            selected_indices: Comma-separated indices of selected links
            base_url: Base URL
            default_duration: Default duration for videos
            default_width: Default width
            default_height: Default height
            logo: Logo file
            use_auto_text: Use auto text overlay
            workflow_name: Workflow filename
            progress: Progress tracker

        Returns:
            Status message
        """
        try:
            progress(0, desc="Parsing links...")

            # Parse links
            all_links = json.loads(links_json)

            if not all_links:
                return "❌ No links available. Please discover links first."

            # Parse selected indices
            if not selected_indices or selected_indices.strip() == "":
                return "❌ No links selected. Please enter indices (e.g., 0,1,2)"

            try:
                indices = [int(i.strip()) for i in selected_indices.split(",")]
            except ValueError:
                return "❌ Invalid indices format. Use comma-separated numbers (e.g., 0,1,2)"

            # Select links
            selected_links = []
            for idx in indices:
                if 0 <= idx < len(all_links):
                    selected_links.append(all_links[idx])

            if not selected_links:
                return "❌ No valid links selected"

            progress(0.3, desc=f"Creating workflow with {len(selected_links)} links...")

            # Create workflow
            workflow_steps = []
            logo_path = logo.name if logo else None

            for i, link in enumerate(selected_links, 1):
                step = {
                    "number": i,
                    "url": link["url"],
                    "description": link["text"],
                    "duration": default_duration,
                    "width": default_width,
                    "height": default_height,
                    "output": f"{i:03d}_{self._sanitize_filename(link['text'])}.mp4",
                    "logo_path": logo_path,
                    "text_overlay": link["text"] if use_auto_text else None,
                }
                workflow_steps.append(step)

            # Save workflow
            workflow_data = {
                "base_url": base_url,
                "steps": workflow_steps,
            }

            if not workflow_name.endswith(".json"):
                workflow_name += ".json"

            workflow_path = self.config.workflow_dir / workflow_name

            progress(0.8, desc="Saving workflow...")

            with open(workflow_path, "w", encoding="utf-8") as f:
                json.dump(workflow_data, f, indent=2, ensure_ascii=False)

            progress(1.0, desc="Complete!")

            return f"✅ Workflow created: {workflow_path}\nSteps: {len(workflow_steps)}"

        except Exception as e:
            return f"❌ Error: {str(e)}"

    def execute_workflow(
        self,
        workflow_file: gr.File,
        start_step: int,
        end_step: int,
        progress=gr.Progress()
    ) -> Tuple[str, str]:
        """
        Execute a workflow.

        Args:
            workflow_file: Workflow JSON file
            start_step: Start from step
            end_step: End at step (0 = all)
            progress: Progress tracker

        Returns:
            Tuple of (status_message, output_directory)
        """
        try:
            if not workflow_file:
                return "❌ Please upload a workflow file", ""

            progress(0, desc="Loading workflow...")

            # Load workflow
            with open(workflow_file.name, "r", encoding="utf-8") as f:
                workflow_data = json.load(f)

            steps = workflow_data.get("steps", [])
            if not steps:
                return "❌ Workflow has no steps", ""

            # Determine range
            end_at = end_step if end_step > 0 else None

            progress(0.1, desc=f"Executing {len(steps)} steps...")

            # Create runner
            runner = WorkflowRunner(workflow_file.name, str(self.config.output_dir))
            runner.load_workflow()

            # Execute
            asyncio.run(runner.execute_workflow(start_step, end_at))

            progress(1.0, desc="Complete!")

            return f"✅ Workflow executed successfully!\nOutput: {self.config.output_dir}", str(self.config.output_dir)

        except Exception as e:
            return f"❌ Error: {str(e)}", ""

    def list_workflows(self) -> str:
        """List available workflows."""
        workflows = list(self.config.workflow_dir.glob("*.json"))

        if not workflows:
            return "No workflows found in: " + str(self.config.workflow_dir)

        result = f"Available Workflows ({len(workflows)}):\n\n"
        for wf in sorted(workflows):
            try:
                with open(wf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    steps = len(data.get("steps", []))
                    base_url = data.get("base_url", "N/A")
                result += f"📁 {wf.name}\n"
                result += f"   Steps: {steps}\n"
                result += f"   URL: {base_url}\n\n"
            except Exception:
                result += f"📁 {wf.name} (corrupted)\n\n"

        return result

    def list_videos(self) -> str:
        """List generated videos."""
        videos = list(self.config.output_dir.glob("*.mp4"))

        if not videos:
            return "No videos found in: " + str(self.config.output_dir)

        result = f"Generated Videos ({len(videos)}):\n\n"
        for video in sorted(videos, key=lambda x: x.stat().st_mtime, reverse=True):
            size_mb = video.stat().st_size / (1024 * 1024)
            result += f"🎬 {video.name}\n"
            result += f"   Size: {size_mb:.2f} MB\n\n"

        return result

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Sanitize filename."""
        return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name)[:50]

    def build_interface(self) -> gr.Blocks:
        """
        Build the Gradio interface.

        Returns:
            Gradio Blocks interface
        """
        with gr.Blocks(
            title="Scroll Video Generator",
            theme=gr.themes.Soft(),
            css=".gradio-container {max-width: 1200px !important}"
        ) as interface:

            gr.Markdown(
                """
                # 🎬 Automated Web Scroll Video Generator

                Create professional scroll-through videos of websites with automatic link discovery,
                workflow management, and batch processing.
                """
            )

            with gr.Tabs():
                # Tab 1: Single Video
                with gr.Tab("📹 Single Video"):
                    gr.Markdown("### Generate a single scroll video from any URL")

                    with gr.Row():
                        with gr.Column():
                            single_url = gr.Textbox(
                                label="Website URL",
                                placeholder="https://example.com",
                                value="https://example.com"
                            )
                            single_duration = gr.Slider(
                                minimum=5,
                                maximum=120,
                                value=15,
                                step=1,
                                label="Duration (seconds)"
                            )

                            with gr.Row():
                                single_width = gr.Number(label="Width", value=1920)
                                single_height = gr.Number(label="Height", value=1080)

                            single_logo = gr.File(label="Logo (optional, PNG)", file_types=[".png"])
                            single_text = gr.Textbox(label="Text Overlay (optional)", placeholder="My Website Tour")

                            single_btn = gr.Button("🎬 Generate Video", variant="primary", size="lg")

                        with gr.Column():
                            single_status = gr.Textbox(label="Status", lines=3)
                            single_video = gr.Video(label="Generated Video")

                    single_btn.click(
                        fn=self.generate_single_video,
                        inputs=[single_url, single_duration, single_width, single_height, single_logo, single_text],
                        outputs=[single_status, single_video]
                    )

                # Tab 2: Link Discovery
                with gr.Tab("🔍 Link Discovery"):
                    gr.Markdown("### Automatically discover links on a website")

                    with gr.Row():
                        with gr.Column():
                            discover_url = gr.Textbox(
                                label="Website URL",
                                placeholder="https://example.com",
                                value="https://example.com"
                            )
                            discover_sitemap = gr.Checkbox(
                                label="Try sitemap.xml first (recommended)",
                                value=True
                            )
                            discover_btn = gr.Button("🔎 Discover Links", variant="primary", size="lg")

                        with gr.Column():
                            discover_status = gr.Textbox(label="Status", lines=2)
                            discover_results = gr.Code(label="Discovered Links (JSON)", language="json", lines=20)

                    discover_btn.click(
                        fn=self.discover_links,
                        inputs=[discover_url, discover_sitemap],
                        outputs=[discover_status, discover_results]
                    )

                # Tab 3: Workflow Builder
                with gr.Tab("⚙️ Workflow Builder"):
                    gr.Markdown("### Create video workflows from discovered links")

                    with gr.Row():
                        with gr.Column():
                            wf_links_json = gr.Code(
                                label="Discovered Links (paste from Link Discovery tab)",
                                language="json",
                                lines=10
                            )
                            wf_selected = gr.Textbox(
                                label="Select Links (comma-separated indices, e.g., 0,1,2,5)",
                                placeholder="0,1,2"
                            )
                            wf_base_url = gr.Textbox(
                                label="Base URL",
                                placeholder="https://example.com"
                            )

                            with gr.Row():
                                wf_duration = gr.Number(label="Default Duration (s)", value=15)
                                wf_width = gr.Number(label="Width", value=1920)
                                wf_height = gr.Number(label="Height", value=1080)

                            wf_logo = gr.File(label="Logo (optional)", file_types=[".png"])
                            wf_auto_text = gr.Checkbox(label="Use page titles as text overlay", value=True)
                            wf_name = gr.Textbox(
                                label="Workflow Name",
                                placeholder="my_workflow.json",
                                value="my_workflow.json"
                            )

                            wf_create_btn = gr.Button("💾 Create Workflow", variant="primary", size="lg")

                        with gr.Column():
                            wf_status = gr.Textbox(label="Status", lines=10)

                    wf_create_btn.click(
                        fn=self.create_workflow_from_links,
                        inputs=[
                            wf_links_json, wf_selected, wf_base_url,
                            wf_duration, wf_width, wf_height,
                            wf_logo, wf_auto_text, wf_name
                        ],
                        outputs=[wf_status]
                    )

                # Tab 4: Workflow Runner
                with gr.Tab("▶️ Workflow Runner"):
                    gr.Markdown("### Execute saved workflows")

                    with gr.Row():
                        with gr.Column():
                            runner_file = gr.File(label="Upload Workflow File", file_types=[".json"])

                            with gr.Row():
                                runner_start = gr.Number(label="Start from Step", value=1, minimum=1)
                                runner_end = gr.Number(label="End at Step (0 = all)", value=0, minimum=0)

                            runner_btn = gr.Button("▶️ Execute Workflow", variant="primary", size="lg")

                        with gr.Column():
                            runner_status = gr.Textbox(label="Status", lines=5)
                            runner_output = gr.Textbox(label="Output Directory", lines=2)

                    runner_btn.click(
                        fn=self.execute_workflow,
                        inputs=[runner_file, runner_start, runner_end],
                        outputs=[runner_status, runner_output]
                    )

                # Tab 5: Library
                with gr.Tab("📚 Library"):
                    gr.Markdown("### Browse workflows and generated videos")

                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("#### Workflows")
                            list_wf_btn = gr.Button("🔄 Refresh Workflows")
                            wf_list = gr.Textbox(label="Available Workflows", lines=15)

                        with gr.Column():
                            gr.Markdown("#### Videos")
                            list_vid_btn = gr.Button("🔄 Refresh Videos")
                            vid_list = gr.Textbox(label="Generated Videos", lines=15)

                    list_wf_btn.click(fn=self.list_workflows, outputs=[wf_list])
                    list_vid_btn.click(fn=self.list_videos, outputs=[vid_list])

                # Tab 6: Settings
                with gr.Tab("⚙️ Settings"):
                    gr.Markdown("### Application Configuration")

                    with gr.Row():
                        with gr.Column():
                            gr.Markdown(f"""
                            **Current Configuration:**

                            - **Workflow Directory:** `{self.config.workflow_dir}`
                            - **Output Directory:** `{self.config.output_dir}`
                            - **Temp Directory:** `{self.config.temp_dir}`
                            - **Max Concurrent Jobs:** {self.config.max_concurrent_jobs}
                            - **Default Duration:** {self.config.default_duration}s
                            - **Default Resolution:** {self.config.default_width}x{self.config.default_height}
                            - **FFmpeg CRF:** {self.config.ffmpeg_crf}
                            - **FFmpeg Preset:** {self.config.ffmpeg_preset}
                            - **Browser Headless:** {self.config.browser_headless}

                            To modify settings, edit the `.env` file or use environment variables.
                            """)

            gr.Markdown(
                """
                ---
                **Version:** 1.1.0 | **License:** MIT | [Documentation](https://github.com/yourusername/BrowserScrollerVideoMaker)
                """
            )

        return interface

    def launch(self, share: bool = False, **kwargs):
        """
        Launch the Gradio interface.

        Args:
            share: Create public share link
            **kwargs: Additional Gradio launch arguments
        """
        interface = self.build_interface()

        print("\n" + "=" * 60)
        print("🎬 Scroll Video Generator - Web GUI")
        print("=" * 60)
        print(f"Starting server on http://{self.config.gui_host}:{self.config.gui_port}")
        print("Press Ctrl+C to stop")
        print("=" * 60 + "\n")

        interface.launch(
            server_name=self.config.gui_host,
            server_port=self.config.gui_port,
            share=share or self.config.gui_share,
            **kwargs
        )


def main():
    """Main entry point for the Web GUI."""
    gui = WebGUI()
    gui.launch()


if __name__ == "__main__":
    main()
