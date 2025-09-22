#!/usr/bin/env python3
"""
Dependency Security Scanner
Scans project dependencies for known vulnerabilities
"""

import subprocess
import sys
import json

def run_safety_check():
    """Run safety check on requirements.txt"""
    try:
        result = subprocess.run([
            sys.executable, '-m', 'safety', 'check', 
            '--full-report', 
            '--file', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ No known vulnerabilities found in dependencies")
            return True
        else:
            print("⚠️  Security vulnerabilities detected:")
            print(result.stdout)
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("⚠️  Safety not installed. Install with: pip install safety")
        return None

def run_bandit_check():
    """Run bandit security linting on Python code"""
    try:
        result = subprocess.run([
            sys.executable, '-m', 'bandit', 
            '-r', 'nexus_server',
            '-f', 'json'
        ], capture_output=True, text=True)
        
        if result.returncode in [0, 1]:  # Bandit returns 1 if issues found
            try:
                output = json.loads(result.stdout)
                if output.get('results'):
                    print("⚠️  Security issues found in code:")
                    for issue in output['results']:
                        print(f"  - {issue['filename']}:{issue['line_range'][0]} - {issue['issue_text']}")
                    return False
                else:
                    print("✅ No security issues found in code")
                    return True
            except json.JSONDecodeError:
                print("⚠️  Bandit output format not as expected")
                print(result.stdout)
                return None
        else:
            print("⚠️  Bandit error:")
            print(result.stderr)
            return None
    except FileNotFoundError:
        print("⚠️  Bandit not installed. Install with: pip install bandit")
        return None

def main():
    """Main function to run all security checks"""
    print("🔒 Running Dependency Security Scanner...")
    print("=" * 50)
    
    # Run safety check
    print("\n1. Checking for vulnerable dependencies...")
    safety_result = run_safety_check()
    
    # Run bandit check
    print("\n2. Checking for security issues in code...")
    bandit_result = run_bandit_check()
    
    print("\n" + "=" * 50)
    if safety_result is False or bandit_result is False:
        print("❌ Security issues detected. Please address them before deployment.")
        sys.exit(1)
    elif safety_result is None or bandit_result is None:
        print("⚠️  Some security tools are not installed. Consider installing them for better security coverage.")
        sys.exit(0)
    else:
        print("✅ All security checks passed!")
        sys.exit(0)

if __name__ == '__main__':
    main()