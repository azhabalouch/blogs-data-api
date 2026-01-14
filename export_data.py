#!/usr/bin/env python3
"""
Blog Data API Export Script
Parses .docx files from /blogs directory and generates JSON API output
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor


class BlogDocxParser:
    """Parse DOCX blog files and extract structured data"""
    
    def __init__(self, docx_path: str, blog_title: str):
        self.docx_path = docx_path
        self.blog_title = blog_title
        self.doc = Document(docx_path)
        self.metadata = {}
        self.excerpt = ""
        self.content_html = ""
        self.faq_html = ""
        self.image_base_url = f"https://azhabalouch.github.io/blogs-data-api/images/{blog_title}"
        
    def parse(self) -> Dict:
        """Parse the document and extract all data"""
        self._extract_metadata()
        self._extract_excerpt()
        self._extract_content()
        self._extract_faq()
        
        return self._build_output()
    
    def _extract_metadata(self):
        """Extract metadata fields from document"""
        full_text = "\n".join([p.text for p in self.doc.paragraphs])
        
        # Define metadata patterns
        patterns = {
            'title': r'Title:\s*(.+?)(?=\n|Author:|$)',
            'author': r'Author:\s*(.+?)(?=\n|Category:|$)',
            'category': r'Category:\s*(.+?)(?=\n|Date:|$)',
            'date': r'Date:\s*(.+?)(?=\n|Excerpt:|$)',
            'excerpt': r'Excerpt:\s*(.+?)(?=\n|Content:|$)',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
            if match:
                self.metadata[key] = match.group(1).strip()
            else:
                self.metadata[key] = ""
        
        # Default title to first H1 if not found
        if not self.metadata.get('title'):
            for para in self.doc.paragraphs:
                if para.style.name.startswith('Heading 1'):
                    self.metadata['title'] = para.text
                    break
        
        # Set defaults for missing fields
        if not self.metadata.get('date'):
            self.metadata['date'] = datetime.now().strftime("%m/%d/%Y")
        
        if not self.metadata.get('category'):
            self.metadata['category'] = "General"
        
        if not self.metadata.get('author'):
            self.metadata['author'] = "Unknown"
    
    def _extract_excerpt(self):
        """Extract excerpt from document"""
        if self.metadata.get('excerpt'):
            self.excerpt = self.metadata['excerpt']
        else:
            # Get first paragraph that's not metadata
            for para in self.doc.paragraphs:
                text = para.text.strip()
                if text and not any(text.startswith(f"{key}:") for key in ['Title', 'Author', 'Category', 'Date', 'Excerpt', 'Content']):
                    if not para.style.name.startswith('Heading'):
                        self.excerpt = text[:200] + ("..." if len(text) > 200 else "")
                        break
    
    def _extract_content(self):
        """Extract main content and convert to HTML"""
        html_parts = []
        skip_until_content = True
        in_faq = False
        
        for para in self.doc.paragraphs:
            text = para.text.strip()
            
            # Skip metadata section
            if any(text.startswith(f"{key}:") for key in ['Title', 'Author', 'Category', 'Date', 'Excerpt']):
                continue
            
            # Stop when reaching FAQ section
            if 'frequently asked questions' in text.lower():
                in_faq = True
                break
            
            # Convert paragraph to HTML
            if text:
                html_parts.append(self._paragraph_to_html(para))
        
        self.content_html = self._wrap_content(html_parts)
    
    def _extract_faq(self):
        """Extract FAQ section and convert to HTML"""
        html_parts = []
        in_faq = False
        current_question = None
        current_answer_parts = []
        
        for para in self.doc.paragraphs:
            text = para.text.strip()
            
            # Start collecting FAQs after "Frequently Asked Questions" heading
            if 'frequently asked questions' in text.lower():
                in_faq = True
                continue
            
            if not in_faq:
                continue
            
            # Skip empty paragraphs
            if not text:
                continue
            
            # Check if this is a question (usually bold or heading style)
            is_question = (para.style.name.startswith('Heading') or 
                          any(run.bold for run in para.runs))
            
            if is_question:
                # Save previous Q&A if exists
                if current_question:
                    answer_html = "".join(current_answer_parts)
                    html_parts.append(
                        f'<div class="faq-item">'
                        f'<h3 class="faq-question">{current_question}</h3>'
                        f'<div class="faq-answer">{answer_html}</div>'
                        f'</div>'
                    )
                
                current_question = text
                current_answer_parts = []
            else:
                # Add to current answer
                current_answer_parts.append(self._paragraph_to_html(para))
        
        # Save last Q&A
        if current_question:
            answer_html = "".join(current_answer_parts)
            html_parts.append(
                f'<div class="faq-item">'
                f'<h3 class="faq-question">{current_question}</h3>'
                f'<div class="faq-answer">{answer_html}</div>'
                f'</div>'
            )
        
        if html_parts:
            self.faq_html = (
                '<div class="faq-container">'
                + "".join(html_parts) +
                '</div>'
            )
    
    def _paragraph_to_html(self, para) -> str:
        """Convert a paragraph to HTML"""
        if not para.text.strip():
            return ""
        
        # Determine heading level
        style_name = para.style.name
        if style_name.startswith('Heading 1'):
            tag = 'h1'
        elif style_name.startswith('Heading 2'):
            tag = 'h2'
        elif style_name.startswith('Heading 3'):
            tag = 'h3'
        elif style_name.startswith('Heading 4'):
            tag = 'h4'
        elif style_name.startswith('List'):
            return self._list_to_html(para)
        else:
            tag = 'p'
        
        # Build inline HTML with formatting
        inner_html = self._build_inline_html(para)
        
        return f'<{tag}>{inner_html}</{tag}>'
    
    def _build_inline_html(self, para) -> str:
        """Build HTML with inline formatting (bold, italic, images)"""
        html_parts = []
        
        for run in para.runs:
            text = run.text
            
            # Process images in runs (if any)
            if text.startswith('http'):
                # External image URL
                html_parts.append(
                    f'<img src="{self._normalize_image_url(text)}" '
                    f'alt="image" width="100%" />'
                )
            else:
                # Format text with bold/italic
                if run.bold:
                    text = f'<strong>{text}</strong>'
                if run.italic:
                    text = f'<em>{text}</em>'
                if run.underline:
                    text = f'<u>{text}</u>'
                
                html_parts.append(text)
        
        return "".join(html_parts)
    
    def _normalize_image_url(self, url: str) -> str:
        """Normalize image URLs to GitHub Pages format"""
        # Extract filename if it's a path
        filename = os.path.basename(url)
        return f"{self.image_base_url}/{filename}"
    
    def _list_to_html(self, para) -> str:
        """Convert list paragraph to HTML"""
        style_name = para.style.name
        is_ordered = 'numbered' in style_name.lower()
        tag = 'ol' if is_ordered else 'ul'
        
        inner_html = self._build_inline_html(para)
        return f'<li>{inner_html}</li>'
    
    def _wrap_content(self, html_parts: List[str]) -> str:
        """Wrap content in container with proper styling"""
        inner_html = "".join(html_parts)
        
        return (
            '<div style="font-family: \'Times New Roman\', serif;">'
            + inner_html +
            '</div>'
        )
    
    def _build_output(self) -> Dict:
        """Build final JSON output"""
        return {
            "id": self._generate_id(),
            "date": self.metadata.get('date', datetime.now().strftime("%m/%d/%Y")),
            "category": self.metadata.get('category', 'General'),
            "author": self.metadata.get('author', 'Unknown'),
            "title": self.metadata.get('title', self.blog_title),
            "excerpt": self.excerpt,
            "content": self.content_html,
            "FAQ": self.faq_html
        }
    
    def _generate_id(self) -> int:
        """Generate unique ID based on blog title"""
        # Simple hash-based ID
        return abs(hash(self.blog_title)) % (10 ** 8)


class BlogDataExporter:
    """Main exporter that processes all blogs and generates API"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.blogs_dir = self.root_dir / "blogs"
        self.output_file = self.root_dir / "api.json"
    
    def export(self) -> List[Dict]:
        """Export all blogs to JSON API"""
        blogs = []
        
        if not self.blogs_dir.exists():
            print(f"Error: {self.blogs_dir} not found")
            return blogs
        
        # Find all .docx files
        docx_files = list(self.blogs_dir.glob("*.docx"))
        
        if not docx_files:
            print(f"No .docx files found in {self.blogs_dir}")
            return blogs
        
        for docx_file in docx_files:
            blog_title = docx_file.stem  # filename without extension
            
            try:
                print(f"Processing: {blog_title}")
                parser = BlogDocxParser(str(docx_file), blog_title)
                blog_data = parser.parse()
                blogs.append(blog_data)
                print(f"✓ Successfully processed: {blog_title}")
            except Exception as e:
                print(f"✗ Error processing {blog_title}: {str(e)}")
        
        # Sort by date (newest first)
        blogs.sort(key=lambda x: datetime.strptime(x['date'], "%m/%d/%Y"), reverse=True)
        
        # Save to API file
        self._save_api(blogs)
        
        return blogs
    
    def _save_api(self, blogs: List[Dict]):
        """Save blogs to JSON file"""
        api_data = {
            "version": "1.0",
            "lastUpdated": datetime.now().isoformat(),
            "blogs": blogs
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(api_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ API saved to {self.output_file}")


def main():
    """Main entry point"""
    exporter = BlogDataExporter()
    blogs = exporter.export()
    
    if blogs:
        print(f"\n{'='*50}")
        print(f"Successfully processed {len(blogs)} blog(s)")
        print(f"{'='*50}")
    else:
        print("\nNo blogs were processed.")


if __name__ == "__main__":
    main()
