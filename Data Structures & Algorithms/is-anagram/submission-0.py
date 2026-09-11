class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
       s1 = s.replace(" ", "").lower()
       t1 = t.replace(" ", "").lower()

       return Counter(s1) == Counter(t1) 