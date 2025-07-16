from datetime import date
from expiry_dates import USDINRExpiryDates2025

class TimeToExpiryCalculator:
    """
    A class to calculate the number of days to expiry for USDINR futures contract.
    Dynamically selects the expiry date based on the current month.
    """

    @staticmethod
    def get_current_month_expiry() -> date:
        """
        Returns the expiry date based on the current month.
        
        Returns:
            date: The expiry date of the current month's contract.
        """
        month = date.today().month
        month_expiry_map = {
            4: USDINRExpiryDates2025.APRIL,
            5: USDINRExpiryDates2025.MAY,
            6: USDINRExpiryDates2025.JUNE,
            7: USDINRExpiryDates2025.JULY,
            8: USDINRExpiryDates2025.AUGUST,
            9: USDINRExpiryDates2025.SEPTEMBER,
            10: USDINRExpiryDates2025.OCTOBER,
            11: USDINRExpiryDates2025.NOVEMBER,
            12: USDINRExpiryDates2025.DECEMBER
        }
        return month_expiry_map.get(month)

    @staticmethod
    def calculate_days_to_expiry() -> int:
        """
        Calculates the number of days to expiry for the current month's USDINR contract.
        Excludes today from the count.
        
        Returns:
            int: Days to expiry. Returns 0 if expiry is today or passed.
        """
        today = date.today()
        expiry = TimeToExpiryCalculator.get_current_month_expiry()
        
        if expiry is None:
            raise ValueError("Expiry date not found for the current month.")

        days_to_expiry = (expiry - today).days
        return max(days_to_expiry, 0)
