from ..base import Base

class TimeOff(Base):
    DATABASE_NAME = "TimeOff"

    def __init__(self, id=None, **kwargs):        
        super().__init__(id=id, **kwargs)
