import objects_init as db
from sqlalchemy import Column, Integer, String, DateTime, or_
import datetime


class Transaction(db.base):
    __tablename__: str = "transaction"

    id: Column = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    time_stamp: Column = Column(DateTime, nullable=False)
    source_uuid: Column = Column(String(36))
    send_amount: Column = Column(Integer, nullable=False, default=0)
    destination_uuid: Column = Column(String(36))
    usage: Column = Column(String, default='')

    @property
    def serialize(self) -> dict:
        _ = self.id
        return {**self.__dict__}

    @staticmethod
    def create(source_uuid: str, send_amount: int, destination_uuid: str, usage: str):
        # create transaction and add it to database
        """
        Returns a transaction of a source_uuid.
        :return: transactions
        """
        # Create a new TransactionModel instance
        transaction: Transaction = Transaction(
            time_stamp=datetime.datetime.now(),
            source_uuid=source_uuid,
            send_amount=send_amount,
            destination_uuid=destination_uuid,
            usage=usage
        )

        # Add the new transaction to the db
        db.session.add(transaction)
        db.session.commit()

    @staticmethod
    def get(source_uuid):
        transactions: list = []
        for i in db.session.query(Transaction).filter(or_(Transaction.source_uuid == source_uuid,
                                                          Transaction.destination_uuid == source_uuid)):
            transactions.append({"time_stamp": str(i.time_stamp), "source_uuid": str(i.source_uuid),
                                 "amount": int(i.send_amount), "destination_uuid": str(i.destination_uuid),
                                 "usage": str(i.usage)})
        return transactions
