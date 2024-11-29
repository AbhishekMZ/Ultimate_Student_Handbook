import PyPDF2

def analyze_pdf(start_page=11, end_page=22):
    pdf_path = "1. AI 2022 Scheme III Year B.E. Programs.pdf"
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            print(f"Total pages in PDF: {total_pages}")
            
            # Adjust page range
            start_page = max(0, start_page - 1)
            end_page = min(total_pages, end_page)
            
            print(f"\nAnalyzing pages {start_page + 1} to {end_page}")
            print("-" * 50)
            
            # Extract text from specified pages
            for page_num in range(start_page, end_page):
                page = reader.pages[page_num]
                text = page.extract_text()
                print(f"\nPage {page_num + 1}:")
                print("-" * 20)
                print(text)
                print("-" * 50)
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    analyze_pdf()
