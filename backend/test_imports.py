"""Test imports"""
import sys
print("Starting imports...")
sys.stdout.flush()

print("1. Importing os...")
sys.stdout.flush()
import os

print("2. Importing dotenv...")
sys.stdout.flush()
from dotenv import load_dotenv

print("3. Importing Path...")
sys.stdout.flush()
from pathlib import Path

print("4. Testing dotenv load...")
sys.stdout.flush()
load_dotenv()

print("5. Importing tiktoken...")
sys.stdout.flush()
import tiktoken

print("6. Importing google.generativeai...")
sys.stdout.flush()
import google.generativeai as genai

print("7. Importing faiss...")
sys.stdout.flush()
import faiss

print("✅ All imports successful!")
sys.stdout.flush()
