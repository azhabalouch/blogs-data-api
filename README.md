# Blog Data API

A simple blog management system that converts `.docx` documents into a JSON API, automatically deployed to GitHub Pages.

## What Does This Do?

1. **Upload Blog**: Write your blog in Microsoft Word (.docx)
2. **Add Images**: Upload title and content images
3. **Process**: Python script converts everything to JSON
4. **Deploy**: GitHub Actions automatically publishes to GitHub Pages
5. **Access**: Your blog is available as a JSON API

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Your First Blog

Create `blogs/my-first-blog.docx` with this format:

```
Title: My First Blog Post
Author: Your Name
Category: Technology
Date: 01/15/2024
Excerpt: This is a brief preview

## Introduction
Your content here with **bold** and *italic* text.

## Frequently Asked Questions
**Q: First question?**
A: Answer here.
```

### 3. Add Images (Optional)

```
images/
└── my-first-blog/
    ├── image-title/header.jpg
    └── image-content/screenshot.png
```

### 4. Generate API

```bash
python export_data.py
```

You'll see:
```
Processing: my-first-blog
✓ Successfully processed: my-first-blog
✓ API saved to api.json
```

### 5. Deploy to GitHub

```bash
git add .
git commit -m "Add blog"
git push origin main
```

GitHub Actions will automatically:
- Process all blogs
- Generate fresh API
- Deploy to GitHub Pages

### 6. Enable GitHub Pages

1. Go to repository **Settings → Pages**
2. Set source to **gh-pages** branch
3. Save

Your API will be live at:
```
https://YOUR_USERNAME.github.io/blogs-data-api/api.json
```

# Blog Data API - Sample Blog Document

This directory contains sample `.docx` files for testing the blog API pipeline.

## How to Add a Blog

1. Create a new `.docx` file with your blog content
2. Follow the metadata format (see README.md for details)
3. Save it in this directory with a descriptive name
4. Run `python export_data.py` from the root directory
5. The blog will be processed and added to `api.json`

## Document Format

```
Title: Your Blog Title
Author: Your Name
Category: Technology
Date: MM/DD/YYYY
Excerpt: Brief summary...

## Introduction

Your content here...

## Frequently Asked Questions

**Q: First question?**

A: Answer here.
```

## File Naming

- Use hyphens or underscores to separate words
- Example: `my-first-blog.docx` or `my_first_blog.docx`
- The filename (without .docx) will be used for image folder organization

## Next Steps

1. Add sample `.docx` files to this directory
2. Add corresponding images to `/images/(blog-title)/`
3. Run the export script to generate the API

# Images Directory

This directory contains all blog images organized by blog title.

## Structure

```
images/
├── blog-title-1/
│   ├── image-title/
│   │   └── header.jpg (main blog header image)
│   └── image-content/
│       ├── screenshot-1.png
│       └── diagram.png
│
├── blog-title-2/
│   ├── image-title/
│   │   └── cover.jpg
│   └── image-content/
│       └── demo.gif
```

## Guidelines

- **Title Images**: Main header/cover image for the blog
- **Content Images**: Inline images used within blog content

## Image Naming

- Use names: `title.png` & `content.jpg`
- Avoid spaces; use hyphens: `my-image.jpg`
- Supported formats: `.jpg`, `.png`, `.gif`, `.webp`, `.svg`

## GitHub Pages URLs

Images are automatically served from:
```
https://azhabalouch.github.io/blogs-data-api/images/(blog-title)/(image-name)
```

## Optimization Tips

- Compress images before uploading
- Use appropriate formats (JPG for photos, PNG for graphics)
- Keep file sizes under 2MB for faster loading
- Use WebP for better compression

## Admin Interface

Open `index.html` in a browser for a web UI to:
- Upload blog documents
- Upload images
- Configure GitHub credentials
- Preview blogs before publishing
- Deploy with one click

### Using Admin Interface

