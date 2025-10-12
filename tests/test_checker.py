"""
Simple test script to verify the compliance checker works
"""
import os
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import ComplianceChecker

def test_compliance_checker():
    print("🔧 Testing Compliance Checker...")
    
    # Check files exist
    regulatory_docs = [
        "data/pdfs/fund manager code of conduct.pdf",
        "data/pdfs/Code_on_MPF_Investment_Funds.pdf"
    ]
    
    test_prospectus = "data/pdfs/20230504163240_1872.pdf"
    
    print("📁 Checking files...")
    for doc in regulatory_docs:
        if os.path.exists(doc):
            print(f"  ✓ {doc}")
        else:
            print(f"  ❌ {doc} NOT FOUND")
            return
    
    if os.path.exists(test_prospectus):
        print(f"  ✓ {test_prospectus}")
    else:
        print(f"  ❌ {test_prospectus} NOT FOUND")
        return
    
    try:
        print("\n🤖 Initializing checker...")
        checker = ComplianceChecker(
            regulatory_pdfs=regulatory_docs,
            llm_model='llama3.1:8b'
        )
        
        print("📚 Building knowledge base...")
        checker.build_knowledge_base(cache_path="knowledge_base_cache.json")
        
        print("📄 Analyzing prospectus (this will take a while)...")
        violations = checker.check_prospectus(test_prospectus)
        
        print(f"\n✅ Analysis complete!")
        print(f"📊 Found {len(violations)} violations")
        
        for i, v in enumerate(violations, 1):
            print(f"  {i}. [{v.severity}] {v.check_type} - Page {v.location_page}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_compliance_checker()