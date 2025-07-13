class Solution:
    def halvesAreAlike(self, s: str) -> bool:
        vowels = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
        return sum(ch in vowels for ch in s[:len(s)//2]) == sum(ch in vowels for ch in s[len(s)//2:])
