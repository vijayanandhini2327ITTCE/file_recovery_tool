# Forensic Deleted File Recovery Tool

## 🔍 Overview

A web-based forensic tool that uses **signature-based file carving** to recover deleted files from disk images. This tool analyzes raw disk images and reconstructs files by identifying their unique header and footer signatures.

## 🎯 Features

- **Signature-Based Carving**: Identifies files by their binary signatures (headers/footers)
- **Multiple File Type Support**: Recovers JPG, PNG, PDF, ZIP, GIF, DOCX, MP3, EXE files
- **Web-Based Interface**: Easy-to-use browser interface
- **Forensic Integrity**: Read-only analysis, preserves original evidence
- **Detailed Metadata**: Provides offset, size, and SHA-256 hash for each recovered file
- **Progress Tracking**: Real-time scanning progress updates

## 📋 Supported File Types

| File Type | Extension | Description |
|-----------|-----------|-------------|
| JPG | .jpg | JPEG Images |
| PNG | .png | PNG Images |
| PDF | .pdf | PDF Documents |
| ZIP | .zip | ZIP Archives |
| GIF | .gif | GIF Images |
| DOCX | .docx | Word Documents |
| MP3 | .mp3 | MP3 Audio Files |
| EXE | .exe | Windows Executables |

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd forensic_recovery_tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify directory structure**
   ```
   forensic_recovery_tool/
   ├── app.py
   ├── file_carver.py
   ├── signatures.py
   ├── utils.py
   ├── uploads/
   ├── recovered_files/
   ├── templates/
   │   ├── index.html
   │   └── results.html
   ├── static/
   │   └── style.css
   └── requirements.txt
   ```

## 🎮 Usage

### Starting the Application

1. **Run the Flask server**
   ```bash
   python app.py
   ```

2. **Access the web interface**
   - Open browser and navigate to: `http://127.0.0.1:5000`

3. **Upload a disk image**
   - Click "Choose disk image file"
   - Select a disk image (.img, .dsk, .dd, .raw, .bin)
   - Click "Start Recovery Process"

4. **View results**
   - Wait for scanning to complete
   - Review recovered files and metadata
   - Download individual files

### Command-Line Usage (Optional)

```python
from file_carver import carve_files

# Carve files from disk image
recovered_files = carve_files('path/to/disk_image.img', 'output_directory')

# Print results
for file in recovered_files:
    print(f"Recovered: {file['filename']} at offset {file['offset']}")
```

## 🔧 Technical Details

### File Carving Process

1. **Binary Scanning**: Reads disk image byte-by-byte
2. **Header Detection**: Searches for file signature headers
3. **Footer Matching**: Locates corresponding footer signatures
4. **Data Extraction**: Extracts byte sequences between header/footer
5. **File Reconstruction**: Saves recovered data as individual files
6. **Hash Calculation**: Generates SHA-256 hash for integrity verification

### Signature Database

File signatures are defined in `signatures.py`:

```python
FILE_SIGNATURES = {
    "jpg": {
        "header": b'\xff\xd8\xff',
        "footer": b'\xff\xd9'
    },
    "png": {
        "header": b'\x89PNG\r\n\x1a\n',
        "footer": b'IEND\xaeB`\x82'
    },
    # ... more signatures
}
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Upload page |
| `/upload` | POST | Upload disk image |
| `/results` | GET | Display recovered files |
| `/download/<filename>` | GET | Download recovered file |
| `/api/status` | GET | Check system status |
| `/clear` | GET | Clear all results |

## 📊 Output Format

### Recovered File Metadata

```json
{
  "filename": "recovered_jpg_1.jpg",
  "type": "jpg",
  "description": "JPEG Image",
  "offset": 102345,
  "size": 24576,
  "size_formatted": "24.00 KB",
  "hash": "abc123...",
  "path": "/path/to/recovered_files/recovered_jpg_1.jpg"
}
```

## 🛡️ Forensic Considerations

### Best Practices

1. **Evidence Preservation**
   - Original disk image is never modified
   - All operations are read-only
   - Chain of custody maintained

