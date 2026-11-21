from pyflow.utils import extract_and_process_archive

if __name__ == "__main__":
    print("--- Compressed File Processing Test ---")
    
    # Kisi sample zip file ka path yahan de sakta hai (e.g., 'data/dataset.zip')
    archive_path = "D:\\tutedude\\Python_Project_t\\PyFlow_Assignment_2\\data\\archive.zip" 
    
    try:
        files = extract_and_process_archive(archive_path, extract_to="data/raw_extracted")
        
        print("\n[SUCCESS] Archive Extracted Successfully:")
        print(f" -> Total Files Extracted : {len(files)}")
        for f in files:
            print(f"    - {f}")
            
    except Exception as e:
        print(f"[ERROR] {e}")