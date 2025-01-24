
class obs:
  def __init__ (self,manager,pos,grabable=False,grabbed=False,shadow=False,wall=False):
    self.pos=pos
    self.grabable=grabable
    self.grabbed=grabbed
    self.shadow=shadow
    self.wall=wall
    manager.thingmanag.append(self)

class thingmanag:
  def __init__ (self):
    self.thingmanag=[]
  def getobs(self):
    return self.thingmanag
  def getposes(self):
    return [obs.pos for obs in self.thingmanag]