2. **Documentation**
   - All operations logged to `forensic_recovery.log`
   - Byte offsets preserved for court admissibility
   - SHA-256 hashes for integrity verification

3. **Limitations**
   - Only recovers files with intact headers/footers
   - Fragmented files may not be fully recovered
   - Overwritten data cannot be recovered

## 🧪 Testing

### Creating a Test Disk Image

```bash
# Create a test disk image
dd if=/dev/zero of=test_disk.img bs=1M count=100

# Add some files to it
# (You can use forensic tools or create a filesystem)
```

### Validation

The tool includes automatic validation:
- File size checks
- Extension validation
- Integrity verification

## 🔒 Security Notes

- **File Size Limits**: Maximum upload size is 500MB (configurable)
- **Allowed Extensions**: Only .img, .dsk, .dd, .raw, .bin accepted
- **Secure Filenames**: Uses `secure_filename()` to prevent path traversal
- **Temporary Storage**: Uploaded files can be automatically cleaned

## 🐛 Troubleshooting

### Common Issues

1. **"No files recovered"**
   - Disk image may not contain deleted files
   - Files may be overwritten or fragmented
   - File types may not be in signature database

2. **"Invalid disk image"**
   - Check file format (.img, .dsk, .dd)
   - Verify file is not corrupted
   - Ensure file size > 0 bytes

3. **Server errors**
   - Check Python version (3.8+)
   - Verify all dependencies installed
   - Check directory permissions

## 📝 Logging

All operations are logged to `forensic_recovery.log`:

```
2024-12-13 10:30:00 - INFO - Starting file carving on: disk_image.img
2024-12-13 10:30:15 - INFO - Recovered: recovered_jpg_1.jpg | Type: jpg | Offset: 102345 | Size: 24.00 KB
2024-12-13 10:35:00 - INFO - File carving completed
2024-12-13 10:35:00 - INFO - Total files recovered: 15
```

## 🔧 Configuration

### Customization Options

Edit `app.py` to modify:

```python
# Maximum upload size
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

# Allowed file extensions
ALLOWED_EXTENSIONS = {'img', 'dsk', 'dd', 'raw', 'bin'}

# Directories
UPLOAD_FOLDER = 'uploads'
RECOVERED_FOLDER = 'recovered_files'
```

### Adding New File Types

Edit `signatures.py`:

```python
FILE_SIGNATURES = {
    "new_type": {
        "header": b'\x00\x00\x00\x00',  # Your header bytes
        "footer": b'\xFF\xFF\xFF\xFF',  # Your footer bytes
        "extension": ".ext",
        "description": "File Description"
    }
}
```

## 📚 Architecture

### Component Overview

- **app.py**: Flask web application and routing
- **file_carver.py**: Core carving algorithms
- **signatures.py**: File signature database
- **utils.py**: Helper functions (hashing, logging)
- **templates/**: HTML user interface
- **static/**: CSS styling

### Data Flow

```
User Upload → Validation → Binary Scanning → Signature Detection → 
File Extraction → Hash Calculation → Results Display → File Download
```

## 🤝 Contributing

To add new features or file types:

1. Add signatures to `signatures.py`
2. Update file carving logic if needed
3. Test with sample disk images
4. Update documentation

## 📄 License

This is a forensic educational tool. Use responsibly and ethically.

## ⚠️ Disclaimer

This tool is for:
- Digital forensics education
- Authorized investigations
- Data recovery purposes

**Do not use for:**
- Unauthorized access to systems
- Privacy violations
- Illegal activities

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review log files (`forensic_recovery.log`)
3. Verify disk image integrity

## 📈 Future Enhancements

Potential improvements:
- [ ] Support for more file types
- [ ] Advanced fragment reassembly
- [ ] Progress bar with percentage
- [ ] Parallel processing for large images
- [ ] File preview functionality
- [ ] Export results to CSV/JSON
- [ ] Integration with forensic frameworks

---

**Version**: 1.0  
**Last Updated**: December 2024  
**Status**: Production Ready
