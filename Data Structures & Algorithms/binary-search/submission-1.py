class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) -1

        while left <= right:
            mid = left + (right-left) // 2
            val = nums[mid]

            if val == target:
                return mid
            elif target > val:
                left = mid + 1
            else:
                right = mid -1

        return -1 