#!/usr/bin/python
from twisted.internet import reactor
from twisted.internet import protocol
import sys
import MySQLdb


class BroadcastingDatagramProtocol(protocol.DatagramProtocol):
    db = MySQLdb.connect(host='localhost', 
                         user='root', 
                         passwd='qwe123',
                         db='ccme_telephony',
                         charset='utf8')
    db_session = []

    def startProtocol(self):
        self.db_session = self.db.cursor()
        return self.db_session

    def stopProtocol(self):
        self.db.close()

    def datagramReceived(self, data, addr):
        try:
            self.db_session.execute("INSERT INTO ccme_raw(data) VALUES ('%s')" % data)
            self.db.commit()
        except:
            self.db.rollback()

def startListening(port):
    reactor.listenUDP(port, BroadcastingDatagramProtocol())
    reactor.run()

if __name__ == "__main__":

    startListening(int(sys.argv[1]))
