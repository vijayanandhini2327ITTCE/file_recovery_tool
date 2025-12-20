# 🚀 Quick Start Guide

## Forensic Deleted File Recovery Tool

### ⚡ 3-Minute Setup

#### Step 1: Install Dependencies
```bash
cd forensic_recovery_tool
pip install -r requirements.txt
```

#### Step 2: Create Test Disk Image (Optional)
```bash
python create_test_disk.py
```
This creates a 10MB test disk image with 6 embedded files for testing.

#### Step 3: Start the Application
```bash
python app.py
```

#### Step 4: Open Browser
Navigate to: **http://127.0.0.1:5000**

#### Step 5: Upload & Recover
1. Click "Choose disk image file"
2. Select `test_disk.img` (or your own disk image)
3. Click "Start Recovery Process"
4. View and download recovered files!

---

## 📁 What's Inside?

```
forensic_recovery_tool/
├── 🎯 app.py                    # Main Flask application
├── 🔧 file_carver.py            # File carving engine
├── 🔑 signatures.py             # File signature database
├── 🛠️  utils.py                  # Helper functions
├── 📤 uploads/                  # Temporary upload storage
├── 📥 recovered_files/          # Recovered files output
├── 🎨 templates/                # HTML templates
│   ├── index.html              # Upload interface
│   └── results.html            # Results display
├── 💅 static/style.css          # Styling
├── 🧪 create_test_disk.py       # Test image generator
└── 📋 requirements.txt          # Python dependencies
```

---

## 🎯 Supported File Types

✅ **Images**: JPG, PNG, GIF  
✅ **Documents**: PDF, DOCX  
✅ **Archives**: ZIP  
✅ **Audio**: MP3  
✅ **Executables**: EXE  

---

## 🔍 How It Works

1. **Upload** → Disk image file (.img, .dsk, .dd)
2. **Scan** → Search for file signatures (headers/footers)
3. **Carve** → Extract byte sequences between signatures
4. **Recover** → Save files with metadata (offset, size, hash)
5. **Download** → Get individual recovered files

---

## 💡 Usage Tips

### For Testing
```bash
# Generate test disk with default settings (10MB)
python create_test_disk.py

# Generate larger test disk (50MB)
python create_test_disk.py 50

# Custom filename
python create_test_disk.py 20 my_test.img
```

### For Real Forensics
1. Use **read-only** disk images
2. Create working copies before analysis
3. Document all findings
4. Verify recovered files with SHA-256 hashes

---

## 🐛 Troubleshooting

**Problem**: "No files recovered"
- ✅ Check if disk image contains deleted files
- ✅ Verify file types are supported
- ✅ Try the test disk image first

**Problem**: Import errors
- ✅ Run: `pip install -r requirements.txt`
- ✅ Check Python version (3.8+)

**Problem**: Permission denied
- ✅ Check directory permissions
- ✅ Run with appropriate privileges

**Problem**: Port already in use
- ✅ Change port in app.py: `app.run(port=5001)`

---

## 📊 Example Output

After recovery, you'll see:

```
Recovered Files Summary:
• Total Files: 6
• JPEG: 2 files
• PNG: 1 file
• PDF: 1 file
• ZIP: 1 file
• GIF: 1 file

Each file includes:
✓ Filename (auto-generated)
✓ File type and description
✓ Byte offset in disk image
✓ File size (bytes & formatted)
✓ SHA-256 hash for verification
✓ Download link
```

---

## 🔐 Security Notes

- ✅ Read-only disk analysis
- ✅ Original image never modified
- ✅ Secure filename handling
- ✅ File type validation
- ✅ Size limits enforced

---

## 📝 Logging

All operations logged to: `forensic_recovery.log`

Example log entries:
```
2024-12-13 10:30:00 - INFO - Starting file carving on: test_disk.img
2024-12-13 10:30:05 - INFO - Recovered: recovered_jpg_1.jpg | Type: jpg | ...
2024-12-13 10:30:10 - INFO - File carving completed
2024-12-13 10:30:10 - INFO - Total files recovered: 6
```

---

## 🎓 Educational Use Cases

✅ Digital Forensics Training  
✅ Data Recovery Education  
✅ Cybersecurity Labs  
✅ File System Research  
✅ Evidence Analysis Practice  

---

## ⚠️ Legal & Ethical Use

**✅ Authorized Use:**
- Personal data recovery
- Authorized forensic investigations
- Educational purposes
- Research projects

**❌ Prohibited Use:**
- Unauthorized access
- Privacy violations
- Illegal activities

---

## 🆘 Need Help?

1. Check `README.md` for detailed documentation
2. Review `forensic_recovery.log` for errors
3. Test with `test_disk.img` first
4. Verify all dependencies installed

---

## 🚀 Advanced Usage

### Custom Signatures

Edit `signatures.py` to add new file types:

```python
FILE_SIGNATURES = {
    "your_type": {
        "header": b'\x00\x00',      # Header bytes
        "footer": b'\xFF\xFF',      # Footer bytes
        "extension": ".ext",
        "description": "Your File Type"
    }
}
```

### Batch Processing

```python
from file_carver import carve_files

images = ['disk1.img', 'disk2.img', 'disk3.img']

for image in images:
    print(f"Processing {image}...")
    results = carve_files(image, f'output_{image}')
    print(f"Recovered {len(results)} files")
```

---

## 📈 Performance

| Disk Size | Scan Time* | Expected Results |
|-----------|------------|------------------|
| 10 MB     | ~5 seconds | Fast |
| 100 MB    | ~30 seconds | Good |
| 500 MB    | ~2 minutes | Acceptable |
| 1 GB+     | ~5+ minutes | Requires patience |

*Times vary based on CPU and disk I/O

---

## ✅ Verification Checklist

Before using for actual forensics:

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Tested with `test_disk.img`
- [ ] Verified recovered files
- [ ] Reviewed logging output
- [ ] Understood limitations
- [ ] Read legal/ethical guidelines

---

**Ready to start? Run:**
```bash
python app.py
```

**Then visit:** http://127.0.0.1:5000

🎉 **Happy File Carving!**
