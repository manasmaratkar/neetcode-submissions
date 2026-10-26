class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        
        if len(set(temperatures)) == 1:
            return [0] * n
        
        result = [0] * n        
        # Storing ONLY indices now
        stack = [] 

        for curr_idx in range(n):
            curr_temp = temperatures[curr_idx]
            # While the stack is not empty and the current temperature is warmer 
            # than the temperature at the top of the stack
            while stack and curr_temp > temperatures[stack[-1]]:
                prev_idx = stack.pop()
                # Calculate the number of days between the two dates
                result[prev_idx] = curr_idx - prev_idx
            
            # Push the current index onto the stack
            stack.append(curr_idx)        
        return result