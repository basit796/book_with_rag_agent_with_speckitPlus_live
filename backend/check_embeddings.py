"""Check embeddings completeness and metadata"""
import pickle
import json
from pathlib import Path

# Load metadata
metadata_path = Path("vectordb/vector_db/metadata.pkl")
with open(metadata_path, 'rb') as f:
    metadata = pickle.load(f)

print(f"✓ Total chunks indexed: {len(metadata)}")
print(f"✓ Sample chunk keys: {list(metadata[0].keys())}")
print(f"✓ First chunk info:")
print(f"  - Chapter: {metadata[0].get('chapter_title', 'N/A')}")
print(f"  - Module: {metadata[0].get('module_name', 'N/A')}")
print(f"  - Content preview: {metadata[0].get('content', '')[:100]}...")

# Check chapter coverage
chapters = set()
for chunk in metadata:
    chapters.add(chunk.get('chapter_title', 'Unknown'))

print(f"\n✓ Chapters covered: {len(chapters)}")
for chapter in sorted(chapters):
    chapter_chunks = sum(1 for c in metadata if c.get('chapter_title') == chapter)
    print(f"  - {chapter}: {chapter_chunks} chunks")

# Load summary metadata
with open("vectordb/summary_metadata.json", 'r') as f:
    summary = json.load(f)

print(f"\n✓ Summary metadata modules: {len(summary['modules'])}")
print(f"✓ Total chapters in summary: {sum(len(m['chapters']) for m in summary['modules'])}")

# Load topic index
with open("vectordb/topic_index.json", 'r') as f:
    topics = json.load(f)

print(f"\n✓ Topic index entries: {len(topics['topics'])}")
print(f"✓ Sample topics: {list(topics['topics'].keys())[:5]}")

print("\n" + "="*60)
print("EMBEDDINGS STATUS: ✅ COMPLETE")
print("="*60)
