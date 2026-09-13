class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 1. Get frequencies
        count = Counter(nums)

        # 2. Initialize buckets
        bucket = [[] for _ in range(len(nums) + 1)]

        # 3. Fill buckets
        for num, freq in count.items():
            bucket[freq].append(num)

        # 4. Gather results from highest to lowest frequency
        output = []
        for i in range(len(bucket) - 1, -1, -1):
            for num in bucket[i]:
                output.append(num)
                if len(output) == k:
                    return output

        return output
