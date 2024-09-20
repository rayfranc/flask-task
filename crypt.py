from flask_bcrypt import Bcrypt


class Crypt(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Crypt, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def setup(self, app):
        self.enc = Bcrypt(app)

    def encrypt(self, pw):
        if not self.enc:
            raise Exception("Not app found on Crypt Class")
        h = self.enc.generate_password_hash(pw)
        print(h)
        return h.decode('utf-8')

    def check_hash(self,hash,pw ):
        if not self.enc:
            raise Exception("Not app found on Crypt Class")
        return self.enc.check_password_hash(hash, pw)
