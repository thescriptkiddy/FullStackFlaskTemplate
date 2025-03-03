import uuid
import logging

from flask import abort

from backend.utils.helper import handle_sql_exceptions
from typing import Type, Any, Optional, Union
from shared.database import db_session, Base

# Initialize logger
logger = logging.getLogger(__name__)


@handle_sql_exceptions
def create_record(model: Type[Base], **kwargs) -> Optional[Base]:
    """Creates a new record of any model which has been passed as an argument."""
    if not model:
        message = "You forgot to provide the model as an argument"
        logger.warning(message)
        return None

    logger.info(f"Creating record with data: {kwargs}")
    record = model(**kwargs)
    db_session.add(record)
    db_session.commit()
    return record


@handle_sql_exceptions
def read_records(model: Type[Base], *identifier: Union[str, uuid.UUID]) -> Optional[Union[Base, list]]:
    """Returns either all existing records or specific records if identifier(s) has been passed"""
    if identifier:
        record = db_session.query(model).filter(model.uuid == identifier[0]).first()
        if not record:
            abort(404)  # This will raise a 404 error if the record is not found
        return record
    else:
        records = db_session.query(model).all()
        return records


@handle_sql_exceptions
def update_record(model: Type[Base], *identifier: Union[str, uuid.UUID], **kwargs) -> Optional[
    Base]:
    """Updates a database object"""
    logger.info(f"Updating record id: {identifier} with data: {kwargs}")
    record = db_session.query(model).filter(model.uuid == identifier[0]).first()
    if record:
        for key, value in kwargs.items():
            setattr(record, key, value)
        db_session.commit()
        return record
    return None


@handle_sql_exceptions
def delete_record(model: Type[Base], identifier: Union[str, uuid.UUID]) -> bool:
    """Deletes a database object"""
    logger.info(f"Deleting record id: {identifier}")
    result = db_session.session.execute(db_session.select(model).where(model.id == uuid.UUID(identifier)))
    record = result.scalar_one_or_none()
    if record:
        db_session.session.delete(record)
        db_session.session.commit()
        return True
    return False
