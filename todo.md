# Project Plan: Blog Data API Pipeline

## 1. File Organization & Input Format
- **Directory Structure:**
  - Place raw blog documents in: `/blogs/(blog-title).docx`
  - Place images in: 
    - `/images/(blog-title)/image-title` (for header/title images)
    - `/images/(blog-title)/image-content` (for inline content images)

- **Source Document (.docx) Specifications:**
  - **Metadata:** The document should contain specific fields such as:
    - Title: [Blog Title]
    - Author: [Author Name]
    - Category: [Category]
    - Date: [Date]
    - Excerpt: [Optional text tag]
    - Content: [Main body text]
    - Frequently Asked Questions: [Heading for FAQs at the end]
  
  - **Formatting Rules:**
    - Preserve formatting styles like headings (H1, H2...), bold, italic, and lists.
    - Standardize font family to "Times New Roman".
  
- **Extraction Logic:**
  - **Title:** Extracted from the "Title:" metadata field or the first H1 heading.
  - **Author:** Extracted from the "Author:" field.
  - **Category:** Extracted from the "Category:" field.
  - **Excerpt:** Extracted from paragraphs appearing *before* the Title, or specifically defined by an `Excerpt:` tag.
  - **Content:** All text and elements following the Title is treated as the main blog content.
  - **FAQs:** Content under the "Frequently Asked Questions" heading is parsed into a specific QnA structure.

## 2. Image Handling
- Images are stored in the structure: `/images/(blog-title)/...`
- **Output:** In the generated HTML, image sources must use the absolute GitHub Pages URL:
  `https://azhabalouch.github.io/blogs-data-api/images/(blog-title)/filename`

## 3. Data Processing & HTML Export
- **Script:** Create a Python script (`export_data.py`) to parse `.docx` files.
- **HTML Conversion:**
  - Convert content to semantic HTML.
  - Wrap the content in a container with `font-family: 'Times New Roman'`.
  - Ensure images render with appropriate `alt`, `width`, and `height` attributes.
  - FAQs should be converted to structured HTML as well.

## 4. JSON API Output
The script will generate a JSON file serving as the "API". 
**Schema:**
```json
{
    "id": 1,
    "date": "MM/DD/YYYY",
    "category": "Technology",
    "author": "Author Name",
    "title": "Blog Title",
    "excerpt": "Short summary...",
    "content": "<div>...HTML Content...</div>",
    "FAQ": "<div>...FAQ HTML...</div>"
}
```

## 5. Automation (CI/CD)
- **Platform:** GitHub Pages will host the JSON API and static assets.
- **Workflow:** Set up a GitHub Actions workflow.
  - **Trigger:** Runs automatically when a commit is pushed to the `main` branch.
  - **Action:** Executes `export_data.py` to regenerate the JSON data and deploys changes to GitHub Pages.

## 6. Admin Interface (index.html)
A simple web interface to simplify uploading new blogs without using git commands manually.
- **Features:**
  1. **Upload DOCX**: Select the blog document.
  2. **Upload Title Image**: Select the main header image.
  3. **Upload Content Images**: Select inline images.
  4. **Preview**: Show a live preview of how the content will look.
  
- **Security & Publishing:**
  - The interface will interact directly with the GitHub Repository.
  - **Authentication:** Require a GitHub Personal Access Token (PAT).
  - **Configuration:** Allow users to input:
    - Repo Name
    - Branch Name
    - Username
    - GitHub Token
  - **Persistence:** Securely save these credentials in the browser's LocalStorage so the user doesn't need to re-enter them frequently.
  - *Note: Ensure client-side security best practices are followed.*
