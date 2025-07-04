#!/usr/bin/env python3
"""
Simple test script to check basic TradingAgents setup.
This can be run without installing all dependencies.
"""

import sys
import os

def check_basic_structure():
    """Check if the basic repository structure exists."""
    print("📁 Checking repository structure:")
    
    required_files = [
        'README.md',
        'requirements.txt', 
        'setup.py',
        'main.py',
        'cli/main.py',
        'tradingagents/__init__.py',
        '.devcontainer/devcontainer.json',
        '.devcontainer/setup.sh',
        'CODESPACES.md',
        'validate_setup.py'
    ]
    
    success = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            success = False
    
    return success

def check_devcontainer_config():
    """Check if devcontainer configuration is valid."""
    print("\n🔧 Checking devcontainer configuration:")
    
    try:
        with open('.devcontainer/devcontainer.json', 'r') as f:
            content = f.read()
            if 'python' in content.lower():
                print("✅ Python environment configured")
            else:
                print("❌ Python environment not found in config")
                return False
                
            if 'postCreateCommand' in content:
                print("✅ Post-create command configured")
            else:
                print("❌ Post-create command not configured")
                return False
                
        return True
    except Exception as e:
        print(f"❌ Error reading devcontainer config: {e}")
        return False

def check_requirements():
    """Check if requirements.txt contains necessary packages."""
    print("\n📦 Checking requirements.txt:")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            required_packages = ['typer', 'rich', 'pandas', 'langchain', 'langgraph']
            
            for package in required_packages:
                if package in content:
                    print(f"✅ {package} found in requirements")
                else:
                    print(f"❌ {package} not found in requirements")
                    
        return True
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def check_setup_script():
    """Check if setup script exists and is executable."""
    print("\n🔧 Checking setup script:")
    
    setup_script = '.devcontainer/setup.sh'
    if os.path.exists(setup_script):
        print(f"✅ {setup_script} exists")
        
        # Check if it's executable
        if os.access(setup_script, os.X_OK):
            print("✅ Setup script is executable")
        else:
            print("⚠️  Setup script is not executable (will be fixed during setup)")
        
        return True
    else:
        print(f"❌ {setup_script} missing")
        return False

def main():
    """Main test function."""
    print("🧪 Testing TradingAgents GitHub Codespaces setup...\n")
    
    success = True
    
    # Check basic structure
    if not check_basic_structure():
        success = False
    
    # Check devcontainer config
    if not check_devcontainer_config():
        success = False
    
    # Check requirements
    if not check_requirements():
        success = False
    
    # Check setup script
    if not check_setup_script():
        success = False
    
    # Final status
    print("\n" + "="*50)
    if success:
        print("🎉 GitHub Codespaces setup test passed!")
        print("💡 Ready to launch in GitHub Codespaces:")
        print("   1. Go to your GitHub repository")
        print("   2. Click Code → Codespaces → Create codespace")
        print("   3. Wait for automatic setup to complete")
        print("   4. Set your API keys and run: python validate_setup.py")
    else:
        print("❌ Setup test failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)