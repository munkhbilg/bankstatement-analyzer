import gradio as gr
from main import BankStatementAnalyzer
import os

analyzer = BankStatementAnalyzer()

def analyze_and_save_bank_statement(file):
    """Gradio interface function with file saving"""
    if file is None:
        return "Please upload a file", None, None
    
    try:
        saved_files = analyzer.process_and_save_all(file.name)
        
        result = analyzer.process_statement(file.name)
        
        output_text = f"""
        ## Bank Statement Analysis Results
        
        ### Files Saved:
        - Raw OCR Text: {saved_files['ocr_file']}
        - Structured Data: {saved_files['json_file']}
        - Financial Analysis: {saved_files['analysis_file']}
        - Categorized Transactions: {saved_files['categorized_file']}
        - Complete Analysis: {saved_files['complete_file']}
        
        ### Financial Summary:
        - Total Transactions: {result['financial_analysis']['total_transactions']}
        - Total Spent: ${result['financial_analysis']['spending_insights']['total_spent']:,.2f}
        - Total Earned: ${result['financial_analysis']['spending_insights']['total_earned']:,.2f}
        - Net Cash Flow: ${result['financial_analysis']['spending_insights']['net_flow']:,.2f}
        """
        
        return output_text, saved_files['json_file'], saved_files['ocr_file']
        
    except Exception as e:
        return f"Error processing file: {str(e)}", None, None
iface = gr.Interface(
    fn=analyze_and_save_bank_statement,
    inputs=gr.File(label="Upload Bank Statement (PDF/Image)"),
    outputs=[
        gr.Markdown(label="Analysis Results"),
        gr.File(label="Download JSON"),
        gr.File(label="Download OCR Text")
    ],
    title="AI Bank Statement Analyzer",
    description="Upload your bank statement to get AI-powered financial analysis and download the results"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)