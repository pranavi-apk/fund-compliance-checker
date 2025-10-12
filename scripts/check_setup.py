#!/usr/bin/env python3
"""
Pre-flight check script to verify all dependencies and files are ready.
"""
import sys
import os


def check_python_version():
    """Check Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required (found {}.{}.{})".format(
            version.major, version.minor, version.micro))
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required = [
        'pdfplumber',
        'sentence_transformers',
        'numpy',
        'ollama',
        'colorama'
    ]
    
    missing = []
    for pkg in required:
        try:
            __import__(pkg.replace('-', '_'))
            print(f"✓ {pkg}")
        except ImportError:
            print(f"❌ {pkg} not installed")
            missing.append(pkg)
    
    if missing:
        print("\nTo install missing packages:")
        print("  pip install -r requirements.txt")
        return False
    
    return True


def check_ollama():
    """Check if Ollama is accessible"""
    try:
        import ollama
        models = ollama.list()
        print("✓ Ollama is running")
        
        # Check for llama3.2 or llama3.1
        model_names = [m.get('name', '') for m in models.get('models', [])]
        has_llama = any('llama3' in name for name in model_names)
        
        if has_llama:
            print("✓ llama3 model available")
        else:
            print("⚠️  llama3 model not found")
            print("   Run: ollama pull llama3.2 or ollama pull llama3.1")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Ollama not accessible: {e}")
        print("   1. Install from https://ollama.ai/")
        print("   2. Run: ollama serve")
        print("   3. Run: ollama pull llama3.2")
        return False


def check_pdfs():
    """Check if required PDF files exist"""
    regulatory = [
        "fund manager code of conduct.pdf",
        "Code_on_MPF_Investment_Funds.pdf"
    ]
    
    test_docs = [
        "20230504163240_1872.pdf",
        "E-[Clean]ChinaAMCGlobalETFSeriesII-ConsolidatedProspectus-EN(Jun2025).pdf",
        "blackrock-premier-funds-active-and-feeder-prospectus-hk-en.pdf"
    ]
    
    print("\nRegulatory Documents:")
    reg_ok = True
    for pdf in regulatory:
        if os.path.exists(pdf):
            size = os.path.getsize(pdf) / 1024
            print(f"✓ {pdf} ({size:.1f} KB)")
        else:
            print(f"❌ {pdf} NOT FOUND")
            reg_ok = False
    
    print("\nTest Prospectuses:")
    test_ok = False
    for pdf in test_docs:
        if os.path.exists(pdf):
            size = os.path.getsize(pdf) / 1024
            print(f"✓ {pdf} ({size:.1f} KB)")
            test_ok = True
        else:
            print(f"⚠️  {pdf} (optional)")
    
    if not reg_ok:
        print("\n❌ Missing required regulatory PDFs!")
        print("   Download from URLs in README.md")
        return False
    
    if not test_ok:
        print("\n⚠️  No test prospectuses found (optional for setup)")
    
    return True


def check_project_structure():
    """Check if all Python modules are present"""
    required_files = [
        'main.py',
        'compliance_checker.py',
        'pdf_parser.py',
        'vector_store.py',
        'llm_analyzer.py',
        'requirements.txt',
        'README.md'
    ]
    
    print("\nProject Files:")
    all_present = True
    for f in required_files:
        if os.path.exists(f):
            print(f"✓ {f}")
        else:
            print(f"❌ {f} NOT FOUND")
            all_present = False
    
    return all_present


def main():
    print("=" * 60)
    print("  Compliance Checker - Pre-flight Check")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Python Dependencies", check_dependencies),
        ("Ollama Service", check_ollama),
        ("PDF Documents", check_pdfs),
        ("Project Structure", check_project_structure)
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n📋 Checking: {name}")
        print("-" * 60)
        result = check_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    
    all_passed = all(r[1] for r in results)
    
    for name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to go.")
        print("\nNext steps:")
        print("  1. python main.py --build-kb-only")
        print("  2. python main.py --prospectus <your_file.pdf>")
        print("\nOr run the full demo:")
        print("  ./run_demo.sh")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
