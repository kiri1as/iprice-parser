from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Integer, Sequence, String, func
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import Enum as SQLEnum

from model.base_model import BaseModel


class ProductRecordType(Enum):
    auto = 'auto'
    manual = 'manual'


class Product(BaseModel):
    __tablename__ = 'product_prices'

    record_id: Mapped[int] = mapped_column(
        BigInteger,
        Sequence('product_price_rec_seq', start=1, increment=1),
        name='record_id',
        primary_key=True
    )
    record_type: Mapped[ProductRecordType] = mapped_column(
        SQLEnum(ProductRecordType, name='record_creation_type'),
        name='record_type',
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        name='created_at',
        server_default=func.now(),
        nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        BigInteger,
        name='product_id',
        nullable=False
    )
    product_name: Mapped[str] = mapped_column(
        String,
        name='product_name',
        nullable=False
    )
    product_status: Mapped[Optional[str]] = mapped_column(
        String,
        name='product_status',
        nullable=True
    )
    product_price_old: Mapped[Optional[int]] = mapped_column(
        Integer,
        name='product_price_old',
        nullable=True
    )
    product_price_old_curr: Mapped[Optional[str]] = mapped_column(
        String,
        name='product_price_old_curr',
        nullable=True
    )
    product_price_new: Mapped[Optional[int]] = mapped_column(
        Integer,
        name='product_price_new',
        nullable=True
    )
    product_price_new_curr: Mapped[Optional[str]] = mapped_column(
        String,
        name='product_price_new_curr',
        nullable=True
    )

    @classmethod
    def from_dict(cls, data: dict):
        product = cls(
            record_type=data['record_type'],
            product_id=data['product_id'],
            product_name=data['product_name'],
            product_status=data['product_status'],
            product_price_old=data['product_price_old'],
            product_price_old_curr=data['product_price_old_curr'],
            product_price_new=data['product_price_new'],
            product_price_new_curr=data['product_price_new_curr']
        )
        return product

    def to_dict(self) -> dict:
        return {
            'record_id': self.record_id,
            'record_type': self.record_type,
            'created_at': self.created_at,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_status': self.product_status,
            'product_price_old': self.product_price_old,
            'product_price_old_curr': self.product_price_old_curr,
            'product_price_new': self.product_price_new,
            'product_price_new_curr': self.product_price_new_curr
        }
