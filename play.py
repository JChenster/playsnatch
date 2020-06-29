from itertools import combinations

# list of scrabble words sorted by longest to shortest
f = open("sorted_scrabble.txt", "r")
words = f.read().split()
f.close()

cur = []
played = []

# checks to see if a word can be played with the flipped tiles
def isPossible(w, cur):
    # get letters in word
    l = []
    for letter in w:
        l.append(letter)
    for letter in cur:
        if letter in l:
            l.remove(letter)
    return len(l) == 0

# finds words to snatch
def findSnatch():
    ans = []
    for w in words:
        if isPossible(w, cur):
            ans.append(w)
    if len(ans) > 0:
        lens = list(map(lambda x: len(x), ans))
        m = max(lens)
        ans = list(filter(lambda x: len(x) == m, ans))
        print("[*] SNATCH:"," ".join(ans))

# processes a played word
def play(word):
    # snatching
    if isPossible(word, cur):
        print(f"{word} was snatched")
        for letter in word:
            cur.remove(letter)
        played.append(word)
    # stealing
    else:
        # makes a list of all the letters in new word
        l = []
        for letter in word:
            l.append(letter)
        for p in played:
            if isPossible(p, l):
                # remove the stolen word
                played.remove(p)
                # remove the letters of the old word in the new word
                for letter in p:
                    l.remove(letter)
                # remove excess
                for letter in l:
                    cur.remove(letter)
                played.append(word)
                print(f"{word} was stolen")

# checks for all possible ways to steal
# run time is garbo
def findStealDeep():
    ans = []
    if x % 10 == 0:
        for p in played:
            # get letters of played words in list
            l = []
            for letter in p:
                l.append(letter)
            # check if any words can be made by stealing said word
            for w in words:
                if len(w) <= len(p):
                    continue
                for i in range(1, len(cur)+1):
                    c = list(combinations(cur, i))
                    for t in c:
                        temp = l + list(t)
                        if len(w) == len(temp) and isPossible(w, temp) and p != w[:len(p)]:
                            ans.append(w)
    if len(ans) > 0:
        print("[*] STEAL:"," ".join(ans))

# only checks for ways to steal by adding an extra letter
def findSteal():
    ans = []
    for p in played:
        # get letters of played words in list
        l = []
        for letter in p:
            l.append(letter)
        # check if any words can be made by stealing said word
        for w in words:
            if len(w) <= len(p):
                continue
            for i in cur:
                temp = l + [i]
                if len(w) == len(temp) and isPossible(w, temp) and p != w[:len(p)]:
                    ans.append(w)
    if len(ans) > 0:
        print("[*] STEAL:"," ".join(ans))

while True:
    # backup var
    oldCur, oldPlayed = [], []
    for letter in cur:
        oldCur.append(letter)
    for word in played:
        oldPlayed.append(word)

    print("-" * 25)
    print("Current Letters:"," ".join(cur))
    print("Played words:"," ".join(played))
    print("Input: ", end="")
    i = input()
    if i == "end":
        break
    # tile is flipped
    if len(i) == 1:
        cur.append(i)
        if len(cur) >= 4:
            findSnatch()
        if len(played) > 0:
            findSteal()
    else:
        try:
            # processing delete
            args = i.split()
            if len(args) == 2 and args[0] == "d":
                cur.remove(args[1])
            # word is played
            else:
                play(i)
                if len(cur) >= 4:
                    findSnatch()
                findSteal()
        except ValueError:
            print("Invalid Play")
            cur = oldCur
            played = oldPlayed
    cur.sort()
    played.sort()
