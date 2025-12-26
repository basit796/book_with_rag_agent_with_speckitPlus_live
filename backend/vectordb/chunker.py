"""Markdown chunking logic with context preservation"""

import re
import tiktoken
from pathlib import Path
from typing import List, Dict, Any


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken."""
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception:
        # Fallback: estimate 1 token per 4 characters
        return len(text) // 4


def extract_headers(content: str) -> List[tuple]:
    """Extract all markdown headers with their positions."""
    headers = []
    for match in re.finditer(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE):
        headers.append((match.start(), match.group(1), match.group(2).strip()))
    return headers


def split_by_sections(content: str, max_tokens: int = 800) -> List[Dict[str, Any]]:
    """Split content by sections (## headers) while preserving context."""
    headers = extract_headers(content)
    
    if not headers:
        # No headers, treat entire content as one section
        return [{"content": content, "heading": ""}]
    
    sections = []
    for i, (pos, level, heading) in enumerate(headers):
        # Find content until next header of same or higher level
        end_pos = len(content)
        for j in range(i + 1, len(headers)):
            next_pos, next_level, _ = headers[j]
            if len(next_level) <= len(level):  # Same or higher level header
                end_pos = next_pos
                break
        
        section_content = content[pos:end_pos].strip()
        
        # If section is too large, split further by paragraphs
        if count_tokens(section_content) > max_tokens:
            sub_chunks = split_by_paragraphs(section_content, heading, max_tokens)
            sections.extend(sub_chunks)
        else:
            sections.append({
                "content": section_content,
                "heading": heading
            })
    
    return sections


def split_by_paragraphs(text: str, heading: str, max_tokens: int) -> List[Dict[str, Any]]:
    """Split large section by paragraphs."""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = f"## {heading}\n\n" if heading else ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        test_chunk = current_chunk + para + "\n\n"
        if count_tokens(test_chunk) > max_tokens and current_chunk:
            # Save current chunk
            chunks.append({
                "content": current_chunk.strip(),
                "heading": heading
            })
            current_chunk = f"## {heading}\n\n{para}\n\n"
        else:
            current_chunk = test_chunk
    
    # Add remaining content
    if current_chunk.strip():
        chunks.append({
            "content": current_chunk.strip(),
            "heading": heading
        })
    
    return chunks


def add_overlap(chunks: List[Dict[str, Any]], overlap_tokens: int = 150) -> List[Dict[str, Any]]:
    """Add overlap from previous chunk for context continuity."""
    if len(chunks) <= 1:
        return chunks
    
    for i in range(1, len(chunks)):
        prev_content = chunks[i-1]["content"]
        # Get last paragraphs from previous chunk
        prev_paras = prev_content.split('\n\n')
        
        # Collect overlap text
        overlap = []
        token_count = 0
        for para in reversed(prev_paras):
            para_tokens = count_tokens(para)
            if token_count + para_tokens > overlap_tokens:
                break
            overlap.insert(0, para)
            token_count += para_tokens
        
        if overlap:
            overlap_text = '\n\n'.join(overlap)
            chunks[i]["content"] = f"{overlap_text}\n\n---\n\n{chunks[i]['content']}"
    
    return chunks


def chunk_markdown_file(file_path: Path, module_name: str, chapter_number: int) -> List[Dict[str, Any]]:
    """Chunk a single markdown file with metadata."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from first # header
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    chapter_title = title_match.group(1).strip() if title_match else file_path.stem
    
    # Split into sections
    sections = split_by_sections(content, max_tokens=800)
    
    # Add overlap
    sections = add_overlap(sections, overlap_tokens=150)
    
    # Add metadata
    chunks = []
    for idx, section in enumerate(sections):
        chunks.append({
            "id": f"{file_path.stem}-chunk-{idx}",
            "content": section["content"],
            "metadata": {
                "module_name": module_name,
                "chapter_number": chapter_number,
                "chapter_id": file_path.stem,
                "chapter_title": chapter_title,
                "section_heading": section["heading"],
                "file_path": str(file_path),
                "chunk_index": idx,
                "word_count": len(section["content"].split()),
                "has_code_blocks": "```" in section["content"],
                "has_images": "![" in section["content"]
            }
        })
    
    return chunks


def chunk_markdown_files(docs_dir: Path) -> List[Dict[str, Any]]:
    """Chunk all markdown files in the docs directory."""
    all_chunks = []
    
    # Define modules
    modules = [
        ("module-1-physical-ai", 1, "Physical AI Foundations"),
        ("module-2-ros2", 2, "ROS2 Middleware"),
        ("module-3-simulation", 3, "Simulation Foundations"),
        ("module-4-isaac", 4, "NVIDIA Isaac Platform")
    ]
    
    for module_dir, module_num, module_title in modules:
        module_path = docs_dir / module_dir
        if not module_path.exists():
            print(f"Warning: Module directory not found: {module_path}")
            continue
        
        # Get all .md files
        md_files = sorted(module_path.glob("*.md"))
        
        for chapter_idx, md_file in enumerate(md_files, start=1):
            print(f"Processing: {md_file.name}")
            file_chunks = chunk_markdown_file(md_file, module_dir, chapter_idx)
            all_chunks.extend(file_chunks)
    
    print(f"\nTotal chunks created: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    # Test chunking
    docs_path = Path(__file__).parent.parent.parent / "docs"
    chunks = chunk_markdown_files(docs_path)
    print(f"\nSample chunk:")
    print(f"ID: {chunks[0]['id']}")
    print(f"Metadata: {chunks[0]['metadata']}")
    print(f"Content preview: {chunks[0]['content'][:200]}...")
