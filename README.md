# APU Finder

This Python program is part of a project aimed at organizing the APUs (Unit Price Analysis) published by the Government of Valle del Cauca [here](https://www.valledelcauca.gov.co/documentos/12530/listado-de-precios-gobernacion-2021/) for construction project budgeting. The data provided by them is challenging to work with, as it is in a PDF format that is difficult to export to Excel.

## Project Background

The project focuses on extracting, organizing, and converting the APU data from the PDF files shared by the government into a more manageable format. This process involves data engineering techniques to extract the data, convert it into a usable format (such as numbers), clean the data by removing irrelevant values, and organize it into a structured format for further analysis.

## Usage

1. **Search by APU code:** Enter an APU code (XX-XX-XX) in the corresponding field and click "Search". The program will search for the code in the JSON file and display the APU table if found.

2. **Search by keywords:** Enter keywords in the corresponding field and click "Search". The program will search for the keywords in the descriptions of the APUs and display a list of matches.

3. **Copy to clipboard:** Click "Copy to Clipboard" to copy the selected table to the clipboard in a format compatible with Excel.

## Data Engineering Process

1. **Data Extraction:** The PDF files shared by the government were parsed to extract the APU data.

2. **Data Conversion:** The extracted data was converted into a usable format, such as converting text to numbers where applicable.

3. **Data Cleaning:** Irrelevant values and inconsistencies in the data were removed to ensure the data is clean and usable.

4. **Data Organization:** The cleaned data was organized into a structured format, first into a Pandas DataFrame and then into JSON for easy access and analysis.

## Acknowledgments

I want to thank Siu H. Huang W. for their invaluable help in creating this code.



