#define isFinal(s)       ((s) < 0)
def scanner():
    ch = ''
    currState = 1

    while (True):
        ch = NextChar( )
        if (ch == EOF): return 0 #fail
        currState = T [currState, ch]
        if (IsFinal(currState)):
            return 1  # success 