1. **GitHub Config Tab**
   - Enter your GitHub username
   - Enter repository name
   - Paste Personal Access Token ([Create here](https://github.com/settings/tokens))
   - Test connection

2. **Blog Upload Tab**
   - Select `.docx` file
   - Select title image
   - Select content images
   - Click "Upload & Deploy"

3. **Preview Tab**
   - See how your blog will look
   - View uploaded images
   - Check formatting

## How It Works

### System Flow

```
.docx file + images
    ↓
export_data.py (Python script)
    ↓
Extracts metadata & content
    ↓
Converts to HTML
    ↓
Generates api.json
    ↓
GitHub Actions
    ↓
Deploys to GitHub Pages
    ↓
Public JSON API
```

### File Organization

```
blogs-data-api/
├── blogs/                    # Put your .docx files here
├── images/
│   └── (blog-name)/
│       ├── image-title/     # Header images
│       └── image-content/   # Inline images
├── export_data.py           # Processing script
├── index.html               # Admin web interface
├── api.json                 # Generated API (auto-created)
└── .github/workflows/       # Auto-deployment
```

### Blog Document Format

**Required Fields:**
```
Title: Your Blog Title
Author: Your Name
Category: Technology
Date: MM/DD/YYYY
```

**Optional Fields:**
```
Excerpt: Brief summary (auto-generated if not provided)
```

**Content:**
- Use Word's heading styles (H1, H2, H3)
- Bold and italic formatting supported
- Lists (bullets and numbered)
- Images (will be replaced with uploaded images)

**FAQ Section:**
```
## Frequently Asked Questions

**Q: First question?**
A: Answer here.

**Q: Second question?**
A: Another answer.
```
## API Output

The generated `api.json` structure:

```json
{
  "version": "1.0",
  "lastUpdated": "2024-01-15T10:30:00.000Z",
  "totalBlogs": 5,
  "blogs": [
    {
      "id": 1234567890,
      "date": "01/15/2024",
      "category": "Technology",
      "author": "Jane Doe",
      "title": "My Blog Title",
      "excerpt": "Brief preview...",
      "content": "<div>...HTML...</div>",
      "FAQ": "<div>...FAQ HTML...</div>"
    }
  ]
}
```

### Using the API

**Fetch all blogs:**
```javascript
fetch('https://YOUR_USERNAME.github.io/blogs-data-api/api.json')
  .then(res => res.json())
  .then(data => {
    data.blogs.forEach(blog => {
      console.log(blog.title);
    });
  });
```

**Display blog:**
```javascript
const blog = data.blogs[0];
document.getElementById('content').innerHTML = blog.content;
```

**Filter by category:**
```javascript
const techBlogs = data.blogs.filter(b => b.category === 'Technology');
```

## Troubleshooting

### Python not found
```bash
python --version  # Check if installed
# On Windows, try: python3 --version
```

### Dependencies error
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### api.json not generated
```bash
# Check if .docx files exist
ls blogs/

# Run with error output
python export_data.py
```

### GitHub Actions failing
1. Check Actions tab in GitHub
2. Review error logs
3. Ensure .docx files are valid
4. Verify Python syntax: `python -m py_compile export_data.py`

## Configuration

### Change GitHub Pages URL

Edit `config.py`:
```python
API_CONFIG = {
    'github_pages_url': 'https://YOUR_USERNAME.github.io/YOUR_REPO',
    'image_base_url': 'https://YOUR_USERNAME.github.io/YOUR_REPO/images',
}
```

### Customize Output

Modify `export_data.py` to:
- Add custom metadata fields
- Change HTML styling
- Adjust image processing
- Add content transformations

## Technical Details

### Components

1. **export_data.py** - Python script that:
   - Reads .docx files using python-docx library
   - Extracts metadata with regex patterns
   - Converts paragraphs to HTML
   - Normalizes image URLs
   - Generates JSON output

2. **index.html** - Web interface that:
   - Uses Mammoth.js to preview DOCX in browser
   - Stores GitHub credentials in LocalStorage
   - Validates file uploads
   - Shows preview with uploaded images

3. **.github/workflows/deploy.yml** - GitHub Actions that:
   - Installs Python dependencies
   - Runs export script
   - Validates JSON
   - Commits to repository
   - Deploys to gh-pages branch

### Security

- ✅ GitHub tokens stored in browser only (not in code)
- ✅ No credentials in Git history
- ✅ HTML content sanitized during processing
- ✅ Image validation (format & size)
- ✅ CORS headers for API access

## Support

- Issues with setup? Check [Troubleshooting](#troubleshooting)
- DOCX not parsing? Verify format matches [Blog Document Format](#blog-document-format)
- API not updating? Check [GitHub Actions](#github-actions-workflow)
