class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) -1

        while left <= right:
            # Calculate the middle index
            mid = (right+left) // 2
            val = nums[mid]

            # Target found, return its index
            if val == target:
                return mid
            # If target is greater, ignore the left half
            elif target > val:                
                left = mid + 1
            # If target is smaller, ignore the right half
            else:
                right = mid -1
                
        # Target does not exist in the array
        return -1 