"""
Quick verification script to check if the project is set up correctly
"""

def verify_imports():
    """Verify that all key imports work"""
    print("Verifying imports...")
    
    try:
        from config.config import Config
        print("✓ Config imported successfully")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    try:
        from src.utils.logger import setup_logger
        from src.utils.text_processing import TextProcessor
        print("✓ Utils imported successfully")
    except Exception as e:
        print(f"✗ Utils import failed: {e}")
        return False
    
    try:
        from src.knowledge_base import KnowledgeBase
        print("✓ KnowledgeBase imported successfully")
    except Exception as e:
        print(f"✗ KnowledgeBase import failed: {e}")
        return False
    
    try:
        from src.ticket_system import TicketRetriever
        print("✓ TicketRetriever imported successfully")
    except Exception as e:
        print(f"✗ TicketRetriever import failed: {e}")
        return False
    
    try:
        from src.agent import CustomerSupportAgent
        print("✓ CustomerSupportAgent imported successfully")
    except Exception as e:
        print(f"✗ CustomerSupportAgent import failed: {e}")
        return False
    
    return True


def verify_initialization():
    """Verify that key components can be initialized"""
    print("\nVerifying initialization...")
    
    try:
        from src.utils.logger import setup_logger
        logger = setup_logger("Test")
        print("✓ Logger initialized successfully")
    except Exception as e:
        print(f"✗ Logger initialization failed: {e}")
        return False
    
    try:
        from src.utils.text_processing import TextProcessor
        processor = TextProcessor()
        ticket_ref = processor.extract_ticket_reference("Check ticket PROJ-123")
        if ticket_ref == "PROJ-123":
            print("✓ TextProcessor works correctly")
        else:
            print(f"✗ TextProcessor test failed (got {ticket_ref})")
            return False
    except Exception as e:
        print(f"✗ TextProcessor test failed: {e}")
        return False
    
    try:
        from src.knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        print("✓ KnowledgeBase initialized successfully")
    except Exception as e:
        print(f"✗ KnowledgeBase initialization failed: {e}")
        return False
    
    try:
        from src.ticket_system import TicketRetriever
        tr = TicketRetriever()
        print("✓ TicketRetriever initialized successfully")
    except Exception as e:
        print(f"✗ TicketRetriever initialization failed: {e}")
        return False
    
    try:
        from src.agent import CustomerSupportAgent
        agent = CustomerSupportAgent()
        print("✓ CustomerSupportAgent initialized successfully")
    except Exception as e:
        print(f"✗ CustomerSupportAgent initialization failed: {e}")
        return False
    
    return True


def verify_file_structure():
    """Verify that required files and directories exist"""
    print("\nVerifying file structure...")
    
    import os
    from pathlib import Path
    
    required_dirs = [
        "src",
        "src/agent",
        "src/knowledge_base",
        "src/ticket_system",
        "src/utils",
        "config",
        "data",
        "data/knowledge_base"
    ]
    
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "config/config.py",
        "src/agent/customer_support_agent.py",
        "src/knowledge_base/knowledge_base.py",
        "src/ticket_system/ticket_retriever.py",
        "src/utils/logger.py",
        "src/utils/text_processing.py"
    ]
    
    all_good = True
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✓ Directory exists: {dir_path}")
        else:
            print(f"✗ Directory missing: {dir_path}")
            all_good = False
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ File exists: {file_path}")
        else:
            print(f"✗ File missing: {file_path}")
            all_good = False
    
    return all_good


if __name__ == "__main__":
    print("="*60)
    print("Customer Support Agent - Setup Verification")
    print("="*60)
    
    all_passed = True
    
    all_passed = verify_imports() and all_passed
    all_passed = verify_initialization() and all_passed
    all_passed = verify_file_structure() and all_passed
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ All checks passed! Setup is complete.")
        print("="*60)
        print("\nYou can now:")
        print("  1. Run 'python main.py' for interactive chat")
        print("  2. Run 'python main.py demo' for demo mode")
        print("  3. Run 'python example_usage.py' for usage examples")
    else:
        print("✗ Some checks failed. Please review the errors above.")
        print("="*60)

