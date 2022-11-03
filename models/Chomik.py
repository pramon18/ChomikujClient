import requests
from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Chomik(Base):
    __tablename__ = 'Chomik'
    id = Column(Integer, Sequence('chomik_id_seq'), primary_key=True)
    username = Column(String)
    __password = Column('password', String)

    
    def __init__(self, name, password, requests_session=None, ssl=True):
        #assert isinstance(name, ustr)
        #assert isinstance(password, ustr)
        #assert isinstance(requests_session, requests.Session) or requests_session is None
        self.username = name
        self.__password = password
        #self.__password = password
        #self.sess = requests.session() if requests_session is None else requests_session
        #self.ssl = ssl
        #self.__token, 
        #self.chomik_id = '', 0
        #self._last_action = datetime.now()
        #self._folder_cache = {}
        #self.logger = logging.getLogger('ChomikBox.Chomik.{}'.format(name))
        # TODO: init adult & gallery_view properly
        #ChomikFolder.__init__(self, self, name, 0, None, False, False, False, None)
    '''
    def __repr__(self):
        return '<ChomikBox.Chomik: {n}>'.format(n=self.name)

    @property
    def path(self):
        return '/'
    '''