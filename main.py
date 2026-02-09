import os
import json
import io
from datetime import datetime
from typing import Dict, Any
from ocr_processor import OCRProcessor
from ai_agent import FinancialAgent
from financial_analyzer import FinancialAnalyzer
from category_classifier import CategoryClassifier

class BankStatementAnalyzer:
    """
    Main class for processing bank statements, performing OCR, 
    structuring data with AI, and analyzing finances.
    """
    
    def __init__(self):
        """Initialize all processing components."""
        self.ocr_processor = OCRProcessor()
        self.financial_agent = FinancialAgent()
        self.analyzer = FinancialAnalyzer()
        self.classifier = CategoryClassifier()
    
    def process_statement(self, file_path: str) -> Dict[str, Any]:
        """
        Main pipeline for processing bank statements.
        
        Args:
            file_path: Path to the bank statement file (PDF or image)
            
        Returns:
            Dictionary containing all processing results
        """
        # Step 1: OCR Processing
        print("Step 1: Extracting text from bank statement...")
        extracted_text = self.ocr_processor.extract_text(file_path)
        
        # Step 2: Structure data with AI Agent
        print("Step 2: Structuring data...")
        structured_data = self.financial_agent.structure_data(extracted_text)
        
        # Step 3: Financial Analysis
        print("Step 3: Performing financial analysis...")
        analysis_results = self.analyzer.analyze_finances(structured_data)
        
        # Step 4: Categorization
        print("Step 4: Categorizing transactions...")
        categorized_data = self.classifier.categorize_transactions(structured_data)
        
        return {
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "source_file": file_path,
                "total_text_length": len(extracted_text)
            },
            "extracted_text": extracted_text,
            "structured_data": structured_data,
            "financial_analysis": analysis_results,
            "categorized_transactions": categorized_data
        }
    
    def process_and_save_all(self, file_path: str, output_prefix: str = None) -> Dict[str, str]:
        """
        Process bank statement and save all results to files.
        
        Args:
            file_path: Path to the bank statement file
            output_prefix: Prefix for output files (optional)
            
        Returns:
            Dictionary with paths to saved files
        """
        # Generate output filename with timestamp
        if output_prefix is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_prefix = f"bank_analysis_{timestamp}"
        
        print("Step 1: Extracting text from bank statement...")
        extracted_text = self.ocr_processor.extract_text(file_path)
        
        # Save raw OCR text
        ocr_filename = f"{output_prefix}_raw_ocr.txt"
        self._save_text_file(extracted_text, ocr_filename)
        print(f"✓ Raw OCR text saved to: {ocr_filename}")
        
        print("Step 2: Structuring data...")
        structured_data = self.financial_agent.structure_data(extracted_text)
        
        # Save structured JSON data
        json_filename = f"{output_prefix}_structured.json"
        self._save_json_file(structured_data, json_filename)
        print(f"✓ Structured JSON saved to: {json_filename}")
        
        print("Step 3: Performing financial analysis...")
        analysis_results = self.analyzer.analyze_finances(structured_data)
        
        # Save analysis results as JSON
        analysis_filename = f"{output_prefix}_analysis.json"
        self._save_json_file(analysis_results, analysis_filename)
        print(f"✓ Financial analysis saved to: {analysis_filename}")
        
        print("Step 4: Categorizing transactions...")
        categorized_data = self.classifier.categorize_transactions(structured_data)
        
        # Save categorized data
        categorized_filename = f"{output_prefix}_categorized.json"
        self._save_json_file(categorized_data, categorized_filename)
        print(f"✓ Categorized data saved to: {categorized_filename}")
        
        # Save complete combined results
        complete_results = {
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "source_file": file_path,
                "total_text_length": len(extracted_text)
            },
            "raw_ocr_text": extracted_text,
            "structured_data": structured_data,
            "financial_analysis": analysis_results,
            "categorized_transactions": categorized_data
        }
        
        complete_filename = f"{output_prefix}_complete.json"
        self._save_json_file(complete_results, complete_filename, indent=4)
        print(f"✓ Complete analysis saved to: {complete_filename}")
        
        return {
            "ocr_file": ocr_filename,
            "json_file": json_filename,
            "analysis_file": analysis_filename,
            "categorized_file": categorized_filename,
            "complete_file": complete_filename
        }
    
    def _save_json_file(self, data: dict, filename: str, indent: int = 2) -> bool:
        """
        Save data as formatted JSON file.
        
        Args:
            data: Dictionary data to save
            filename: Output filename
            indent: JSON indentation level
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving JSON file {filename}: {e}")
            return False
    
    def _save_text_file(self, text: str, filename: str) -> bool:
        """
        Save raw text to file.
        
        Args:
            text: Text content to save
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            return True
        except Exception as e:
            print(f"Error saving text file {filename}: {e}")
            return False

def main():
    """Main function to run the bank statement analyzer."""
    analyzer = BankStatementAnalyzer()
    
    print("=== Mongolian Bank Statement Analyzer ===")
    print("This tool processes bank statements and generates structured analysis.")
    
    file_path = input("Enter the path to your bank statement (PDF or image): ").strip()
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return
    
    try:
        # Process and save all results
        saved_files = analyzer.process_and_save_all(file_path)
        
        print("\n" + "="*50)
        print("PROCESSING COMPLETED SUCCESSFULLY!")
        print("="*50)
        print("\nGenerated files:")
        for file_type, file_path in saved_files.items():
            print(f"  - {file_type}: {file_path}")
        
        print("\nGenerating summary...")
        result = analyzer.process_statement(file_path)
        
        # Display financial summary
        financial_analysis = result['financial_analysis']
        spending = financial_analysis['spending_insights']
        
        print(f"\nFINANCIAL SUMMARY:")
        print(f"  Total Transactions: {financial_analysis['total_transactions']}")
        print(f"  Total Spent: ${spending['total_spent']:,.2f}")
        print(f"  Total Earned: ${spending['total_earned']:,.2f}")
        print(f"  Net Cash Flow: ${spending['net_flow']:,.2f}")
        
        if financial_analysis['top_categories']:
            print(f"\nSPENDING BY CATEGORY:")
            for category, amount in financial_analysis['top_categories'].items():
                print(f"  - {category}: ${amount:,.2f}")
        
    except Exception as e:
        print(f"\nError during processing: {e}")
        print("Please check if all dependencies are installed and the file format is supported.")

if __name__ == "__main__":
    main()