Certainly! Below is a template for a README file that explains the functionality of the `extract_word_files_from_msg` and `extract_data_from_img` functions:

---

# Document Extraction Functions

## Introduction

This repository contains Python functions for extracting data from email message files (`*.msg`) and images.

## Functions

### 1. extract_word_files_from_msg

#### Description

This function extracts Word files (`*.docx`) embedded in email message files (`*.msg`) and saves them to a specified output folder. Additionally, it removes the processed `.msg` files if a corresponding `.docx` file is successfully extracted.

#### Usage

```python
extract_word_files_from_msg(input_folder, output_folder)
```

- `input_folder`: Path to the folder containing email message files (`*.msg`).
- `output_folder`: Path to the folder where extracted Word files (`*.docx`) will be saved.

### 2. extract_data_from_img

#### Description

This function extracts data (such as PAN, TAN, and CIN numbers) from images using Optical Character Recognition (OCR) techniques. It processes images in a specified directory, extracts relevant information, and saves it to an Excel file.

#### Usage

```python
extract_data_from_img(directory, doc_file_path)
```

- `directory`: Path to the directory containing images.
- `doc_file_path`: Path to the Word file associated with the extracted data.

## Dependencies

- Python 3.x
- Required Python packages (e.g., `extract_msg`, `PIL`, `pandas`)

## Installation

1. Clone this repository to your local machine:

   ```bash
  git@github.com:sharma-vishal006/data_scraping.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Example Usage

```python
from document_extraction import extract_word_files_from_msg, extract_data_from_img

# Example usage of extract_word_files_from_msg function
input_folder = "/path/to/msg_files"
output_folder = "/path/to/extracted_docs"
extract_word_files_from_msg(input_folder, output_folder)

# Example usage of extract_data_from_img function
img_directory = "/path/to/images"
doc_file_path = "/path/to/associated_word_file.docx"
extract_data_from_img(img_directory, doc_file_path)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

- git@github.com:sharma-vishal006/data_scraping.git
- Vishal Sharma

## Issues

Please report any issues or bugs [here](https://github.com/yourusername/document-extraction/issues).

---
Adjust the paths, dependencies, and contributors according to your specific project details.
