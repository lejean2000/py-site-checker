# Description

This is a poor man's checker for site changes. It retrieves websites and compares them with a previously saved version. It uses levenshtein distance after stripping all html tags and reports similarity between 0 (no match) and 1 (exact match).

All page versions are kept in pickled objects on disk.

# Requirements 
    pip install "textdistance[extras]"
    pip install beautifulsoup4

# Usage
See __site_checker_example.py__ for exaple usage.