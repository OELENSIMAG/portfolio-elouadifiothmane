from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a portfolio HTML page from a JSON data file."
    )
    parser.add_argument(
        "--data",
        default="data.json",
        help="Path to the portfolio JSON data file.",
    )
    parser.add_argument(
        "--template",
        default="portfolio_template.html",
        help="Path to the Jinja2 HTML template.",
    )
    parser.add_argument(
        "--output",
        default="index.html",
        help="Path to the generated HTML file.",
    )
    return parser.parse_args()


def load_data(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    data.setdefault("site", {})
    data["site"].setdefault("title", "My Portfolio")
    data["site"].setdefault("description", "Personal portfolio")

    if "Programming Languages" in data and isinstance(data["Programming Languages"], list):
        data["programming_languages"] = data["Programming Languages"]
    else:
        data["programming_languages"] = []

    if "frameworks" not in data or not isinstance(data["frameworks"], list):
        data["frameworks"] = []

    if "skills" not in data or not isinstance(data["skills"], list):
        data["skills"] = []

    data["current_year"] = datetime.now().year
    return data


def render_html(data: dict, template_path: Path) -> str:
    environment = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = environment.get_template(template_path.name)
    return template.render(**data)


def main() -> None:
    args = parse_args()

    data_path = Path(args.data)
    template_path = Path(args.template)
    output_path = Path(args.output)

    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    data = load_data(data_path)
    html = render_html(data, template_path)

    output_path.write_text(html, encoding="utf-8")
    print(f"Portfolio generated: {output_path}")


if __name__ == "__main__":
    main()
