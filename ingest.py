from langchain_community.document_loaders import PyPDFLoader

PDF_PATH ="data/diabetes_guideline.pdf"  #path to our medical pdf

# this creates loader object 
loader = PyPDFLoader(PDF_PATH) 

#load Pdf pages in docs
docs = loader.load() 

# Print total pages loaded
print(f"Total pages loaded: {len(docs)}")

# Print sample content from first page
print("\n--- FIRST PAGE CONTENT ---\n")

print(docs[0].page_content)

# Print metadata
print("\n--- METADATA ---\n")

print(docs[0].metadata)

