from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from passlib.hash import bcrypt

### USER AND TOKEN MANAGEMENT ###############################################################

########################################################
## kleine Anleitung zum User erstellen und nutzen:
#   User erstellen:
#       POST Request an jan-ehehalt.de:8000/users 
#       im payload muss username und password_hash sein
#       password_hash ist btw noch kein hash, variable ist nur doof benannt lol
#       wird im backend aber zu hash umgewandelt und als hash gespeichert
#       in password_hash muss einfach das vom User vergebene Passwort stehen
#   Bearer Token erhalten:
#       POST Request an  jan-ehehalt.de:8000/token
#       Payload ist username und password
#       Response ist der token
#   Zum prüfen ob alles richtig funktioniert hat:
#       GET Request an jan-ehehalt.de:8000/users/me
#       braucht Authorization bearer token
#       siehe https://youtu.be/6hTRw_HK3Ts?si=QULkBCbJgXscvW9-&t=2272
#       Response ist dann die User info lol
#
#   Ich habe auch mal einen Testuser angelegt: username: testuser password: testpasswort
#   Die ganzen Accounts werden aktuell in der sqlite Datenbank hier im Ordner gespeichert (lol), wird noch umgestellt auf die richtige db
#
########################################################

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128) 
    
    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)
    
User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

## Prüft ob Username Passwort kombination richtig, also ob Anmeldung erfolgreich
async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user



