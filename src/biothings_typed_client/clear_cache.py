#!/usr/bin/env python3
"""
Helper script to clear BioThings client cache files.

Run this script if you encounter HTTP 400 errors that might be caused by corrupted cache files.
"""

import os
import sys
from pathlib import Path
import typer
from typing import Optional

def clear_cache_files(cache_dir: Path | str | None = None):
    """Clear all BioThings client cache files in the specified directory.
    
    Args:
        cache_dir: Directory path to search for cache files. 
                  Defaults to current working directory if None.
    """
    cache_files = [
        "mychem_cache",
        "mygene_cache", 
        "myvariant_cache",
        "mygeneset_cache",
        "mytaxon_cache"
    ]
    
    if cache_dir is None:
        target_dir = Path.cwd()
    else:
        target_dir = Path(cache_dir)
    
    removed_files = []
    
    for cache_file in cache_files:
        cache_path = target_dir / cache_file
        if cache_path.exists():
            try:
                cache_path.unlink()
                removed_files.append(cache_file)
                print(f"✓ Removed {cache_file}")
            except Exception as e:
                print(f"✗ Failed to remove {cache_file}: {e}")
        else:
            print(f"- {cache_file} not found")
    
    if removed_files:
        print(f"\nSuccessfully removed {len(removed_files)} cache file(s).")
        print("You can now try running your code again.")
    else:
        print("\nNo cache files found to remove.")

app = typer.Typer(help="Clear BioThings client cache files")

@app.command()
def clear(
    cache_dir: Optional[str] = typer.Argument(
        None, 
        help="Directory path to search for cache files. Defaults to current working directory."
    )
):
    """Clear BioThings client cache files.
    
    Run this script if you encounter HTTP 400 errors that might be caused by corrupted cache files.
    This will remove cache files like mychem_cache, mygene_cache, myvariant_cache, etc.
    """
    print("BioThings Client Cache Cleaner")
    print("=" * 30)
    
    if cache_dir:
        print(f"Searching for cache files in: {cache_dir}")
        clear_cache_files(cache_dir)
    else:
        print(f"Searching for cache files in: {Path.cwd()}")
        clear_cache_files()

def main():
    """Main entry point for the clear-cache script."""
    app()

if __name__ == "__main__":
    main() 