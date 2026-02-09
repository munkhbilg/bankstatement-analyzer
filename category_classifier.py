import google.generativeai as genai
import os
from typing import List, Dict, Any

class CategoryClassifier:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def categorize_transactions(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """Categorize transactions using LLM"""
        
        transactions = structured_data.get('transactions', [])
        
        prompt = f"""
        Categorize the following bank transactions into these categories:
        - Income (salary, deposits, transfers in)
        - Food & Dining (restaurants, cafes, groceries)
        - Transportation (fuel, taxi, public transport)
        - Entertainment (movies, concerts, hobbies)
        - Utilities (electricity, water, internet)
        - Shopping (clothing, electronics, general shopping)
        - Loan (loan payments, credit card payments)
        - Housing (rent, mortgage)
        - Healthcare (medical expenses, pharmacy)
        - Other (uncategorized)
        
        Transactions to categorize:
        {transactions}
        
        Return JSON format with categorized transactions.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_categorization_response(response.text)
        except Exception as e:
            print(f"LLM categorization failed: {e}")
            return self._basic_categorization(transactions)
    
    def _parse_categorization_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response for categorization"""
        return {"categorized_transactions": [], "raw_response": response_text}
    
    def _basic_categorization(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Basic rule-based categorization fallback"""
        categorized = []
        for transaction in transactions:
            desc = transaction.get('description', '').lower()
            category = self._categorize_by_keywords(desc)
            categorized.append({
                **transaction,
                "category": category
            })
        
        return {"categorized_transactions": categorized}
    
    def _categorize_by_keywords(self, description: str) -> str:
        """Basic keyword-based categorization"""
        food_keywords = ['restaurant', 'cafe', 'food', 'grocery']
        transport_keywords = ['fuel', 'taxi', 'bus', 'transport']
        
        if any(keyword in description for keyword in food_keywords):
            return "Food & Dining"
        elif any(keyword in description for keyword in transport_keywords):
            return "Transportation"
        
        return "Other"