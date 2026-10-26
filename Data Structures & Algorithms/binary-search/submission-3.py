import bisect

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # bisect_left uses O(log n) binary search in native C
        index = bisect.bisect_left(nums, target)
        
        # Check if the index is valid and actually matches the target
        if index < len(nums) and nums[index] == target:
            return index
            
        return -1