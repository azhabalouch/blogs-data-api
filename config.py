#!/usr/bin/env python3
"""
Configuration file for Blog Data API
Contains settings for the export process
"""

# Blog API Configuration
API_CONFIG = {
    # GitHub Pages URL (change to your GitHub Pages domain)
    'github_pages_url': 'https://azhabalouch.github.io/blogs-data-api',
    
    # Image base URL
    'image_base_url': 'https://azhabalouch.github.io/blogs-data-api/images',
    
    # Default metadata
    'default_author': 'Unknown',
    'default_category': 'General',
    
    # HTML styling
    'default_font_family': 'Times New Roman',
    'content_wrapper_style': "font-family: 'Times New Roman', serif;",
    
    # Image dimensions
    'image_max_width': '100%',
    'image_default_height': 'auto',
}

# Metadata fields to extract from documents
METADATA_FIELDS = {
    'title': 'Title',
    'author': 'Author',
    'category': 'Category',
    'date': 'Date',
    'excerpt': 'Excerpt',
    'content': 'Content',
    'faq': 'Frequently Asked Questions'
}

# Supported image formats
IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']

# File processing
FILES_CONFIG = {
    'blogs_directory': 'blogs',
    'images_directory': 'images',
    'output_file': 'api.json',
    'allowed_extensions': ['.docx'],
}

if __name__ == '__main__':
    print("Blog Data API Configuration")
    print("=" * 50)
    print(f"GitHub Pages URL: {API_CONFIG['github_pages_url']}")
    print(f"Image Base URL: {API_CONFIG['image_base_url']}")
    print(f"Blogs Directory: {FILES_CONFIG['blogs_directory']}")
    print(f"Images Directory: {FILES_CONFIG['images_directory']}")
    print(f"Output File: {FILES_CONFIG['output_file']}")
