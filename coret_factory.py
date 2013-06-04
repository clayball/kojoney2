#!/usr/bin/env python
from coret_fake import *
from honey_pot_ssh_user_auth_server import *
from twisted.conch.ssh import factory, connection, keys, transport

publicKey = FAKE_SSH_KEY
privateKey = FAKE_SSH_PRIVKEY

class CoretFactory(factory.SSHFactory):
    publicKeys = {'ssh-rsa': keys.getPublicKeyString(data=publicKey)}
    privateKeys = {'ssh-rsa': keys.getPrivateKeyObject(data=privateKey)}
    services = {
                'ssh-userauth': HoneyPotSSHUserAuthServer,
                'ssh-connection': connection.SSHConnection
                }
    
    def buildProtocol(self, addr):
        t = transport.SSHServerTransport()
        #
        # Fix for BUG 1463701 "NMap recognizes Kojoney as a Honeypot"
        #
        t.ourVersionString = FAKE_SSH_SERVER_VERSION
        t.supportedPublicKeys = self.privateKeys.keys()
        if not self.primes:
            ske = t.supportedKeyExchanges[:]
            ske.remove('diffie-hellman-group-exchange-sha1')
            t.supportedKeyExchanges = ske
        t.factory = self
        return t