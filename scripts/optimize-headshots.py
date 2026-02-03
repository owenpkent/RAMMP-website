#!/usr/bin/env python3
"""
Optimize headshot images for web use.
Resizes to max 400x400px and compresses to JPEG format.
Target size: ~50-150KB per image.
"""

import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow")
    from PIL import Image

HEADSHOTS_DIR = Path(__file__).parent.parent / "assets" / "images" / "headshots"
MAX_SIZE = (400, 400)  # Max dimensions for headshots
JPEG_QUALITY = 85  # Good balance of quality and file size


def optimize_image(input_path: Path) -> None:
    """Optimize a single image file."""
    print(f"Processing: {input_path.name}")
    
    # Get original size
    original_size = input_path.stat().st_size / 1024  # KB
    
    # Open and convert image
    with Image.open(input_path) as img:
        # Convert to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Resize if larger than max size (maintain aspect ratio)
        img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
        
        # Create output filename (always .jpg for consistency)
        output_path = input_path.with_suffix('.jpg')
        
        # Save optimized image
        img.save(output_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
    
    # Get new size
    new_size = output_path.stat().st_size / 1024  # KB
    
    # Delete original if it was a different format
    if input_path.suffix.lower() != '.jpg' and input_path.exists():
        input_path.unlink()
        print(f"  Deleted original: {input_path.name}")
    
    reduction = ((original_size - new_size) / original_size) * 100
    print(f"  {original_size:.1f}KB -> {new_size:.1f}KB ({reduction:.1f}% reduction)")


def main():
    print(f"Optimizing headshots in: {HEADSHOTS_DIR}\n")
    
    if not HEADSHOTS_DIR.exists():
        print(f"Error: Directory not found: {HEADSHOTS_DIR}")
        return
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    images = [f for f in HEADSHOTS_DIR.iterdir() 
              if f.suffix.lower() in image_extensions]
    
    if not images:
        print("No images found to optimize.")
        return
    
    print(f"Found {len(images)} images to optimize.\n")
    
    total_original = 0
    total_new = 0
    
    for img_path in sorted(images):
        original_size = img_path.stat().st_size
        total_original += original_size
        
        optimize_image(img_path)
        
        # Get new file (might have different extension now)
        new_path = img_path.with_suffix('.jpg')
        if new_path.exists():
            total_new += new_path.stat().st_size
    
    print(f"\n{'='*50}")
    print(f"Total: {total_original/1024/1024:.2f}MB -> {total_new/1024/1024:.2f}MB")
    print(f"Overall reduction: {((total_original-total_new)/total_original)*100:.1f}%")
    print("Done!")


if __name__ == "__main__":
    main()
