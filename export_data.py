#!/usr/bin/env python3
"""
Blog Data API Aggregator
Reads JSON blog files from /blogs directory and generates aggregated api.json
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class BlogAggregator:
    """Aggregates individual blog JSON files into a single API file"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.blogs_dir = self.root_dir / "blogs"
        self.output_file = self.root_dir / "api.json"
    
    def aggregate(self) -> List[Dict]:
        """Aggregate all blog JSON files into a single API"""
        blogs = []
        
        if not self.blogs_dir.exists():
            print(f"Error: {self.blogs_dir} not found")
            return blogs
        
        # Find all .json files
        json_files = list(self.blogs_dir.glob("*.json"))
        
        if not json_files:
            print(f"No .json files found in {self.blogs_dir}")
            # Still create empty api.json
            self._save_api(blogs)
            return blogs
        
        for json_file in json_files:
            blog_slug = json_file.stem  # filename without extension
            
            try:
                print(f"Processing: {blog_slug}")
                with open(json_file, 'r', encoding='utf-8') as f:
                    blog_data = json.load(f)
                
                # Validate required fields
                if not self._validate_blog(blog_data):
                    print(f"⚠️  Skipping {blog_slug}: Missing required fields")
                    continue
                
                blogs.append(blog_data)
                print(f"✓ Successfully processed: {blog_slug}")
            except json.JSONDecodeError as e:
                print(f"✗ Error parsing {blog_slug}: Invalid JSON - {str(e)}")
            except Exception as e:
                print(f"✗ Error processing {blog_slug}: {str(e)}")
        
        # Sort by date (newest first)
        def parse_date(date_str):
            """Parse date in multiple formats"""
            if not date_str:
                return datetime.now()
            
            # Normalize backslashes to forward slashes
            normalized = date_str.replace('\\', '/')
            
            # Try MM/DD/YYYY first
            for fmt in ["%m/%d/%Y", "%d/%m/%Y"]:
                try:
                    return datetime.strptime(normalized, fmt)
                except ValueError:
                    continue
            
            # If all fail, return current date
            return datetime.now()
        
        blogs.sort(key=lambda x: parse_date(x.get('date', '')), reverse=True)
        
        # Save to API file
        self._save_api(blogs)
        
        return blogs
    
    def _validate_blog(self, blog: Dict) -> bool:
        """Validate blog has required fields"""
        required_fields = ['id', 'title', 'author', 'category', 'date', 'excerpt', 'content']
        return all(field in blog for field in required_fields)
    
    def _get_next_id(self) -> int:
        """Get the next ID by reading the current API file and incrementing"""
        if self.output_file.exists():
            try:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    current_id = existing_data.get('id', 0)
                    return current_id + 1
            except (json.JSONDecodeError, IOError):
                return 1
        return 1
    
    def _save_api(self, blogs: List[Dict]):
        """Save blogs to JSON file"""
        api_id = self._get_next_id()
        api_data = {
            "id": api_id,
            "blogs": blogs
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(api_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ API saved to {self.output_file} (ID: {api_id})")


def main():
    """Main entry point"""
    aggregator = BlogAggregator()
    blogs = aggregator.aggregate()
    
    if blogs:
        print(f"\n{'='*50}")
        print(f"Successfully aggregated {len(blogs)} blog(s)")
        print(f"{'='*50}")
    else:
        print("\nNo blogs were processed.")


if __name__ == "__main__":
    main()

