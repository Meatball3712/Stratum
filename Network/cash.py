# Transaction Cash Accounts

import time, os
import Crypto.PublicKey.RSA as RSA
import Crypto.Hash.SHA256 as SHA256
import json

def generateKeys():
        """ Generate a new Private/Public Key pair """
        PrivKey = RSA.generate(1024, os.urandom)
        PubKey = PrivKey.publickey()
        return PrivKey, PubKey

class transaction():
    """ 
    A Transaction Object

    Used to create cash accounts and move money around. 
    """

    def __init__(self, source, target, amount, **kwargs):
        self.timestamp = kwargs.get("timestamp", int(round(time.time()*1000.0)))
        self.source = source
        self.target = target
        self.amount = amount
        self.SrcSig = kwargs.get("SrcSig", None)
        self.TrgSig = kwargs.get("TrgSig", None)

        self.ID = kwargs["ID"] if kwargs.has_key("ID") else self.generateID()

    def generateID(self):
        h = SHA256.new()
        h.update(str(self.timestamp))
        h.update(self.source)
        h.update(self.target)
        h.update(str(self.amount))
        return h.hexdigest()

    def getHash(self):

        temp = {
            "ID": self.ID,
            "Source" : self.source,
            "Target" : self.target,
            "Amount" : self.amount
        }
        return SHA256.new(json.dumps(temp)).digest()

    def sign(self, privKey):
        plaintext = self.getHash()
        K = ''
        signature = privKey.sign(plaintext, K)
        return signature

    def signSrc(self, privKey):
        self.SrcSig = self.sign(privKey)
        return self.SrcSig

    def signTrg(self, privKey):
        self.TrgSig = self.sign(privKey)
        return self.TrgSig

    def verify(self, pubKey, signature):
        plaintext = self.getHash()
        key = RSA.importKey(pubKey)
        return key.verify(plaintext, signature)

    def verifySrc(self):
        return self.verify(self.source, self.SrcSig)

    def verifyTrg(self):
        return self.verify(self.target, self.TrgSig)

    def verifyTransaction(self):
        assert self.SrcSig != "", "Transaction not signed by Source"                                                    # Check Signed by Source
        assert self.TrgSig != "", "Transaction not signed by Target"                                                    # Check Signed by Target
        assert self.verifySrc(), "Source Signature does not verify"                                                     # Check Source Signature Verifies
        assert self.verifyTrg(), "Target Signature does not verify"                                                       # Check Target Signature Verifies

        # Check Ledger adds up.

    def __str__(self):
        S = "Transaction: {}".format(self.ID)
        S += "\n{:-<32}---{:-<64}---{:-<64}---{:-<10}---{:-<32}---{:-<32}".format("","","","","","")
        S += "\n{:<32} | {:<64} | {:<64} | {:<10} | {:<32} | {:<32}".format("ID", "Source", "Target", "Amount", "Source Signature", "Target Signature")
        S += "\n{:-<32}-+-{:-<64}-+-{:-<64}-+-{:-<10}-+-{:-<32}-+-{:-<32}".format("","","","","","")
        # Build rows.
        rows = [["",]*6]
        column = 0
        ID = "\n".join([self.ID[i*32:(i+1)*32] for i in range(0, len(self.ID)//32)])
        ssig = "\n".join([str(self.SrcSig[0])[i*32:(i+1)*32] for i in range(0, len(str(self.SrcSig[0]))//32)])
        tsig = "\n".join([str(self.TrgSig[0])[i*32:(i+1)*32] for i in range(0, len(str(self.TrgSig[0]))//32)])
        for element in (ID, self.source, self.target, str(self.amount), ssig, tsig):
            row = 0
            for line in element.split("\n"):
                if len(rows) <= row:
                    rows.append( ["",]*6 )
                rows[row][column] = line
                row += 1
            column += 1

        for row in rows:
            S += "\n{:<32} | {:<64} | {:<64} | {:<10} | {:<32} | {:<32}".format(*row)

        return S


"""
# Signing Example
import Crypto.Hash.SHA256 as SHA256
import Crypto.PublicKey.RSA as RSA
import Crypto.PublicKey.DSA as DSA
import Crypto.PublicKey.ElGamal as ElGamal
import Crypto.Util.number as CUN
import os

plaintext='The rain in Spain falls mainly on the Plain'

# Here is a hash of the message
hash=SHA256.new(plaintext).digest()
print(repr(hash))
# '\xb1./J\xa883\x974\xa4\xac\x1e\x1b!\xc8\x11'

for alg in (RSA,):
    # Generates a fresh public/private key pair
    key=alg.generate(1024,os.urandom)

    if alg == DSA:
        K=CUN.getRandomNumber(128,os.urandom)
    elif alg == ElGamal:
        K=CUN.getPrime(128,os.urandom)
        while CUN.GCD(K,key.p-1)!=1:
            print('K not relatively prime with {n}'.format(n=key.p-1))
            K=CUN.getPrime(128,os.urandom)
        # print('GCD({K},{n})=1'.format(K=K,n=key.p-1))
    else:
        K=''

    # You sign the hash
    signature=key.sign(hash,K)
    print(len(signature),alg.__name__)
    # (1, 'Crypto.PublicKey.RSA')
    # (2, 'Crypto.PublicKey.DSA')
    # (2, 'Crypto.PublicKey.ElGamal')

    # You share pubkey with Friend
    pubkey=key.publickey()

    # You send message (plaintext) and signature to Friend.
    # Friend knows how to compute hash.
    # Friend verifies the message came from you this way:
    assert pubkey.verify(hash,signature)

    # A different hash should not pass the test.
    assert not pubkey.verify(hash[:-1],signature)
print("Finished")
"""

if __name__=="__main__":
    # Test Cash 

    # Test Transaction Module
    S_PRV, S_PUB = generateKeys()
    T_PRV, T_PUB = generateKeys()

    T = transaction(S_PUB.exportKey(), T_PUB.exportKey(), 100)
    S_SIG = T.signSrc(S_PRV)
    T_SIG = T.signTrg(T_PRV)

    print(T)

    T.verifyTransaction()
    print "Transaction Verified"