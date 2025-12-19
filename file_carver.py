# forensic_recovery_tool/file_carver.py

import os
from signatures import FILE_SIGNATURES
from utils import log_carving_activity, generate_sha256

# Configuration
UPLOAD_FOLDER = 'forensic_recovery_tool/uploads'
RECOVERED_FOLDER = 'forensic_recovery_tool/recovered_files'

def find_header(data, header):
    """
    Finds the first occurrence of a header in the data.
    Returns the starting index or -1 if not found.
    """
    return data.find(header)

def find_footer(data, footer, start_offset):
    """
    Finds the first occurrence of a footer in the data starting from a given offset.
    Returns the starting index of the footer or -1 if not found.
    """
    # Search only from the start_offset onwards
    # The search is limited to a reasonable size (e.g., 10MB) to prevent excessively long searches
    # For a real forensic tool, this would be more sophisticated.
    search_limit = start_offset + 10 * 1024 * 1024 # 10MB limit
    search_data = data[start_offset:search_limit]
    
    # Find the footer in the limited search data
    relative_index = search_data.find(footer)
    
    if relative_index != -1:
        # Return the absolute index in the original data
        return start_offset + relative_index + len(footer)
    else:
        return -1

def carve_file(data, start, end, file_type, file_index):
    """
    Extracts the file content and saves it to the recovered_files folder.
    Returns the path to the saved file.
    """
    content = data[start:end]
    
    # Ensure the recovered files directory exists
    os.makedirs(RECOVERED_FOLDER, exist_ok=True)
    
    # Create a unique filename
    filename = f"recovered_{file_index}.{file_type}"
    file_path = os.path.join(RECOVERED_FOLDER, filename)
    
    try:
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Generate hash (Optional Enhancement, but good practice)
        file_hash = generate_sha256(file_path)
        
        log_carving_activity(f"Carved file: {filename} (Type: {file_type}, Size: {len(content)} bytes, Hash: {file_hash[:8]}...)")
        
        return {
            "filename": filename,
            "type": file_type,
            "offset": start,
            "size": len(content),
            "hash": file_hash
        }
    except Exception as e:
        log_carving_activity(f"Error saving carved file {filename}: {e}")
        return None

def scan_image(image_path):
    """
    Main function to scan the disk image and perform file carving.
    Returns a list of metadata for all recovered files.
    """
    log_carving_activity(f"Starting scan on image: {image_path}")
    
    recovered_files_metadata = []
    file_index = 1
    
    try:
        with open(image_path, 'rb') as f:
            # Read the entire disk image into memory (for simplicity and small images)
            # For large images, this would need to be chunked.
            disk_image_data = f.read()
    except Exception as e:
        log_carving_activity(f"Error reading disk image {image_path}: {e}")
        return []

    image_size = len(disk_image_data)
    current_offset = 0
    
    # Loop through the data to find headers
    while current_offset < image_size:
        
        # Search for all supported headers from the current offset
        found_header = None
        best_match_offset = -1
        best_match_type = None
        
        # Iterate through all signatures to find the next header
        for file_type, sigs in FILE_SIGNATURES.items():
            header = sigs['header']
            
            # Find the header in the remaining data
            # We search from current_offset to avoid re-scanning the same area
            # The find method on bytes object is efficient
            header_offset = disk_image_data.find(header, current_offset)
            
            if header_offset != -1:
                # Check if this is the earliest header found so far
                if best_match_offset == -1 or header_offset < best_match_offset:
                    best_match_offset = header_offset
                    best_match_type = file_type
                    found_header = header
        
        if best_match_offset != -1:
            # A header was found
            log_carving_activity(f"Found {best_match_type} header at offset: {best_match_offset}")
            
            # Now search for the corresponding footer
            footer = FILE_SIGNATURES[best_match_type]['footer']
            
            # Start searching for the footer immediately after the header
            footer_start_search_offset = best_match_offset + len(found_header)
            footer_end_offset = find_footer(disk_image_data, footer, footer_start_search_offset)
            
            if footer_end_offset != -1:
                # Footer found, carve the file
                log_carving_activity(f"Found {best_match_type} footer at offset: {footer_end_offset}")
                
                # The file content is from the start of the header to the end of the footer
                metadata = carve_file(
                    disk_image_data, 
                    best_match_offset, 
                    footer_end_offset, 
                    best_match_type, 
                    file_index
                )
                
                if metadata:
                    recovered_files_metadata.append(metadata)
                    file_index += 1
                
                # Continue scan from the end of the carved file to avoid re-carving
                current_offset = footer_end_offset
            else:
                # Footer not found, skip this header and continue search from after the header
                log_carving_activity(f"Footer for {best_match_type} not found. Skipping.")
                current_offset = best_match_offset + len(found_header)
        else:
            # No more headers found, end scan
            log_carving_activity("No more file headers found. Scan complete.")
            break
            
    return recovered_files_metadata

# Example usage (for testing purposes)
if __name__ == '__main__':
    # This part is for local testing and will be removed or commented out in the final app.py
    # For now, we will rely on the Flask app to call scan_image.
    pass
