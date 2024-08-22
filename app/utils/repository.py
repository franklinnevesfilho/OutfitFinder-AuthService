import logging
from typing import Optional, Type, List, TypeVar
from sqlalchemy.exc import SQLAlchemyError
from app.config import database
from app.models import Base

# Set up a logger for the repository
logger = logging.getLogger(__name__)

T = TypeVar('T', bound=Base)

class Repository:
    def __init__(self, base_model: Type[T], options = None):
        self.base_model = base_model
        self.options = options

    def _query(self, session):
        return session.query(self.base_model).options(self.options) if self.options else session.query(self.base_model)


    def get_by(self, **kwargs) -> Optional[T]:
        session = database.get_session()
        try:
            model = self._query(session).filter_by(**kwargs).first()
            return model
        except SQLAlchemyError as e:
            logger.error(f"Error fetching {self.base_model.__name__} by {kwargs}: {str(e)}")
            session.rollback()
            return None
        finally:
            session.close()

    def create(self, model: Base) -> Optional[T]:
        session = database.get_session()
        try:
            session.add(model)
            session.commit()
            return model
        except SQLAlchemyError as e:
            logger.error(f"Error creating {self.base_model.__name__}: {str(e)}")
            session.rollback()
            return None
        finally:
            session.close()

    def update(self, model: Base) -> Optional[T]:
        session = database.get_session()
        try:
            session.merge(model)
            session.commit()
            return model
        except SQLAlchemyError as e:
            logger.error(f"Error updating {self.base_model.__name__}: {str(e)}")
            session.rollback()
            return None
        finally:
            session.close()

    def delete(self, model: Base) -> bool:
        session = database.get_session()
        try:
            session.delete(model)
            session.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error deleting {self.base_model.__name__}: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()

    def get_all(self) -> List[T]:
        session = database.get_session()
        try:
            models = self._query(session).all()
            return models
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all {self.base_model.__name__}: {str(e)}")
            session.rollback()
            return []
        finally:
            session.close()

    def get_all_by(self, **kwargs) -> List[T]:
        session = database.get_session()
        try:
            models = self._query(session).filter_by(**kwargs).all()
            return models
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all {self.base_model.__name__} by {kwargs}: {str(e)}")
            session.rollback()
            return []
        finally:
            session.close()

    def delete_by(self, **kwargs) -> bool:
        session = database.get_session()
        try:
            self._query(session).filter_by(**kwargs).delete()
            session.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error deleting {self.base_model.__name__} by {kwargs}: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()