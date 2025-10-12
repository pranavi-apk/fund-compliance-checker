#!/usr/bin/env python3
"""
Main CLI for the Investment Fund Compliance Checker.

This tool scans investment fund prospectuses against Hong Kong regulatory 
requirements (SFC Fund Manager Code of Conduct and MPF Code on Investment Funds)
and flags potential compliance violations.

Author: Built for Klares.io application
"""
import argparse
import os
import sys
from colorama import Fore, Style, init

from src.core import ComplianceChecker


init(autoreset=True)


def print_banner():
    """Print application banner."""
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("=" * 80)
    print("  Investment Fund Compliance Checker")
    print("  Hong Kong Regulatory Requirements (SFC & MPF)")
    print("=" * 80)
    print(f"{Style.RESET_ALL}")


def validate_files(files):
    """Validate that all required files exist."""
    missing = []
    for f in files:
        if not os.path.exists(f):
            missing.append(f)
    
    if missing:
        print(f"{Fore.RED}Error: The following files were not found:")
        for f in missing:
            print(f"  - {f}")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Check investment fund prospectuses for regulatory compliance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check a single prospectus
  python main.py --prospectus "20230504163240_1872.pdf"
  
  # Build knowledge base only (for faster subsequent runs)
  python main.py --build-kb-only
  
  # Check prospectus with custom output
  python main.py --prospectus "efund.pdf" --output report.txt
  
  # Use different LLM model
  python main.py --prospectus "efund.pdf" --model llama3.1

Regulatory Documents (auto-detected):
  - fund manager code of conduct.pdf
  - Code_on_MPF_Investment_Funds.pdf
        """
    )
    
    parser.add_argument(
        '--prospectus',
        type=str,
        help='Path to the prospectus PDF to check'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Path to save the compliance report (default: print to console)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='llama3.1:8b',
        help='Ollama model to use (default: llama3.1:8b)'
    )
    
    parser.add_argument(
        '--build-kb-only',
        action='store_true',
        help='Only build the knowledge base and exit (useful for setup)'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Rebuild knowledge base from scratch (ignore cache)'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Define regulatory documents (auto-detect in data/pdfs directory)
    regulatory_docs = [
        "data/pdfs/fund manager code of conduct.pdf",
        "data/pdfs/Code_on_MPF_Investment_Funds.pdf"
    ]
    
    # Validate regulatory documents exist
    if not validate_files(regulatory_docs):
        print(f"\n{Fore.YELLOW}Please ensure the regulatory PDFs are in the current directory:")
        print("  1. fund manager code of conduct.pdf")
        print("  2. Code_on_MPF_Investment_Funds.pdf")
        return 1
    
    # Initialize compliance checker
    print(f"{Fore.GREEN}Initializing Compliance Checker...")
    print(f"  LLM Model: {args.model}")
    print(f"  Embedding Model: all-MiniLM-L6-v2")
    
    try:
        checker = ComplianceChecker(
            regulatory_pdfs=regulatory_docs,
            llm_model=args.model
        )
    except Exception as e:
        print(f"{Fore.RED}Error initializing checker: {e}")
        print(f"\n{Fore.YELLOW}Make sure Ollama is running: ollama serve")
        print(f"And the model is available: ollama pull {args.model}")
        return 1
    
    # Build or load knowledge base
    cache_path = None if args.no_cache else "knowledge_base_cache.json"
    
    try:
        checker.build_knowledge_base(cache_path=cache_path)
    except Exception as e:
        print(f"{Fore.RED}Error building knowledge base: {e}")
        return 1
    
    # If only building KB, exit here
    if args.build_kb_only:
        print(f"\n{Fore.GREEN}✓ Knowledge base built successfully!")
        print(f"  Cache saved to: knowledge_base_cache.json")
        print(f"\nYou can now run compliance checks with:")
        print(f"  python main.py --prospectus <prospectus.pdf>")
        return 0
    
    # Check if prospectus specified
    if not args.prospectus:
        print(f"{Fore.YELLOW}\nNo prospectus specified. Use --prospectus <file.pdf>")
        print(f"\nAvailable test prospectuses:")
        test_docs = [
            "20230504163240_1872.pdf",
            "E-[Clean]ChinaAMCGlobalETFSeriesII-ConsolidatedProspectus-EN(Jun2025).pdf",
            "blackrock-premier-funds-active-and-feeder-prospectus-hk-en.pdf"
        ]
        for doc in test_docs:
            exists = "✓" if os.path.exists(doc) else "✗"
            print(f"  {exists} {doc}")
        return 1
    
    # Validate prospectus exists
    if not validate_files([args.prospectus]):
        return 1
    
    # Run compliance check
    try:
        violations = checker.check_prospectus(args.prospectus)
    except Exception as e:
        print(f"{Fore.RED}Error checking prospectus: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Generate report
    report = checker.generate_report(args.prospectus, violations)
    
    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"\n{Fore.GREEN}✓ Report saved to: {args.output}")
        
        # Also print summary to console
        print(f"\n{Fore.CYAN}Summary:")
        print(f"  Violations found: {len(violations)}")
        if violations:
            critical = sum(1 for v in violations if v.severity == 'CRITICAL')
            warning = sum(1 for v in violations if v.severity == 'WARNING')
            print(f"  Critical: {critical}")
            print(f"  Warnings: {warning}")
    else:
        # Print full report to console
        print("\n" + report)
    
    print(f"\n{Fore.GREEN}✓ Compliance check complete!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
