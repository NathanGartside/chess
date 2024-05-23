from ..piece import Piece


class Rook(Piece):
    def __init__(self, position):
        super().__init__(position)
        self.set_name('R')
        a = [1,2,3,4]
        b = [5,6,7]
        c = a + b

def lengthOfLongestSubstring(s):
    """
    :type s: str
    :rtype: int
    """
    maxPos = len(set(s))
    currMax = 0
    substring = []
    for i in range(len(s)):
        if (s[i] in substring):
            currMax = len(substring) if len(substring) > currMax else currMax
            substring = []
            # No need to continue if we've achieved the possible max
            # if (currMax == maxPos):
            #    break
        else:
            substring.append(s[i])
    return len(substring) if len(substring) > currMax else currMax