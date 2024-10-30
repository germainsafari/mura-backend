import os
import PyPDF2
from app import db
from models import KnowledgeBase  # A model in your database for storing extracted PDF content

def extract_text_from_pdfs(pdf_directory="data/pdfs/"):
    """Extract text from PDFs and store it in the database."""
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            with open(os.path.join(pdf_directory, filename), "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                for page_num in range(pdf_reader.numPages):
                    page = pdf_reader.getPage(page_num)
                    text = page.extract_text()
                    save_to_database(text, filename, page_num)

def save_to_database(text, document_id, page_number):
    """Save extracted text to the KnowledgeBase table."""
    knowledge_entry = KnowledgeBase(content=text, document_id=document_id, page_number=page_number)
    db.session.add(knowledge_entry)
    db.session.commit()

# Extract and store all PDF data in the database
extract_text_from_pdfs()
