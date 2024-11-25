from fastapi import Depends
from sqlmodel import Session
from typing import Annotated
from app.core.db import get_db


SessionDeps  = Annotated[Session, Depends(get_db)]


