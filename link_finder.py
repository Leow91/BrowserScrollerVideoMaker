#!/usr/bin/env python3
"""
Link and Category Finder
-------------------------
Automatically discovers links and categories on a webpage,
including support for sitemap.xml parsing.
"""

import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class LinkFinder:
    """Finds and categorizes links on a website."""

    def __init__(self, base_url: str, max_depth: int = 1):
        """
        Initialize the LinkFinder.

        Args:
            base_url: The base URL of the website
            max_depth: Maximum depth for link discovery (default: 1)
        """
        self.base_url = base_url
        self.max_depth = max_depth
        self.parsed_base = urlparse(base_url)
        self.discovered_links: Set[str] = set()

    def is_same_domain(self, url: str) -> bool:
        """Check if URL belongs to the same domain."""
        parsed = urlparse(url)
        return parsed.netloc == self.parsed_base.netloc or parsed.netloc == ""

    def normalize_url(self, url: str) -> str:
        """Normalize and make URL absolute."""
        # Make absolute
        absolute_url = urljoin(self.base_url, url)

        # Remove fragment
        parsed = urlparse(absolute_url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

        # Remove trailing slash for consistency (except root)
        if normalized.endswith("/") and len(parsed.path) > 1:
            normalized = normalized[:-1]

        return normalized

    def find_links_from_page(self, url: str) -> List[Dict[str, str]]:
        """
        Find all links on a given page.

        Args:
            url: The URL to scrape

        Returns:
            List of dictionaries with 'url', 'text', and 'category' keys
        """
        links = []

        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Find all <a> tags
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                text = a_tag.get_text(strip=True) or "(No text)"

                # Skip anchors, javascript, mailto, etc.
                if href.startswith(("#", "javascript:", "mailto:", "tel:")):
                    continue

                # Normalize URL
                normalized_url = self.normalize_url(href)

                # Only include same-domain links
                if not self.is_same_domain(normalized_url):
                    continue

                # Skip duplicates
                if normalized_url in self.discovered_links:
                    continue

                self.discovered_links.add(normalized_url)

                # Try to detect category from parent elements or URL
                category = self._detect_category(a_tag, normalized_url)

                links.append({
                    "url": normalized_url,
                    "text": text,
                    "category": category,
                })

            print(f"Found {len(links)} unique links on {url}")

        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")

        return links

    def _detect_category(self, tag, url: str) -> str:
        """
        Attempt to detect the category of a link.

        Args:
            tag: BeautifulSoup tag object
            url: The normalized URL

        Returns:
            Category name (string)
        """
        # Check parent elements for nav, menu, category indicators
        parent = tag.parent
        for _ in range(3):  # Check up to 3 levels up
            if parent is None:
                break

            # Check class names
            if parent.has_attr("class"):
                classes = " ".join(parent["class"]).lower()
                if "nav" in classes:
                    return "Navigation"
                if "menu" in classes:
                    return "Menu"
                if "category" in classes or "categor" in classes:
                    return "Category"
                if "footer" in classes:
                    return "Footer"
                if "sidebar" in classes:
                    return "Sidebar"

            # Check tag names
            if parent.name in ["nav", "header"]:
                return "Navigation"
            if parent.name == "footer":
                return "Footer"
            if parent.name == "aside":
                return "Sidebar"

            parent = parent.parent

        # Fallback: analyze URL path
        path = urlparse(url).path.strip("/")
        if path:
            segments = path.split("/")
            if len(segments) > 0:
                first_segment = segments[0].replace("-", " ").replace("_", " ").title()
                return first_segment

        return "Other"

    def find_links_from_sitemap(self, sitemap_url: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Parse sitemap.xml to find URLs.

        Args:
            sitemap_url: URL to sitemap.xml (if None, tries default locations)

        Returns:
            List of dictionaries with 'url', 'text', and 'category' keys
        """
        links = []

        # Try common sitemap locations if not provided
        sitemap_urls = []
        if sitemap_url:
            sitemap_urls.append(sitemap_url)
        else:
            base = self.base_url.rstrip("/")
            sitemap_urls = [
                f"{base}/sitemap.xml",
                f"{base}/sitemap_index.xml",
                f"{base}/sitemap1.xml",
            ]

        for url in sitemap_urls:
            try:
                print(f"Trying sitemap: {url}")
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                # Parse XML
                root = ET.fromstring(response.content)

                # Handle namespaces
                namespaces = {
                    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
                    "": "http://www.sitemaps.org/schemas/sitemap/0.9",
                }

                # Find all <url> entries
                urls_found = root.findall(".//sm:url", namespaces) or root.findall(".//url")

                for url_entry in urls_found:
                    loc = url_entry.find("sm:loc", namespaces) or url_entry.find("loc")
                    if loc is not None and loc.text:
                        normalized_url = self.normalize_url(loc.text)

                        # Skip duplicates
                        if normalized_url in self.discovered_links:
                            continue

                        self.discovered_links.add(normalized_url)

                        # Derive text from URL
                        path = urlparse(normalized_url).path.strip("/")
                        text = path.replace("/", " > ").replace("-", " ").replace("_", " ").title() or "Home"

                        # Category from URL path
                        category = self._categorize_from_url(normalized_url)

                        links.append({
                            "url": normalized_url,
                            "text": text,
                            "category": category,
                        })

                print(f"Found {len(links)} URLs in sitemap")
                return links  # Return on first successful sitemap

            except requests.RequestException as e:
                print(f"Could not fetch sitemap from {url}: {e}")
                continue
            except ET.ParseError as e:
                print(f"Could not parse sitemap XML from {url}: {e}")
                continue

        if not links:
            print("No sitemap found or sitemap is empty")

        return links

    def _categorize_from_url(self, url: str) -> str:
        """Categorize URL based on path structure."""
        path = urlparse(url).path.strip("/")

        if not path:
            return "Home"

        segments = path.split("/")
        if len(segments) > 0:
            category = segments[0].replace("-", " ").replace("_", " ").title()
            return category

        return "Other"

    def discover_all_links(self, use_sitemap: bool = True) -> Dict[str, List[Dict[str, str]]]:
        """
        Discover all links using multiple methods.

        Args:
            use_sitemap: Whether to try sitemap.xml first

        Returns:
            Dictionary with categories as keys and lists of link dicts as values
        """
        all_links = []

        # Method 1: Try sitemap first
        if use_sitemap:
            print("Attempting to find links from sitemap.xml...")
            sitemap_links = self.find_links_from_sitemap()
            all_links.extend(sitemap_links)

        # Method 2: Scrape from homepage (if sitemap didn't work or as supplement)
        if not all_links or not use_sitemap:
            print(f"Scraping links from homepage: {self.base_url}")
            page_links = self.find_links_from_page(self.base_url)
            all_links.extend(page_links)

        # Group by category
        categorized: Dict[str, List[Dict[str, str]]] = {}
        for link in all_links:
            category = link["category"]
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(link)

        # Sort each category alphabetically
        for category in categorized:
            categorized[category].sort(key=lambda x: x["text"])

        return categorized


def main():
    """Test the LinkFinder."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python link_finder.py <url>")
        sys.exit(1)

    url = sys.argv[1]

    finder = LinkFinder(url)
    categorized_links = finder.discover_all_links()

    print("\n" + "=" * 60)
    print("DISCOVERED LINKS")
    print("=" * 60 + "\n")

    for category, links in sorted(categorized_links.items()):
        print(f"\n📁 {category} ({len(links)} links)")
        print("-" * 60)
        for i, link in enumerate(links, 1):
            print(f"{i:3}. {link['text']}")
            print(f"     {link['url']}")


if __name__ == "__main__":
    main()
