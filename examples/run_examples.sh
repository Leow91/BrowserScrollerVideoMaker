#!/bin/bash
# Example scripts for using the Scroll Video Generator

echo "=== Automated Web Scroll Video Creator - Examples ==="
echo ""

# Example 1: Simple scroll video
echo "Example 1: Simple scroll video of Example.com"
python ../scroll_video_generator.py \
    --url https://example.com \
    --duration 10 \
    --output example1_simple.mp4

echo ""
echo "---"
echo ""

# Example 2: Longer scroll with custom dimensions
echo "Example 2: Scroll video with HD resolution"
python ../scroll_video_generator.py \
    --url https://news.ycombinator.com \
    --duration 20 \
    --output example2_hackernews.mp4 \
    --width 1280 \
    --height 720

echo ""
echo "---"
echo ""

# Example 3: With text overlay
echo "Example 3: Scroll video with text overlay"
python ../scroll_video_generator.py \
    --url https://github.com \
    --duration 15 \
    --output example3_with_text.mp4 \
    --text_overlay "GitHub Homepage Tour"

echo ""
echo "---"
echo ""

echo "All examples completed!"
echo "Videos saved in the examples/ directory"
