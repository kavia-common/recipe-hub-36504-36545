import json
import os
import sys

# Ensure this script works when run from the container root or any working dir
# Compute the backend root as two levels up from this file: .../recipe_backend
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
# Add backend root to sys.path so "src.api.main" can be imported reliably
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from src.api.main import app  # noqa: E402

def main() -> None:
    """Generate and write the OpenAPI schema to interfaces/openapi.json."""
    # Generate OpenAPI schema from the FastAPI app
    openapi_schema = app.openapi()

    # Write to interfaces/openapi.json at the backend root
    output_dir = os.path.join(BACKEND_ROOT, "interfaces")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "openapi.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)

    print(f"OpenAPI schema written to {output_path}")

if __name__ == "__main__":
    main()
