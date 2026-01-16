"""CLI demonstration of radical-algebra.

Run with: uv run python -m radical_algebra [--rank N] [--radicals CHARS]
"""

import argparse
import sys

from radical_algebra import WU_XING, RadicalSet, outer_product


def print_matrix(matrix, radicals: list[str]) -> None:
    """Print rank-2 tensor as a matrix."""
    n = len(radicals)

    # Header
    print(f"\n{'':4}", end="")
    for r in radicals:
        print(f"{r:8}", end="")
    print()
    print("    " + "-" * (8 * n))

    # Rows
    for i, r1 in enumerate(radicals):
        print(f"{r1:3}|", end="")
        for j in range(n):
            chars = matrix[i, j]
            if chars:
                display = ",".join(sorted(chars)[:2])
                if len(chars) > 2:
                    display = display[:6] + ".."
            else:
                display = "--"
            print(f"{display:8}", end="")
        print()


def print_tensor_diagonal(tensor, radicals: list[str], rank: int) -> None:
    """Print the super-diagonal of a higher-rank tensor."""
    print(f"\nRank-{rank} diagonal (same radical repeated {rank} times):")
    print("-" * 50)

    for i, r in enumerate(radicals):
        idx = tuple([i] * rank)
        chars = tensor[idx]
        if chars:
            char_list = ", ".join(sorted(chars))
            print(f"  {r} x {rank} = {char_list}")
        else:
            print(f"  {r} x {rank} = (no character found)")


def main() -> int:
    """Main entry point for CLI demonstration."""
    parser = argparse.ArgumentParser(
        description="Tensor algebra on Chinese radicals",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      # Wu Xing (Five Elements) rank-2
  %(prog)s --rank 3             # Wu Xing rank-3 (triple compositions)
  %(prog)s --radicals 日月      # Custom radicals (sun, moon)
  %(prog)s --radicals 口女人    # Custom radicals (mouth, woman, person)
""",
    )
    parser.add_argument(
        "--rank",
        type=int,
        default=2,
        choices=[2, 3, 4, 5, 6, 7, 8],
        help="Tensor rank (default: 2)",
    )
    parser.add_argument(
        "--radicals",
        type=str,
        default=None,
        help="Custom radicals as a string (default: Wu Xing 金木水火土)",
    )
    args = parser.parse_args()

    # Build radical set
    if args.radicals:
        radicals = list(args.radicals)
        try:
            radical_set = RadicalSet("custom", radicals)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        print(f"Radicals: {' '.join(radicals)} (custom)")
    else:
        radical_set = WU_XING
        radicals = list(WU_XING)
        print(f"Radicals: {' '.join(radicals)} (Wu Xing / Five Elements)")

    print(f"Rank: {args.rank}")

    # Compute tensor
    result = outer_product(radical_set, rank=args.rank)

    # Display results
    if args.rank == 2:
        print_matrix(result, radicals)
    else:
        print_tensor_diagonal(result, radicals, args.rank)

    # Show some notable results
    print("\nNotable characters:")
    print("-" * 50)

    if args.rank == 2:
        for i, r in enumerate(radicals):
            chars = result[i, i]
            if chars:
                print(f"  {r}+{r} = {', '.join(sorted(chars)[:3])}")
    else:
        count = 0
        for i, r in enumerate(radicals):
            idx = tuple([i] * args.rank)
            chars = result[idx]
            if chars:
                print(f"  {r}x{args.rank} = {', '.join(sorted(chars))}")
                count += 1
        if count == 0:
            print("  (no diagonal characters found at this rank)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
