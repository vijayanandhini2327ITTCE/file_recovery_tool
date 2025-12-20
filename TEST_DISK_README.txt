# Test Disk Image

This is a synthetic disk image created for testing the Forensic File Recovery Tool.

## Contents

The disk image contains embedded file signatures that simulate deleted files:

1. **JPEG Image** - Located at offset 0x000186A0
2. **PNG Image** - Located at offset 0x0007A120
3. **PDF Document** - Located at offset 0x000F4240
4. **ZIP Archive** - Located at offset 0x001E8480
5. **GIF Image** - Located at offset 0x002DC6C0
6. **JPEG Image #2** - Located at offset 0x003D0900

## Usage

1. Upload `test_disk.img` to the forensic recovery tool
2. Click "Start Recovery Process"
3. The tool should recover all 6 embedded files

## Expected Results

- 2 JPEG images (recovered_jpg_1.jpg, recovered_jpg_2.jpg)
- 1 PNG image (recovered_png_1.png)
- 1 PDF document (recovered_pdf_1.pdf)
- 1 ZIP archive (recovered_zip_1.zip)
- 1 GIF image (recovered_gif_1.gif)

## Notes

- This is a synthetic image for testing purposes only
- File data is simulated and not actual valid image/document content
- The tool correctly identifies signatures but recovered files may not open in viewers
- This demonstrates the signature-based carving capability
