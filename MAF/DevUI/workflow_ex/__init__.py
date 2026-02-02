# Copyright (c) Microsoft. All rights reserved.

"""Agent Workflow - Content Review with Quality Routing."""

try:
    from .workflow import workflow
    __all__ = ["workflow"]
except ImportError as e:
    import warnings
    warnings.warn(f"Failed to import workflow: {e}")
    __all__ = []
