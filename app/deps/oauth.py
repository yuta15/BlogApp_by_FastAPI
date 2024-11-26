from fastapi.security import OAuth2PasswordBearer 


oauth2_scheme_suseruser = OAuth2PasswordBearer(tokenUrl='/superuser')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')