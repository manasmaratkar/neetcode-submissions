class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
        
        # Initialize directly to the first day's price
        min_price = prices[0]
        max_profit = 0

        for price in prices:
             # Update the lowest price seen so far
            if price < min_price:
                min_price = price
            # Calculate profit if sold today and update max_profit    
            elif price - min_price > max_profit:
                max_profit = price - min_price
        
        return max_profit