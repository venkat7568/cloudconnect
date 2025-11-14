"""
CloudConnect - Main Entry Point

Run this file to start the application:
    python main.py
"""

from src.app import CloudConnectApp


def main():
    """Main entry point"""
    app = CloudConnectApp()
    app.run()


if __name__ == '__main__':
    main()