def brute_force_median(S: set):
    """Brute force median"""
    ordered_set = sorted(list(S))
    return ordered_set[(len(S)-1) // 2]


def select(S, i):
    
    S = list(S)
    n = len(S)
    
    if n <= 5:
        return brute_force_median(S)
    
    ms = []
    for j in range(0, n, 5):
        ms.append(brute_force_median(S[j:j+5]))
    
    m_star = select(ms, (len(ms)-1)//2)
    
    S1, S2 = set(), set()
    for si in S: 
        if si < m_star:
            S1.add(si) 
        elif si > m_star: 
            S2.add(si)
    
    if i == len(S1):
        return m_star
    elif i < len(S1):
        return select(list(S1), i)
    else:
        return select(list(S2), i - len(S1))
    
    
if __name__ == "__main__":
    spam = [4, 7, 3, 18, 13, 15, 19, 12, 23, 5, 14, 17, 16, 20, 27]
    median = select(spam, (len(spam)-1)//2)
    print(median)