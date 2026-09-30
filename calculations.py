# Online Python add a new message MESSAGE @ compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
#print("Start small. Ship something.")

class calculations:
    def __init__(self):
        ls=self.ls

    def aver(self):
        for j in self.ls:
            if type(j)==str:
                self.ls.remove(j)
        #print(ls,"INSIDE CALL")
        temp=0
        for i in self.ls:
            temp=temp+i
        den=len(self.ls)
        avg=temp/den
        return avg
    