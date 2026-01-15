import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class BlogAggregator:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.blogs_dir = self.root_dir / "blogs"
        self.output_file = self.root_dir / "api.json"
    
    def aggregate(self) -> List[Dict]:
        blogs = self._load_existing_blogs()
        existing_ids = {blog['id'] for blog in blogs}
        existing_slugs = {blog.get('slug') for blog in blogs if 'slug' in blog}
        next_id = max(existing_ids) + 1 if existing_ids else 1
        
        if not self.blogs_dir.exists():
            print(f"Error: {self.blogs_dir} not found")
            return blogs

        json_files = list(self.blogs_dir.glob("*.json"))
        
        if not json_files:
            print(f"No .json files found in {self.blogs_dir}")
            self._save_api(blogs)
            return blogs
        
        for json_file in json_files:
            blog_slug = json_file.stem
            
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    blog_data = json.load(f)

                if not self._validate_blog(blog_data):
                    print(f"Skipping {blog_slug}: Missing required fields")
                    continue

                if blog_slug in existing_slugs or blog_data.get('id') in existing_ids:
                    print(f"Already processed: {blog_slug}")
                    continue

                if 'id' not in blog_data or not blog_data['id']:
                    blog_data['id'] = next_id

                blog_data['slug'] = blog_slug
                
                blogs.append(blog_data)
                print(f"Added: {blog_slug} (ID: {blog_data['id']})")
                next_id += 1
                
            except json.JSONDecodeError as e:
                print(f"Error parsing {blog_slug}: Invalid JSON - {str(e)}")
            except Exception as e:
                print(f"Error processing {blog_slug}: {str(e)}")

        blogs.sort(key=lambda x: self._parse_date(x.get('date', '')), reverse=True)

        self._save_api(blogs)
        
        return blogs
    
    def _load_existing_blogs(self) -> List[Dict]:
        if self.output_file.exists():
            try:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('blogs', [])
            except (json.JSONDecodeError, IOError):
                pass
        return []
    
    def _parse_date(self, date_str):
        if not date_str:
            return datetime.now()
        
        normalized = date_str.replace('\\', '/')
        
        for fmt in ["%m/%d/%Y", "%d/%m/%Y"]:
            try:
                return datetime.strptime(normalized, fmt)
            except ValueError:
                continue
        
        return datetime.now()
    
    def _validate_blog(self, blog: Dict) -> bool:
        required_fields = ['title', 'author', 'category', 'date', 'excerpt', 'content']
        return all(field in blog for field in required_fields)
    
    def _save_api(self, blogs: List[Dict]):
        api_data = {
            "blogs": blogs
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(api_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ API saved to {self.output_file}")
        print(f"Total blogs: {len(blogs)}")


def main():
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
