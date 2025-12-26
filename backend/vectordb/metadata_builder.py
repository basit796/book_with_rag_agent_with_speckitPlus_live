"""Build metadata files for book structure and topic indexing"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any
import json


def extract_title_from_markdown(file_path: Path) -> str:
    """Extract the title from the first # header in a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
        # Fallback: use filename
        return file_path.stem.replace('-', ' ').title()
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
        return file_path.stem.replace('-', ' ').title()


def extract_topics_from_markdown(file_path: Path) -> List[str]:
    """Extract topic keywords from markdown content."""
    topics = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Extract from headers (##, ###)
            headers = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
            for header in headers:
                # Clean and add significant words
                words = re.findall(r'\b[A-Z][a-z]+\b|\b[A-Z]{2,}\b', header)
                topics.update(words)
            
            # Extract bold text (often key terms)
            bold_terms = re.findall(r'\*\*(.+?)\*\*', content)
            for term in bold_terms:
                if len(term) < 30 and not term.startswith('http'):  # Reasonable term length
                    topics.add(term.strip())
            
            # Extract code blocks languages (programming concepts)
            code_langs = re.findall(r'```(\w+)', content)
            topics.update(code_langs)
    
    except Exception as e:
        print(f"⚠️  Error extracting topics from {file_path}: {e}")
    
    return sorted(list(topics))[:10]  # Limit to top 10 topics


def count_words_in_file(file_path: Path) -> int:
    """Count words in a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Remove code blocks
            content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            # Remove markdown syntax
            content = re.sub(r'[#*`\[\]()]', '', content)
            # Count words
            words = content.split()
            return len(words)
    except Exception as e:
        print(f"⚠️  Error counting words in {file_path}: {e}")
        return 0


def get_module_title(module_name: str) -> str:
    """Get human-readable title for module."""
    module_titles = {
        "module-1-physical-ai": "Physical AI Foundations",
        "module-2-ros2": "ROS2 Middleware",
        "module-3-simulation": "Simulation & Digital Twins",
        "module-4-isaac": "NVIDIA Isaac Platform"
    }
    return module_titles.get(module_name, module_name.replace('-', ' ').title())


def build_summary_metadata(docs_dir: Path) -> Dict[str, Any]:
    """
    Build summary metadata with module and chapter structure.
    
    Returns structure:
    {
        "modules": [
            {
                "id": "module-1-physical-ai",
                "title": "Physical AI Foundations",
                "order": 1,
                "description": "...",
                "chapters": [
                    {
                        "id": "01-what-is-physical-ai",
                        "number": 1,
                        "title": "What is Physical AI?",
                        "file_path": "docs/module-1-physical-ai/01-what-is-physical-ai.md",
                        "topics": ["AI", "Robotics", ...],
                        "word_count": 2500
                    }
                ]
            }
        ],
        "total_chapters": 16,
        "total_modules": 4,
        "total_words": 42000
    }
    """
    modules = []
    total_words = 0
    total_chapters = 0
    
    # Find all module directories
    module_dirs = sorted([d for d in docs_dir.iterdir() if d.is_dir() and d.name.startswith('module-')])
    
    for module_order, module_dir in enumerate(module_dirs, start=1):
        module_name = module_dir.name
        module_title = get_module_title(module_name)
        
        chapters = []
        module_word_count = 0
        
        # Find all markdown files in module
        chapter_files = sorted([f for f in module_dir.iterdir() if f.suffix == '.md'])
        
        for chapter_file in chapter_files:
            # Extract chapter number from filename (e.g., "01-what-is-physical-ai.md" -> 1)
            chapter_number_match = re.match(r'(\d+)-', chapter_file.name)
            chapter_number = int(chapter_number_match.group(1)) if chapter_number_match else len(chapters) + 1
            
            chapter_id = chapter_file.stem
            chapter_title = extract_title_from_markdown(chapter_file)
            topics = extract_topics_from_markdown(chapter_file)
            word_count = count_words_in_file(chapter_file)
            
            chapters.append({
                "id": chapter_id,
                "number": chapter_number,
                "title": chapter_title,
                "file_path": f"docs/{module_name}/{chapter_file.name}",
                "topics": topics,
                "word_count": word_count
            })
            
            module_word_count += word_count
            total_words += word_count
            total_chapters += 1
        
        # Get module description (from first chapter intro or default)
        module_description = f"Learn about {module_title.lower()}"
        
        modules.append({
            "id": module_name,
            "title": module_title,
            "order": module_order,
            "description": module_description,
            "chapters": chapters,
            "word_count": module_word_count
        })
    
    return {
        "modules": modules,
        "total_chapters": total_chapters,
        "total_modules": len(modules),
        "total_words": total_words
    }


def build_topic_index(summary_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build topic index for fast topic lookup.
    
    Returns structure:
    {
        "topics": {
            "ROS2": {
                "chapters": ["module-2-ros2/01-why-middleware.md", ...],
                "description": "Robot Operating System 2"
            },
            "Isaac Sim": {
                "chapters": ["module-4-isaac/02-isaac-sim-overview.md"],
                "description": "NVIDIA Isaac Simulator"
            }
        },
        "module_index": {
            "module-1-physical-ai": ["01-what-is-physical-ai.md", ...],
            "module-2-ros2": ["01-why-middleware.md", ...]
        }
    }
    """
    topics = {}
    module_index = {}
    
    # Build indices from summary
    for module in summary_metadata["modules"]:
        module_id = module["id"]
        module_index[module_id] = []
        
        for chapter in module["chapters"]:
            chapter_path = chapter["file_path"]
            chapter_filename = Path(chapter_path).name
            
            # Add to module index
            module_index[module_id].append(chapter_filename)
            
            # Build topic index from chapter topics
            for topic in chapter["topics"]:
                if topic not in topics:
                    topics[topic] = {
                        "chapters": [],
                        "description": f"Learn about {topic}"
                    }
                
                if chapter_path not in topics[topic]["chapters"]:
                    topics[topic]["chapters"].append(chapter_path)
            
            # Add module name as a topic
            module_topic = module["title"]
            if module_topic not in topics:
                topics[module_topic] = {
                    "chapters": [],
                    "description": module["description"]
                }
            topics[module_topic]["chapters"].append(chapter_path)
            
            # Add chapter title as a topic
            chapter_title = chapter["title"]
            if chapter_title not in topics:
                topics[chapter_title] = {
                    "chapters": [chapter_path],
                    "description": f"Chapter: {chapter_title}"
                }
    
    return {
        "topics": topics,
        "module_index": module_index
    }


def build_metadata(docs_dir: Path, output_dir: Path):
    """
    Build both summary and index metadata files.
    
    Args:
        docs_dir: Path to docs directory
        output_dir: Path to save metadata files
    """
    print("=== Building Metadata ===\n")
    
    # Step 1: Build summary metadata
    print("Step 1: Building summary metadata...")
    summary_metadata = build_summary_metadata(docs_dir)
    
    print(f"  Found {summary_metadata['total_modules']} modules")
    print(f"  Found {summary_metadata['total_chapters']} chapters")
    print(f"  Total words: {summary_metadata['total_words']:,}")
    
    # Step 2: Build topic index
    print("\nStep 2: Building topic index...")
    topic_index = build_topic_index(summary_metadata)
    
    print(f"  Indexed {len(topic_index['topics'])} unique topics")
    print(f"  Indexed {len(topic_index['module_index'])} modules")
    
    # Step 3: Save files
    print("\nStep 3: Saving metadata files...")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    summary_path = output_dir / "summary_metadata.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary_metadata, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Saved {summary_path}")
    
    index_path = output_dir / "topic_index.json"
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(topic_index, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Saved {index_path}")
    
    print("\n=== Metadata Build Complete ===")
    
    return summary_metadata, topic_index


if __name__ == "__main__":
    # Build metadata
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent.parent / "docs"
    output_dir = script_dir
    
    if not docs_dir.exists():
        print(f"❌ Docs directory not found: {docs_dir}")
        exit(1)
    
    build_metadata(docs_dir, output_dir)
