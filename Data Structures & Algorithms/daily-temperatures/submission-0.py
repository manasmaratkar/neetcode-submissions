class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        result = [0] * n
        
        # Will store pairs of (temperature, index)
        stack = [] 

        for curr_idx, curr_temp in enumerate(temperatures):
            # While the stack is not empty and the current temperature is warmer 
            # than the temperature at the top of the stack
            while stack and curr_temp > stack[-1][0]:
                prev_temp, prev_idx = stack.pop()
                # Calculate the number of days between the two dates
                result[prev_idx] = curr_idx - prev_idx
            
            # Push the current temperature and its index onto the stack
            stack.append((curr_temp, curr_idx))
        
        return result