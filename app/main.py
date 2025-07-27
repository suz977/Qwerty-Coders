import fitz  # PyMuPDF
import json
import re
import time
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_sections_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    for i, page in enumerate(doc):
        blocks = page.get_text("blocks")
        for b in blocks:
            text = b[4].strip()
            if len(text) > 10 and re.match(r'^[A-Z].{5,}', text):
                sections.append({
                    "page": i + 1,
                    "title": text,
                    "text": text,
                })
    return sections


def rank_sections(sections, job_to_be_done):
    corpus = [s['text'] for s in sections] + [job_to_be_done]
    vectorizer = TfidfVectorizer(stop_words='english').fit_transform(corpus)
    scores = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()

    ranked_sections = sorted(zip(sections, scores), key=lambda x: -x[1])
    top_sections = []
    for rank, (sec, score) in enumerate(ranked_sections[:5], start=1):
        sec["importance_rank"] = rank
        top_sections.append(sec)
    return top_sections


def extract_subsections(section_text, job_to_be_done):
    paras = section_text.split("\n")
    paras = [p.strip() for p in paras if len(p.strip()) > 20]

    if not paras:
        return []

    corpus = paras + [job_to_be_done]
    vectorizer = TfidfVectorizer(stop_words='english').fit_transform(corpus)

    if vectorizer.shape[0] <= 1:
        return []

    scores = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()
    ranked = sorted(zip(paras, scores), key=lambda x: -x[1])
    return [r[0] for r in ranked[:3]]


def build_output_json(pdf_paths, persona, job_to_be_done):
    start_time = time.time()
    extracted_sections = []
    refined_subsections = []

    for pdf_path in pdf_paths:
        sections = extract_sections_from_pdf(pdf_path)
        top_sections = rank_sections(sections, job_to_be_done)

        for sec in top_sections:
            extracted_sections.append({
                "document": Path(pdf_path).name,
                "page_number": sec["page"],
                "section_title": sec["title"],
                "importance_rank": sec["importance_rank"]
            })
            sub_texts = extract_subsections(sec["text"], job_to_be_done)
            for t in sub_texts:
                refined_subsections.append({
                    "document": Path(pdf_path).name,
                    "refined_text": t,
                    "page_number": sec["page"]
                })

    output = {
        "metadata": {
            "input_documents": [Path(p).name for p in pdf_paths],
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": refined_subsections
    }
    print("Total time:", round(time.time() - start_time, 2), "seconds")
    return output


if __name__ == "__main__":
    pdf_folder = "input_pdfs"  # This will look for input_pdfs in current directory
    pdf_files = list(Path(pdf_folder).glob("*.pdf"))

    if not (3 <= len(pdf_files) <= 10):
        print(f"❌ Found {len(pdf_files)} PDF(s). Please ensure there are between 3 and 10 PDF files in the '{pdf_folder}' directory.")
        exit(1)

    persona = input("Enter the persona (e.g., 'PhD Researcher in Computational Biology'): ")
    job = input("Enter the job to be done (e.g., 'Prepare a literature review on...'): ")

    result = build_output_json([str(p) for p in pdf_files], persona, job)

    with open("output.json", "w") as f:
        json.dump(result, f, indent=2)

    print("✅ Output written to output.json")