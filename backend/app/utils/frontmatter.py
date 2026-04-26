import yaml
import re
from typing import Tuple, Dict, Any

def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter and return (metadata, body)."""
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if match:
        try:
            metadata = yaml.safe_load(match.group(1)) or {}
            body = match.group(2)
            return metadata, body
        except yaml.YAMLError:
            pass
    return {}, content

def serialize_frontmatter(metadata: Dict[str, Any], body: str) -> str:
    """Serialize metadata into YAML frontmatter and append body."""
    if not metadata:
        return body
    fm = yaml.dump(metadata, default_flow_style=False, sort_keys=False).strip()
    return f"---\n{fm}\n---\n\n{body.strip()}\n"
