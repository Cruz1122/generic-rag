import argparse
import sys
from importlib import metadata
from typing import Sequence

from generic_rag.cli.commands.doctor import doctor_handler
from generic_rag.cli.commands.demo import demo_handler
from generic_rag.cli.commands.inspect import inspect_handler
from generic_rag.cli.commands.provider import provider_handler

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="generic-rag",
        description="CLI for generic-rag: Agnostic RAG and LLM orchestration library",
    )
    
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Doctor command
    subparsers.add_parser("doctor", help="Check environment and dependencies")

    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run demos")
    demo_subparsers = demo_parser.add_subparsers(dest="demo_command", help="Demo types")
    demo_subparsers.add_parser("offline", help="Run a minimal offline demo")

    # Inspect command
    inspect_parser = subparsers.add_parser("inspect", help="Inspect files")
    inspect_subparsers = inspect_parser.add_subparsers(dest="inspect_command", help="Inspect types")
    file_inspect_parser = inspect_subparsers.add_parser("file", help="Inspect a specific file")
    file_inspect_parser.add_argument("path", help="Path to the file to inspect")

    # Provider command
    provider_parser = subparsers.add_parser("provider", help="Provider utilities")
    provider_subparsers = provider_parser.add_subparsers(dest="provider_command", help="Provider utilities")
    provider_subparsers.add_parser("check-env", help="Check environment variables for providers")

    args = parser.parse_args(argv)

    if args.version:
        pkg_version = metadata.version("generic-rag")
        print(f"generic-rag version: {pkg_version}")
        print(f"python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return 0

    if args.command == "doctor":
        return doctor_handler()
    elif args.command == "demo":
        if args.demo_command == "offline":
            return demo_handler(args)
        else:
            demo_parser.print_help()
            return 1
    elif args.command == "inspect":
        if args.inspect_command == "file":
            return inspect_handler(args)
        else:
            inspect_parser.print_help()
            return 1
    elif args.command == "provider":
        if args.provider_command == "check-env":
            return provider_handler()
        else:
            provider_parser.print_help()
            return 1

    parser.print_help()
    return 1

if __name__ == "__main__":
    sys.exit(main())
