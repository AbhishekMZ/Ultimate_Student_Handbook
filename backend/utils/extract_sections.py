import os
import csv
from PyPDF2 import PdfReader, PdfWriter

def extract_pages(input_pdf_path, output_pdf_path, start_page, end_page):
    try:
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        # Adjust for 0-based indexing
        start_page = int(start_page) - 1
        end_page = int(end_page)

        # Validate page range
        if start_page < 0 or end_page > len(reader.pages):
            print(f"Invalid page range for {input_pdf_path}: {start_page+1}-{end_page}")
            return False

        # Add specified pages to the writer
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])

        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

        # Write the output PDF
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"Successfully created: {output_pdf_path}")
        return True
    except Exception as e:
        print(f"Error processing {input_pdf_path}: {str(e)}")
        return False

def get_pdf_filename(textbook_id):
    # Map textbook IDs to actual PDF filenames
    pdf_mapping = {
        'DBMS_TB1': 'Fundamentals_of_Database_Systems_6th_Edition-1.pdf',
        'DBMS_TB2': 'Fundamentals_of_Database_Systems_6th_Edition-1.pdf',
        'AISE_TB1': 'softwareEngineeringSomerville.pdf',
        'AISE_TB2': 'softwareEngineeringSomerville.pdf',
        'MLOPS_TB1': 'oreilly-ml-ops.pdf',
        'MLOPS_TB2': 'oreilly-ml-ops.pdf',
        'ANN_TB1': 'deep_learning_goodfellow.pdf',
        'PME_TB1': 'principles_of_management.pdf',
        'PME_TB2': 'principles_of_economics.pdf',
        'PME_TB3': 'Microeconomics2e-OP.pdf'
    }
    filename = pdf_mapping.get(textbook_id)
    if filename:
        return os.path.join('textbooks', filename)
    return None

def main():
    # Create sections directory
    sections_dir = 'textbook_sections'
    os.makedirs(sections_dir, exist_ok=True)

    # Ensure textbooks directory exists
    textbooks_dir = 'textbooks'
    if not os.path.exists(textbooks_dir):
        print(f"Error: {textbooks_dir} directory not found. Please create it and add the required PDF files.")
        return

    # Read the mapping file
    with open('topic_book_mapping.csv', 'r') as mapping_file:
        reader = csv.DictReader(mapping_file)
        
        for row in reader:
            topic_id = row['TopicID']
            textbook_id = row['TextbookID']
            page_range = row['PageNumbers'].split('-')
            
            if len(page_range) != 2:
                print(f"Invalid page range for {topic_id}: {row['PageNumbers']}")
                continue

            # Get the input PDF filename
            input_pdf = get_pdf_filename(textbook_id)
            if not input_pdf:
                print(f"No PDF mapping found for textbook ID: {textbook_id}")
                continue

            if not os.path.exists(input_pdf):
                print(f"PDF file not found: {input_pdf}")
                continue

            # Create output PDF path
            output_pdf = os.path.join(sections_dir, f"{topic_id}.pdf")
            
            # Extract the pages
            success = extract_pages(input_pdf, output_pdf, page_range[0], page_range[1])
            
            if success:
                print(f"Successfully processed {topic_id}")
            else:
                print(f"Failed to process {topic_id}")

if __name__ == "__main__":
    main()
