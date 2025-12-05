from datetime import datetime, timedelta

class DateHelper:
    
    @staticmethod
    def format_date_header(date_str: str) -> str:
        """
        Format tanggal 'Today', 'Yesterday', atau tanggal lengkap
        Args:
            date_str: Date string in format "YYYY-MM-DD"
        Returns:
            Formatted date string
        """
        today = datetime.now().date()
        trans_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        if trans_date == today:
            return "Today"
        elif trans_date == today - timedelta(days=1):
            return "Yesterday"
        else:
            return trans_date.strftime("%B %d, %Y")
    
    @staticmethod
    def get_today() -> str:
        """Mendapatkan tanggal hari ini di format YYYY-MM-DD"""
        return datetime.now().strftime("%Y-%m-%d")


class CurrencyHelper:
    
    @staticmethod
    def format_amount(amount: float, prefix: str = "") -> str:
        """
        Format jumlah sebagai mata uang
        Args:
            amount: Amount to format
            prefix: Optional prefix (+ or -)
        Returns:
            Formatted string like "+ Rp 50,000"
        """
        if prefix:
            return f"{prefix} Rp {amount:,.0f}"
        return f"Rp {amount:,.0f}"