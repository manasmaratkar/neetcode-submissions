class Solution:
    def isValid(self, s: str) -> bool:

        # Fast exit for odd lengths
        if len(s) % 2 != 0: 
            return False

        bracket_map = {'(': ')', '[': ']', '{': '}'}
        stack = []

        for char in s:
            if char in bracket_map:
                # Push the expected CLOSING bracket onto the stack
                stack.append(bracket_map[char])
            else:
                # If stack is empty or the top doesn't match the current closing char
                 if not stack or stack.pop() != char:
                    return False       
        return not stack