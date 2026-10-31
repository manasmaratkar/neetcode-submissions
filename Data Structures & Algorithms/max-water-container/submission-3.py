class Solution:
    def maxArea(self, heights: List[int]) -> int:
       left = 0
       right = len(heights) -1
       max_water = 0

       while left < right:
        # 1. Store the heights to minimize repeated array lookups
        left_h = heights[left]
        right_h = heights[right]

        # 2. Calculate area using the limiting height
        current_height = left_h if left_h < right_h else right_h
        current_water = (right - left) * current_height

        if current_water > max_water:
            max_water = current_water
        
        if left_h < right_h:
            while left < right and heights[left] <= left_h:
                left += 1
        else:
            while left < right and heights[right] <= right_h:
                right -= 1

       return max_water     