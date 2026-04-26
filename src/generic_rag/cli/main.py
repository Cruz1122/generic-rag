import argparse
import sys
from importlib import metadata
from typing import Sequence

from generic_rag.cli.commands.doctor import doctor_handler
from generic_rag.cli.commands.demo import demo_handler
from generic_rag.cli.commands.inspect import inspect_handler
from generic_rag.cli.commands.provider import provider_handler
from generic_rag.cli.commands.eval import eval_retrieval_handler

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

    # Eval command
    eval_parser = subparsers.add_parser("eval", help="Evaluation utilities")
    eval_subparsers = eval_parser.add_subparsers(dest="eval_command", help="Evaluation types")
    retrieval_eval_parser = eval_subparsers.add_parser("retrieval", help="Evaluate retrieval performance")
    retrieval_eval_parser.add_argument("dataset", help="Path to evaluation dataset (JSON/JSONL)")
    retrieval_eval_parser.add_argument("predictions", help="Path to predictions file (JSON)")
    retrieval_eval_parser.add_argument("--k", default="1,3,5,10", help="Comma-separated list of k values for metrics")

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
    elif args.command == "eval":
        if args.eval_command == "retrieval":
            return eval_retrieval_handler(args)
        else:
            eval_parser.print_help()
            return 1

    parser.print_help()
    return 1

if __name__ == "__main__":
    sys.exit(main())
