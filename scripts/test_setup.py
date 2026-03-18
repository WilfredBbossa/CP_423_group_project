"""
Test script to verify all components are installed correctly
Run this first to ensure your environment is ready
"""

import sys
import platform
import os
import subprocess

def print_header(text):
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

def test_python():
    print_header("PYTHON ENVIRONMENT")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Virtual env active: {sys.prefix != sys.base_prefix}")

def test_packages():
    print_header("INSTALLED PACKAGES")
    
    packages = [
        ('pyannote.audio', 'pyannote.audio'),
        ('groq', 'groq'),
        ('livekit', 'livekit'),
        ('livekit-api', 'livekit-api'),
        ('supabase', 'supabase'),
        ('numpy', 'numpy'),
        ('pandas', 'pandas'),
        ('sklearn', 'scikit-learn'),
        ('dotenv', 'python-dotenv'),
        ('flask', 'flask')
    ]
    
    for package_name, display_name in packages:
        try:
            if package_name == 'sklearn':
                import sklearn
                print(f"✅ {display_name}: {sklearn.__version__}")
            elif package_name == 'dotenv':
                import dotenv
                print(f"✅ {display_name}: {dotenv.__version__}")
            else:
                mod = __import__(package_name)
                version = getattr(mod, '__version__', 'unknown')
                print(f"✅ {display_name}: {version}")
        except ImportError as e:
            print(f"❌ {display_name}: NOT INSTALLED")
        except Exception as e:
            print(f"⚠️  {display_name}: Error - {e}")

def test_ffmpeg():
    print_header("FFMPEG")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            first_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg found: {first_line}")
            
            # Try to find where ffmpeg is located
            if platform.system() == "Windows":
                where_result = subprocess.run(['where', 'ffmpeg'], 
                                           capture_output=True, text=True)
                if where_result.returncode == 0:
                    print(f"   Location: {where_result.stdout.strip()}")
            return True
        else:
            print("❌ FFmpeg not working properly")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found in PATH")
        print("\nTo fix: Add this to your PATH:")
        print("C:\\ffmpeg\\ffmpeg-8.0.1-essentials_build\\bin")
        return False
    except Exception as e:
        print(f"❌ FFmpeg test error: {e}")
        return False

def test_docker():
    print_header("DOCKER")
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Docker: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker not working")
            return False
    except FileNotFoundError:
        print("❌ Docker not found in PATH")
        print("   Install Docker Desktop from: https://www.docker.com/products/docker-desktop/")
        return False

def test_env_file():
    print_header("ENVIRONMENT FILE")
    if os.path.exists('.env'):
        print("✅ .env file exists")
        # Check if it has placeholder values
        with open('.env', 'r') as f:
            content = f.read()
            if 'your_' in content:
                print("⚠️  .env contains placeholder values - update with real API keys")
        return True
    else:
        print("❌ .env file missing")
        print("   Create one with: notepad .env")
        return False

def main():
    print("\n" + "="*60)
    print("   CLINICAL INTERVIEW IR SYSTEM - SETUP VERIFICATION")
    print("="*60)
    
    test_python()
    test_packages()
    test_ffmpeg()
    test_docker()
    test_env_file()
    
    print_header("NEXT STEPS")
    print("1. If any packages are missing, install them:")
    print("   pip install [package-name]")
    print("\n2. If FFmpeg is missing, add to PATH:")
    print("   C:\\ffmpeg\\ffmpeg-8.0.1-essentials_build\\bin")
    print("\n3. If Docker is missing, install Docker Desktop")
    print("\n4. Update .env with your actual API keys from:")
    print("   - Pyannote: https://dashboard.pyannote.ai")
    print("   - Groq: https://console.groq.com")
    print("   - LiveKit: https://livekit.io/cloud")
    print("   - Supabase: https://supabase.com")
    print("\n5. Run n8n when Docker is ready:")
    print("   docker run -d --name n8n -p 5678:5678 -v C:\\Users\\Administrator\\n8n-data:/home/node/.n8n -e N8N_SECURE_COOKIE=false n8nio/n8n")

if __name__ == "__main__":
    main()