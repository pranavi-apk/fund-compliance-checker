"""
Configuration settings for the Compliance Checker.
Modify these values to customize behavior.
"""

# LLM Configuration
LLM_MODEL = "llama3.2"  # Ollama model to use
LLM_TEMPERATURE = 0.1   # Lower = more focused, Higher = more creative

# Embedding Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Sentence transformer model
# Alternative models (uncomment to use):
# EMBEDDING_MODEL = "all-mpnet-base-v2"  # More accurate but slower
# EMBEDDING_MODEL = "multi-qa-MiniLM-L6-cos-v1"  # Optimized for Q&A

# PDF Parsing Configuration
CHUNK_SIZE = 1000       # Characters per chunk
CHUNK_OVERLAP = 200     # Overlap between chunks for context

# Search Configuration
TOP_K_REGULATORY = 3    # Number of regulatory chunks to retrieve
TOP_K_PROSPECTUS = 3    # Number of prospectus sections to analyze

# Cache Configuration
CACHE_ENABLED = True    # Use cached knowledge base if available
CACHE_FILE = "knowledge_base_cache.json"

# Regulatory Documents (auto-detected in current directory)
REGULATORY_PDFS = [
    "fund manager code of conduct.pdf",
    "Code_on_MPF_Investment_Funds.pdf"
]

# Compliance Checks Configuration
COMPLIANCE_CHECKS = [
    {
        'type': 'fee_disclosure',
        'query': 'management fees performance fees expenses charges fee structure calculation',
        'description': 'Fee Disclosure Completeness',
        'enabled': True
    },
    {
        'type': 'risk_disclosure',
        'query': 'risk factors market risk liquidity risk currency risk investment risks',
        'description': 'Risk Disclosure Requirements',
        'enabled': True
    },
    {
        'type': 'concentration_limits',
        'query': 'investment restrictions concentration limits single issuer exposure diversification',
        'description': 'Investment Concentration Limits',
        'enabled': True
    }
]

# Output Configuration
REPORT_FORMAT = "text"  # Options: text, json
COLORED_OUTPUT = True   # Use colored terminal output
VERBOSE = True          # Show progress messages

# Advanced Settings
BATCH_SIZE = 32         # Batch size for embedding generation
MAX_RETRIES = 3         # Retry attempts for LLM calls
TIMEOUT = 300           # Timeout for LLM calls (seconds)
