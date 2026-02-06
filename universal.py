"""
Universal Metadata Extractor - A cross-platform tool for extracting metadata
from various file types (images, audio, video) with detailed logging.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import exifread
import mutagen
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image, UnidentifiedImageError

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

def setup_logging() -> tuple[logging.Logger, logging.Logger]:
    """
    Configure dual logging system:
    - Process logger: Console output for real-time monitoring
    - Metadata logger: File output for detailed metadata reports
    
    Returns:
        tuple: (process_logger, metadata_logger)
    """
    # Metadata logger (writes to file)
    metadata_handler = logging.FileHandler(
        'metadata_report.log',
        encoding='utf-8',
        mode='w'
    )
    metadata_handler.setFormatter(logging.Formatter('%(message)s'))
    metadata_logger = logging.getLogger('metadata')
    metadata_logger.setLevel(logging.INFO)
    metadata_logger.addHandler(metadata_handler)
    
    # Process logger (console output)
    process_handler = logging.StreamHandler()
    process_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    )
    process_logger = logging.getLogger('process')
    process_logger.setLevel(logging.INFO)
    process_logger.addHandler(process_handler)
    
    return process_logger, metadata_logger


# ============================================================================
# UNIVERSAL METADATA EXTRACTOR
# ============================================================================

class UniversalMetadataExtractor:
    """
    Extracts metadata from various file formats including images, audio, and video.
    Uses specialized libraries for each file type to maximize metadata extraction.
    """
    
    # File type mappings
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.webp', '.heic', '.bmp', '.gif'}
    AUDIO_EXTENSIONS = {'.mp3', '.flac', '.m4a', '.ogg', '.wav', '.aac', '.wma'}
    VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'}
    
    @staticmethod
    def get_image_metadata(file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from image files using exifread.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Dictionary containing image metadata
        """
        metadata = {}
        try:
            with open(file_path, 'rb') as file:
                tags = exifread.process_file(file, details=False)
                for tag, value in tags.items():
                    if tag not in ['JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'JPEGThumbnail']:
                        metadata[f"IMG_{tag}"] = str(value)
        except Exception as e:
            logging.debug(f"Could not extract image metadata from {file_path}: {e}")
        
        return metadata
    
    @staticmethod
    def get_audio_metadata(file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from audio files using mutagen.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary containing audio metadata
        """
        metadata = {}
        try:
            audio = mutagen.File(file_path)
            if audio:
                # Technical metadata
                if hasattr(audio, 'info'):
                    for attr in dir(audio.info):
                        if not attr.startswith('_') and not callable(getattr(audio.info, attr)):
                            value = getattr(audio.info, attr)
                            if value is not None:
                                metadata[f"AUDIO_TECH_{attr}"] = str(value)
                
                # Tag metadata (ID3, Vorbis comments, etc.)
                if audio.tags:
                    for tag in audio.tags:
                        value = audio.tags[tag]
                        if value:
                            metadata[f"AUDIO_TAG_{tag}"] = str(value[0] if isinstance(value, list) else value)
        except Exception as e:
            logging.debug(f"Could not extract audio metadata from {file_path}: {e}")
        
        return metadata
    
    @staticmethod
    def get_video_metadata(file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from video files using hachoir.
        
        Args:
            file_path: Path to the video file
            
        Returns:
            Dictionary containing video metadata
        """
        metadata = {}
        try:
            parser = createParser(str(file_path))
            if parser:
                with parser:
                    extracted = extractMetadata(parser)
                    if extracted:
                        for line in extracted.exportPlaintext():
                            if ":" in line:
                                key, value = line.split(":", 1)
                                metadata[f"VIDEO_{key.strip()}"] = value.strip()
        except Exception as e:
            logging.debug(f"Could not extract video metadata from {file_path}: {e}")
        
        return metadata
    
    @classmethod
    def get_all_metadata(cls, file_path: Path) -> Dict[str, Any]:
        """
        Main method to extract metadata based on file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing all extracted metadata
        """
        all_metadata = {}
        extension = file_path.suffix.lower()
        
        # Image files
        if extension in cls.IMAGE_EXTENSIONS:
            all_metadata.update(cls.get_image_metadata(file_path))
        
        # Audio files
        elif extension in cls.AUDIO_EXTENSIONS:
            all_metadata.update(cls.get_audio_metadata(file_path))
        
        # Video files
        elif extension in cls.VIDEO_EXTENSIONS:
            all_metadata.update(cls.get_video_metadata(file_path))
        
        # Basic file metadata (always included)
        try:
            stat_info = file_path.stat()
            all_metadata.update({
                "FILE_SIZE": f"{stat_info.st_size} bytes",
                "CREATED": str(stat_info.st_ctime),
                "MODIFIED": str(stat_info.st_mtime),
                "FILE_EXTENSION": extension,
            })
        except Exception:
            pass
        
        return all_metadata


# ============================================================================
# FILE MANAGER
# ============================================================================

class FileManager:
    """
    Manages recursive file system traversal and metadata extraction.
    Handles directory exploration and generates comprehensive reports.
    """
    
    def __init__(self, base_folder: str):
        """
        Initialize FileManager with target directory.
        
        Args:
            base_folder: Root directory to scan
        """
        self.base_folder = Path(base_folder).resolve()
        self.ignored_dirs = {'.git', '__pycache__', '.venv', 'node_modules'}
        self.ignored_files = {'.DS_Store', 'Thumbs.db', 'desktop.ini'}
    
    def should_skip(self, path: Path) -> bool:
        """
        Determine if a file or directory should be skipped.
        
        Args:
            path: Path to check
            
        Returns:
            True if should be skipped, False otherwise
        """
        # Skip hidden files and directories
        if any(part.startswith('.') for part in path.parts):
            return True
        
        # Skip ignored directories
        if path.is_dir() and path.name in self.ignored_dirs:
            return True
        
        # Skip ignored files
        if path.is_file() and path.name in self.ignored_files:
            return True
        
        return False
    
    def run(self, process_logger: logging.Logger, metadata_logger: logging.Logger) -> None:
        """
        Main execution method - recursively scans directory and extracts metadata.
        
        Args:
            process_logger: Logger for process information
            metadata_logger: Logger for metadata output
        """
        process_logger.info(f"Starting deep exploration of: {self.base_folder}")
        process_logger.info(f"Metadata report will be saved to: metadata_report.log")
        
        file_count = 0
        supported_files = 0
        
        # Recursive directory walk
        for root, dirs, files in os.walk(self.base_folder, topdown=True):
            current_path = Path(root)
            
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if not self.should_skip(current_path / d)]
            
            # Skip this directory if it should be ignored
            if self.should_skip(current_path):
                continue
            
            relative_path = current_path.relative_to(self.base_folder)
            
            # Log directory header
            if str(relative_path) != '.':
                metadata_logger.info(f"\n{'='*80}")
                metadata_logger.info(f"DIRECTORY: {relative_path}")
                metadata_logger.info(f"{'='*80}")
            
            # Process files in current directory
            for filename in sorted(files):
                file_path = current_path / filename
                file_count += 1
                
                # Skip ignored files
                if self.should_skip(file_path):
                    continue
                
                # Skip the script itself and log files
                if filename == Path(__file__).name or filename.endswith('.log'):
                    continue
                
                # Extract metadata
                metadata = UniversalMetadataExtractor.get_all_metadata(file_path)
                
                # Log file information
                metadata_logger.info(f"\nFILE: {filename}")
                metadata_logger.info(f"PATH: {relative_path / filename}")
                
                if metadata:
                    supported_files += 1
                    metadata_logger.info("METADATA:")
                    for key in sorted(metadata.keys()):
                        value = str(metadata[key])
                        # Truncate very long values
                        if len(value) > 500:
                            value = value[:497] + "..."
                        metadata_logger.info(f"  • {key}: {value}")
                else:
                    metadata_logger.info("  • No extractable metadata found")
        
        # Summary
        process_logger.info(f"\n{'='*60}")
        process_logger.info("SCAN COMPLETE")
        process_logger.info(f"{'='*60}")
        process_logger.info(f"Total files scanned: {file_count}")
        process_logger.info(f"Files with metadata extracted: {supported_files}")
        process_logger.info(f"Metadata report saved to: metadata_report.log")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point for the script."""
    # Setup logging
    process_logger, metadata_logger = setup_logging()
    
    # Get target directory from command line or use current directory
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = "."
    
    try:
        # Validate directory
        target_path = Path(target_dir)
        if not target_path.exists():
            process_logger.error(f"Directory does not exist: {target_dir}")
            sys.exit(1)
        
        if not target_path.is_dir():
            process_logger.error(f"Path is not a directory: {target_dir}")
            sys.exit(1)
        
        # Run metadata extraction
        manager = FileManager(target_dir)
        manager.run(process_logger, metadata_logger)
        
        process_logger.info("\n✅ Process completed successfully!")
        
    except KeyboardInterrupt:
        process_logger.info("\n\n⚠️  Process interrupted by user")
        sys.exit(130)
    except Exception as e:
        process_logger.error(f"\n❌ Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
