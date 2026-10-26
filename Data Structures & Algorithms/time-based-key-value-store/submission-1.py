class TimeMap:

    def __init__(self):
        # A dictionary mapping each key to a list of [timestamp, value] pairs
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = []
        # Timestamps are strictly increasing, so appending maintains sorted order
        self.store[key].append([timestamp, value])
        

    def get(self, key: str, timestamp: int) -> str:
        # If the key doesn't exist at all, return an empty string immediately
        if key not in self.store:
            return ""

        pairs = self.store[key]
        left, right = 0, len(pairs) -1
        res = ""

        # Binary search loop: O(log N) runtime
        while left <= right:
            mid = (left + right) // 2

            # pairs[mid][0] is the timestamp
            if pairs[mid][0] <= timestamp:
                res = pairs[mid][1]      # Save the current valid string value candidate
                left = mid + 1           # Search the right half to find a closer/larger timestamp
            else:
                right = mid -1           # Timestamp is too far in the future, search the left half

        return res
