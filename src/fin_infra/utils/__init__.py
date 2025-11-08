"""Utilities namespace for fin-infra.

Networking timeouts/retries and related resource limits are provided by svc-infra
and should be consumed from there in services. This package intentionally keeps
no local HTTP/retry wrappers to avoid duplication.

Scaffold utilities for template-based code generation are provided in scaffold.py.
"""

from .scaffold import ensure_init_py, render_template, write

__all__ = [
    "render_template",
    "write",
    "ensure_init_py",
]
