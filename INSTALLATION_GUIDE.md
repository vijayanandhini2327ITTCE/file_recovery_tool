# 🎯 INSTALLATION & USAGE GUIDE
## Forensic Deleted File Recovery Tool

---

## 📥 STEP 1: DOWNLOAD THE PROJECT

You now have the complete `forensic_recovery_tool` folder downloaded to your system.

---

## 🔧 STEP 2: INSTALL REQUIREMENTS

Open a terminal/command prompt in the project folder and run:

```bash
# Navigate to project directory
cd forensic_recovery_tool

# Install Python dependencies
pip install -r requirements.txt
```

### Requirements:
- **Python**: 3.8 or higher
- **Flask**: 3.0.0
- **Werkzeug**: 3.0.1

---

## 🧪 STEP 3: CREATE TEST DISK IMAGE (OPTIONAL)

To test the tool before using real disk images:

```bash
python create_test_disk.py
```

This creates `test_disk.img` (10MB) with 6 embedded test files:
- 2 JPEG images
- 1 PNG image
- 1 PDF document
- 1 ZIP archive
- 1 GIF image

**Custom sizes:**
```bash
python create_test_disk.py 50          # 50MB disk
python create_test_disk.py 20 my.img   # 20MB with custom name
```

---

## 🚀 STEP 4: START THE APPLICATION

```bash
python app.py
```

You should see:
```
============================================================
Forensic Deleted File Recovery Tool
Signature-Based File Carving System
============================================================
Supported file types: jpg, png, pdf, zip, gif, docx, mp3, exe
Upload directory: uploads
Recovery directory: recovered_files
============================================================
Starting Flask server...
Access the application at: http://127.0.0.1:5000
============================================================
```

---

## 🌐 STEP 5: ACCESS WEB INTERFACE

Open your web browser and go to:

```
http://127.0.0.1:5000
```

or

```
http://localhost:5000
```

---

## 📤 STEP 6: UPLOAD DISK IMAGE

1. Click **"Choose disk image file"**
2. Select a disk image file:
   - `test_disk.img` (generated in Step 3)
   - Or your own `.img`, `.dsk`, `.dd`, `.raw`, `.bin` file
3. Click **"Start Recovery Process"**
4. Wait for scanning to complete (progress shown in terminal)

---

## 📊 STEP 7: VIEW RESULTS

After processing, you'll see:

### Recovery Summary
- Total files recovered
- Total data size
- File type breakdown

### Results Table
Each recovered file shows:
- **Filename**: Auto-generated (e.g., recovered_jpg_1.jpg)
- **Type**: File type (JPG, PNG, PDF, etc.)
- **Offset**: Location in disk image (hex format)
- **Size**: File size (formatted)
- **SHA-256 Hash**: For integrity verification
- **Download Button**: Click to download the file

---

## ⬇️ STEP 8: DOWNLOAD RECOVERED FILES

Click the **"⬇️ Download"** button next to any file to save it.

All recovered files are also available in:
```
forensic_recovery_tool/recovered_files/
```

---

## 🔄 STEP 9: PROCESS ANOTHER IMAGE

Click **"🔄 Scan Another Image"** to return to the upload page.

Or click **"🗑️ Clear Results"** to delete all recovered files and reset.

---

## 📝 MONITORING & LOGS

### Terminal Output
Watch the terminal where you ran `python app.py` for:
- Scanning progress (e.g., "Scanning progress: 45.3%")
- File recovery notifications
- Any errors or warnings

### Log File
All operations are logged to:
```
forensic_recovery_tool/forensic_recovery.log
```

Example log entries:
```
2024-12-13 10:30:00 - INFO - Starting file carving on: test_disk.img
2024-12-13 10:30:05 - INFO - Recovered: recovered_jpg_1.jpg | Type: jpg | Offset: 100000 | Size: 5.27 KB
2024-12-13 10:30:10 - INFO - File carving completed
2024-12-13 10:30:10 - INFO - Total files recovered: 6
```

---

## 🎯 WHAT TO EXPECT WITH TEST DISK

When you upload `test_disk.img`, you should recover:

| # | File Type | Expected Filename | Approx. Size |
|---|-----------|-------------------|--------------|
| 1 | JPEG | recovered_jpg_1.jpg | ~5 KB |
| 2 | JPEG | recovered_jpg_2.jpg | ~5 KB |
| 3 | PNG | recovered_png_1.png | ~3 KB |
| 4 | PDF | recovered_pdf_1.pdf | ~2 KB |
| 5 | ZIP | recovered_zip_1.zip | ~1.5 KB |
| 6 | GIF | recovered_gif_1.gif | ~800 B |

**Note**: Files from test disk are synthetic and may not open in viewers, but they demonstrate the carving capability.

---

## 🔍 USING WITH REAL DISK IMAGES

### Creating Disk Images

**From Windows:**
```powershell
# Using FTK Imager or similar tools
# Or using dd:
dd if=\\.\PhysicalDrive0 of=disk.img bs=1M
```

