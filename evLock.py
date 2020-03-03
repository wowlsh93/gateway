'''
Created on 2015. 2. 16.

@author: brad
'''


class evAutoThreadLock:
    m_oLock = None

    def __init__(self, oLock):
        self.m_oLock = oLock
        self.m_oLock.acquire()

    def __del__(self):
        self.m_oLock.release()