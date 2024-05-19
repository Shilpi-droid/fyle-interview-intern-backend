import os
from waitress import serve
from core import app  # Adjust this import to match your application

# Default configuration
DEFAULT_PROC_NAME = 'fyle-interview-be'
DEFAULT_PORT = 7755
DEFAULT_HOST = '0.0.0.0'
DEFAULT_THREADS = 4
DEFAULT_BACKLOG = 50

# Get configuration from environment variables or use defaults
proc_name = os.environ.get('WAITRESS_PROC_NAME', DEFAULT_PROC_NAME)
port_number = int(os.environ.get('WAITRESS_PORT', DEFAULT_PORT))
host = os.environ.get('WAITRESS_HOST', DEFAULT_HOST)
threads = int(os.environ.get('WAITRESS_THREADS', DEFAULT_THREADS))
backlog = int(os.environ.get('WAITRESS_BACKLOG', DEFAULT_BACKLOG))

# Logging settings (basic example)
access_log = os.environ.get('WAITRESS_ACCESS_LOG', '-')
error_log = os.environ.get('WAITRESS_ERROR_LOG', '-')

# Function to start the server
def start_server():
    serve(
        app,
        host=host,
        port=port_number,
        threads=threads,
        backlog=backlog,
        expose_tracebacks=True
    )

if __name__ == "__main__":
    start_server()
