from typing import Dict, Any, List
import json
import re

class FinancialAnalyzer:
    def __init__(self):
        self.categories = {
            "income": ["цалин", "хуримтлал", "salary", "deposit"],
            "food": ["ресторан", "кафе", "хоол", "хүнсний дэлгүүр", "restaurant", "grocery"],
            "transport": ["бензин", "такси", "автобус", "тээвэр"],
            "loan": ["зээл", "зээлийн эргэн төлөлт", "loan", "credit"]
        }
    
    def analyze_finances(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform financial analysis with proper type handling"""
        
        transactions = structured_data.get('transactions', [])
        
        # Convert amount strings to floats
        processed_transactions = self._process_transaction_amounts(transactions)
        
        analysis = {
            "total_transactions": len(processed_transactions),
            "spending_insights": self._get_spending_insights(processed_transactions),
            "monthly_summary": self._get_monthly_summary(processed_transactions),
            "top_categories": self._categorize_spending(processed_transactions),
            "cash_flow_analysis": self._analyze_cash_flow(processed_transactions)
        }
        
        return analysis
    
    def _process_transaction_amounts(self, transactions: List[Dict]) -> List[Dict]:
        """Convert transaction amount strings to floats"""
        processed = []
        
        for transaction in transactions:
            processed_transaction = transaction.copy()
            
            # Handle amount conversion
            if 'amount' in processed_transaction:
                amount = processed_transaction['amount']
                if isinstance(amount, str):
                    # Remove currency symbols and commas, then convert to float
                    cleaned_amount = re.sub(r'[^\d.-]', '', amount)
                    try:
                        processed_transaction['amount'] = float(cleaned_amount)
                    except (ValueError, TypeError):
                        processed_transaction['amount'] = 0.0
                elif not isinstance(amount, (int, float)):
                    processed_transaction['amount'] = 0.0
            
            processed.append(processed_transaction)
        
        return processed
    
    def _get_spending_insights(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Generate spending insights with type-safe comparisons"""
        try:
            withdrawals = [t for t in transactions if self._get_numeric_amount(t) < 0]
            deposits = [t for t in transactions if self._get_numeric_amount(t) > 0]
            
            total_spent = abs(sum(self._get_numeric_amount(t) for t in withdrawals))
            total_earned = sum(self._get_numeric_amount(t) for t in deposits)
            
            return {
                "total_spent": total_spent,
                "total_earned": total_earned,
                "net_flow": total_earned - total_spent,
                "average_transaction": total_spent / len(withdrawals) if withdrawals else 0,
                "withdrawal_count": len(withdrawals),
                "deposit_count": len(deposits)
            }
        except Exception as e:
            print(f"Error in spending insights: {e}")
            return {
                "total_spent": 0,
                "total_earned": 0,
                "net_flow": 0,
                "average_transaction": 0,
                "withdrawal_count": 0,
                "deposit_count": 0
            }
    
    def _get_numeric_amount(self, transaction: Dict) -> float:
        """Safely extract numeric amount from transaction"""
        amount = transaction.get('amount', 0)
        if isinstance(amount, (int, float)):
            return float(amount)
        elif isinstance(amount, str):
            try:
                cleaned = re.sub(r'[^\d.-]', '', amount)
                return float(cleaned)
            except (ValueError, TypeError):
                return 0.0
        return 0.0
    
    def _get_monthly_summary(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Generate monthly spending summary"""
        monthly_data = {}
        
        for transaction in transactions:
            date_str = transaction.get('date', '')
            amount = self._get_numeric_amount(transaction)
            
            if len(date_str) >= 7:
                month = date_str[:7]
            else:
                month = "Unknown"
            
            if month not in monthly_data:
                monthly_data[month] = {"spent": 0, "earned": 0}
            
            if amount < 0:
                monthly_data[month]["spent"] += abs(amount)
            else:
                monthly_data[month]["earned"] += amount
        
        return monthly_data
    
    def _categorize_spending(self, transactions: List[Dict]) -> Dict[str, float]:
        """Categorize spending by predefined categories"""
        categorized = {category: 0.0 for category in self.categories.keys()}
        
        for transaction in transactions:
            amount = self._get_numeric_amount(transaction)
            if amount < 0:  # Only spending (negative amounts)
                description = transaction.get('description', '').lower()
                abs_amount = abs(amount)
                
                category_found = False
                for category, keywords in self.categories.items():
                    if any(keyword in description for keyword in keywords):
                        categorized[category] += abs_amount
                        category_found = True
                        break
                
                # If no category found, add to "other"
                if not category_found:
                    if "other" not in categorized:
                        categorized["other"] = 0.0
                    categorized["other"] += abs_amount
        
        return {k: round(v, 2) for k, v in categorized.items() if v > 0}
    
    def _analyze_cash_flow(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Analyze cash flow patterns"""
        daily_flow = {}
        
        for transaction in transactions:
            date_str = transaction.get('date', 'Unknown')
            amount = self._get_numeric_amount(transaction)
            
            if date_str not in daily_flow:
                daily_flow[date_str] = 0.0
            
            daily_flow[date_str] += amount
        
        # Calculate statistics
        flows = list(daily_flow.values())
        avg_daily_flow = sum(flows) / len(flows) if flows else 0
        
        return {
            "daily_cash_flow": daily_flow,
            "average_daily_flow": round(avg_daily_flow, 2),
            "days_with_positive_flow": len([f for f in flows if f > 0]),
            "days_with_negative_flow": len([f for f in flows if f < 0])
        }