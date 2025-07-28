# Adobe Hackathon Round 1B: Persona-Driven Document Intelligence

## Overview  
This project addresses the Persona-Driven Document Intelligence challenge from Adobe India Hackathon Round 1B.  
It processes a collection of PDFs to identify and rank sections most relevant to a given persona and job-to-be-done using TF-IDF-based semantic scoring.

## Key Features
- Fully Dockerized and CPU-optimized  
- Accepts 3–10 PDFs and a persona + job-to-be-done input  
- Uses TF-IDF and cosine similarity for relevance scoring  
- Intelligent section extraction using PyMuPDF  
-  Subsection-level analysis and ranking  
-  Clean, structured JSON output  

## Input Requirements
- Place PDFs (3 to 10 files) inside:  
  `app/input_pdfs/`  

- Enter persona and job_to_be_done via terminal prompt  
- Each PDF should be ≤ 50 pages  

## Output Format
Output will be written to:  
`app/output/output.json`

### Example Output Structure
```json
{
  "metadata": {
    "persona": "PhD Researcher in Computational Biology",
    "job_to_be_done": "Prepare a lecture on it",
    "input_documents": [
      "2506.01302v1.pdf",
      "Graph_Neural_Networks_for_Drug_Discovery_An_Integrated_Decision_Support_Pipeline.pdf",
      "paper-5.pdf",
      "peerj-13163.pdf"
    ],
    "processing_timestamp": "2025-07-27T10:58:38"
  },
  "extracted_sections": [
    {
      "document": "paper-5.pdf",
      "page_number": 1,
      "section_title": "Explaining Graph Neural Network Predictions for Drug Repurposing",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "paper-5.pdf",
      "refined_text": "Here we show that the attention mechanism allows interpretation of which drug-target interactions influence the GNN model prediction...",
      "page_number": 1
    }
  ]
}
```
## How It Works
1.	PDFs are parsed using PyMuPDF
2.	Headings are detected using font size and layout rules
3.	TF-IDF vectorizer scores relevance using cosine similarity
4.	Top sections are refined using paragraph-level filtering
5.	Results are saved in structured JSON format
   
## Docker Setup
Build the Docker Image
docker build --platform linux/amd64 -t persona-docs .

## Run the Container
docker run --rm \
  -v $(pwd)/app/input_pdfs:/app/input_pdfs \
  -v $(pwd)/app/output:/app/output \
  persona-docs

## Folder Structure
├── app/
│   ├── main.py
│   ├── requirements.txt
│   ├── input_pdfs/        # PDF files to process
│   └── output/            # JSON output written here
├── Dockerfile
├── README.md (this file)

## Performance
- Runtime: ~1–2 seconds per 10-page PDF
-	Fully offline, no internet or GPU needed
- Lightweight (≤200MB total dependency size)
  
## Error Handling
●	Errors for <3 or >10 PDFs are handled gracefully
●	Empty or malformed PDFs return fallback-safe structures
●	Logs give detailed feedback if sections can’t be extracted

## Future Enhancements
●	LLM integration for deeper semantic section scoring
●	GUI or web input form
●	Advanced layout parser for academic PDFs

## Team
QWERTY Coders
