# Adobe Hackathon Round 1B: Persona-Driven Document Intelligence

## Goal

The goal of this task was to process a PDF like a machine — extract its high-level structure and identify meaningful sections, ranked by relevance to a user-defined persona and task ("job to be done").

## Overview

This solution reads through a bunch of PDF files and picks out the parts that matter most based on what a specific person is looking for. It uses simple natural language processing and compares the content using TF-IDF scores to figure out what’s most relevant. Then, it organizes and ranks the sections so the important information is easy to find and understand.

## Features

- **Multi-Method Extraction**: Uses PyMuPDF for existing bookmarks, falls back to font-based analysis
- **Fast Performance**: Optimized for ≤10 second processing of 50-page PDFs
- **CPU Optimized**: Runs efficiently on AMD64 architecture without GPU requirements
- **Robust Analysis**: Intelligent font size and formatting analysis for heading detection
- **Docker Ready**: Containerized solution with all dependencies included

## Methodology

1. **PDF Text Extraction**:
   - Each PDF is parsed using PyMuPDF.
   - Text blocks are filtered based on visual cues such as starting with a capital letter and having a minimum     length, as well as basic regex rules to identify candidate headings.

2. **Section Detection**:
   - We identify section-level headings (not necessarily structured like H1/H2/H3 here) by looking at bold or larger-font text that usually appears in blocks at the beginning of paragraphs or pages.

3. **Ranking Relevant Sections**:
   - We build a TF-IDF vector space using all detected section texts and the user’s `job_to_be_done` phrase.
   - Cosine similarity is used to score how relevant each section is to the job/task.
   - The top 5 sections are selected and ranked by their importance.

4. **Subsection Extraction**:
   - Each top section is further split into smaller paragraphs.
   - These paragraphs are again ranked by similarity to the job description to extract the top 3 refined insights or highlights.

5. **JSON Construction**:
   - The final structured output contains:
     - Metadata (persona, job, timestamp, input files)
     - Top-ranked sections with page numbers
     - Refined highlights for deeper insight

## Execution Setup

The solution is fully containerized using Docker. It processes PDFs from an input folder and writes the output as a JSON file to the output folder, supporting offline and fast execution (≤10s for 50 pages). The Docker image respects all constraints including no GPU, no internet, and ≤200MB model usage.

## Input/Output Format

### Input
- Directory: `/input_pdfs`
- Format: PDF files (*.pdf)
- Limit: Up to 50 pages per PDF

### Output
- Directory: `/output`
- Format: JSON files with same name 'output'
- Structure:
```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "College Student Exploring Data Analytics",
    "job_to_be_done": "Understand key tools and skills needed to become a data analyst",
    "processing_timestamp": "2025-07-26T14:30:00"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "page_number": 4,
      "section_title": "Data Analytics Tools Overview",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "refined_text": "Pandas is a fundamental Python library for data wrangling...",
      "page_number": 4
    }
  ]
}
```
## Performance Specifications

- **Input Limit**: 3–10 PDFs per run
- **Output**: Single structured JSON file
- **Processing Time**: ~1–2 seconds per document (avg. 5–10 pages)
- **Model Type**: Lightweight, rule-based with TF-IDF (no external model or internet dependency)

## Error Handling

- Graceful exit if input folder contains less than 3 or more than 10 PDFs
- Robust handling of empty or non-relevant text blocks
- Ensures fallback to empty output structures rather than failure

## Future Enhancements
- Use of language models for deeper semantic scoring
- Dockerized deployment for easier portability
- GUI/Web interface for easier persona input and result viewing

## Summary

The solution is built in a clean, flexible way, so it’s easy to expand or adjust later. It runs well even without internet and handles performance limits smoothly. Overall, it lays a solid base for future hackathon tasks and helps make sense of documents based on what different types of users are looking for.

---

**Authors**: 
- Suyash Pandey
- Atishay Jain
- Dhwanit Shah
**Created**: 2025
