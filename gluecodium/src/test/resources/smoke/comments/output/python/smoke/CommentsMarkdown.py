

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class CommentsMarkdown(_NativeBase):
    """First line.
Second line.

Another paragraph. **bold** and *italic* and `code`.

> blockquote

# Heading one

## Heading two

### Heading three

Unordered list:
- A
- B

Ordered list:
1. foo
2. bar

---

[title](https://www.markdownguide.org/cheat-sheet/)"""

    def __init__(self, native):
        super().__init__(native)

