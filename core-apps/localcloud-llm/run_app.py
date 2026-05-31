import streamlit.web.cli as stcli
import os, sys

def resolve_path(path):
    """
    Constructs an absolute path from the current working directory.
    Essential for bundled applications (like PyInstaller) where relative paths break.
    """
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path

if __name__ == "__main__":
    # Programmatically inject CLI flags to simulate terminal execution
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("app.py"),             # Change to required filename
        "--global.developmentMode=false",   # Disables dev overhead/monitoring for production environments
    ]
    
    # Hand off execution control directly to Streamlit's main CLI entry point handler
    sys.exit(stcli.main())
