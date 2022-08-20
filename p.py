class Solution:
    def halvesAreAlike(self, s: str) -> bool:
        v = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
        return sum(ss in v for ss in s[:len(s)//2]) == sum(ss in v for ss in s[len(s)2:])