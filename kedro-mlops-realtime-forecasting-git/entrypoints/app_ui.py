import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from app_ui.app import app

if __name__ == "__main__":
    # Defaults to localhost-only so the dashboard isn't reachable by others
    # on the same network. Docker sets DASH_HOST=0.0.0.0 via docker-compose.yml
    # since that's required for port publishing to work from inside a container.
    host = os.environ.get("DASH_HOST", "127.0.0.1")
    port = int(os.environ.get("DASH_PORT", "8050"))
    app.run(debug=False, host=host, port=port)