**From Linux:**
```bash
# Create image of entire disk
sudo dd if=/dev/sda of=disk.img bs=1M status=progress

# Create image of partition
sudo dd if=/dev/sda1 of=partition.img bs=1M status=progress
```

**From macOS:**
```bash
# Create image of disk
sudo dd if=/dev/disk2 of=disk.img bs=1m
```

### Best Practices

1. **Always work with copies**
   - Never analyze original evidence
   - Create working copy of disk image

2. **Document everything**
   - Note original disk source
   - Record SHA-256 hash of original
   - Save recovery logs

3. **Verify results**
   - Check recovered file hashes
   - Cross-reference with known data
   - Document findings

---

## ⚙️ CONFIGURATION OPTIONS

### Change Upload Size Limit

Edit `app.py`:
```python
MAX_FILE_SIZE = 1000 * 1024 * 1024  # Change to 1GB
```

### Change Server Port

Edit `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change to port 8080
```

### Add New File Types

Edit `signatures.py`:
```python
FILE_SIGNATURES = {
    # ... existing types ...
    "bmp": {
        "header": b'BM',
        "footer": None,
        "extension": ".bmp",
        "description": "Bitmap Image"
    }
}
```

---

## 🐛 TROUBLESHOOTING

### "ModuleNotFoundError: No module named 'flask'"
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### "Address already in use"
**Solution**: Port 5000 is occupied
```python
# Change port in app.py to 5001 or another free port
app.run(port=5001)
```

### "Permission denied" on uploads/recovered_files
**Solution**: Check directory permissions
```bash
chmod 755 uploads recovered_files
```

### "No files recovered" from test disk
**Solution**: 
1. Verify test disk was created: `ls -lh test_disk.img`
2. Check file size is > 0 bytes
3. Review terminal output for errors
4. Check `forensic_recovery.log`

### Browser shows "Connection refused"
**Solution**: Make sure Flask server is running
```bash
python app.py
# Wait for "Running on http://127.0.0.1:5000"
```

---

## 📊 PERFORMANCE TIPS

### For Large Disk Images (>500MB)

1. **Be patient**: Scanning takes time
2. **Monitor progress**: Watch terminal output
3. **Check logs**: Verify scanning is progressing
4. **Sufficient space**: Ensure enough disk space for recovered files

### For Many Files

1. **Results may load slowly**: Large result tables take time
2. **Download individually**: Better than bulk download
3. **Clear results**: After processing to free space

---

## 🔐 SECURITY RECOMMENDATIONS

### For Forensic Use

1. **Isolated Environment**
   - Run on dedicated forensic workstation
   - No network access during analysis
   - Secure storage for results

2. **Evidence Integrity**
   - Hash original images before analysis
   - Maintain chain of custody logs
   - Document all steps

3. **Data Protection**
   - Encrypt recovered files if sensitive
   - Secure deletion when done
   - Follow organizational policies

---

## 📞 GETTING HELP

### Documentation
1. **README.md** - Comprehensive documentation
2. **QUICKSTART.md** - Quick reference guide
3. **PROJECT_SUMMARY.md** - Technical overview
4. **This guide** - Installation & usage

### Debugging
1. Check terminal output
2. Review `forensic_recovery.log`
3. Verify file permissions
4. Test with `test_disk.img` first

---

## ✅ VERIFICATION CHECKLIST

Before reporting issues, verify:

- [ ] Python 3.8+ installed: `python --version`
- [ ] Dependencies installed: `pip list | grep Flask`
- [ ] Server running: See "Running on..." message
- [ ] Browser can access: http://127.0.0.1:5000
- [ ] Directories exist: `uploads/`, `recovered_files/`
- [ ] Test disk created: `test_disk.img` exists
- [ ] Permissions correct: Can read/write in project folder

---

## 🎓 LEARNING RESOURCES

### Understanding the Code

1. **Start with**: `signatures.py` - Simple database
2. **Then read**: `file_carver.py` - Core logic
3. **Finally**: `app.py` - Web integration

### Key Concepts

- **File Signatures**: Unique byte patterns
- **Header/Footer**: Start/end markers of files
- **Carving**: Extracting data based on signatures
- **Forensics**: Evidence-preserving analysis

---

## 🎉 SUCCESS INDICATORS

You'll know it's working when:

✅ Server starts without errors  
✅ Browser loads upload page  
✅ Test disk uploads successfully  
✅ Terminal shows "Scanning progress"  
✅ Results page displays recovered files  
✅ Files download successfully  
✅ Logs show recovery operations  

---

## 🚀 YOU'RE READY!

The Forensic File Recovery Tool is now installed and ready to use.

Start with the test disk, then move to real forensic work!

**Happy File Carving! 🔍**

---

**Need Quick Help?**
- Can't start: Check Python version and dependencies
- No files found: Try test disk first
- Errors: Check forensic_recovery.log
- Questions: Read README.md

**Remember**: This is a forensic tool - use ethically and legally!
