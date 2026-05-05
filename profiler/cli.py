import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Energy Profiler CLI")

    subparsers = parser.add_subparsers(dest="command")

    # compare command
    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("file", help="Python file with functions")
    compare_parser.add_argument("--runs", type=int, default=3)
    compare_parser.add_argument("--tdp", type=float, default=28)

    args = parser.parse_args()

    if args.command == "compare":
        run_comparison(args)
    else:
        parser.print_help()


def run_comparison(args):
    from profiler.comparison import compare_multiple

    file_path = os.path.abspath(args.file)

    if not os.path.exists(file_path):
        print(f"Error: File not found -> {file_path}")
        return

    # Prevent running __main__ blocks
    namespace = {"__name__": "__not_main__"}

    # Snapshot BEFORE exec
    before_keys = set(namespace.keys())

    with open(file_path, "r") as f:
        code = f.read()

    exec(code, namespace)

    # Snapshot AFTER exec
    after_keys = set(namespace.keys())

    # Only new objects added by exec
    new_keys = after_keys - before_keys

    # Extract only user-defined functions
    functions = [
        namespace[name]
        for name in new_keys
        if callable(namespace[name])
        and hasattr(namespace[name], "__code__")
        and not name.startswith("_")
    ]

    if not functions:
        print("No valid functions found in file.")
        return

    # Run comparison
    results = compare_multiple(functions, runs=args.runs, tdp=args.tdp)

    print("\n=== Ranking ===\n")
    for i, r in enumerate(results, start=1):
        print(f"{i}. {r['name']} -> {r['energy']:.6f} J")


if __name__ == "__main__":
    main()