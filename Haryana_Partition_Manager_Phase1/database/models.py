from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Text
)

from sqlalchemy.orm import (
    declarative_base,
    relationship
)

Base = declarative_base()


# =====================================================
# VILLAGES
# =====================================================

class Village(Base):

    __tablename__ = "villages"

    id = Column(
        Integer,
        primary_key=True
    )

    district = Column(
        String(100)
    )

    tehsil = Column(
        String(100)
    )

    sub_tehsil = Column(
        String(100)
    )

    village_name = Column(
        String(100)
    )

    hadbast_no = Column(
        String(50)
    )

    jamabandi_year = Column(
        String(20)
    )

    khewats = relationship(
        "Khewat",
        back_populates="village"
    )

    def __repr__(self):
        return self.village_name


# =====================================================
# OWNERS
# =====================================================

class Owner(Base):

    __tablename__ = "owners"

    id = Column(
        Integer,
        primary_key=True
    )

    owner_name = Column(
        String(200)
    )

    father_name = Column(
        String(200)
    )

    address = Column(
        Text
    )

    mobile = Column(
        String(20)
    )

    email = Column(
        String(100)
    )

    remarks = Column(
        Text
    )

    ownerships = relationship(
        "Ownership",
        back_populates="owner"
    )

    def __repr__(self):
        return self.owner_name


# =====================================================
# KHEWATS
# =====================================================

class Khewat(Base):

    __tablename__ = "khewats"

    id = Column(
        Integer,
        primary_key=True
    )

    village_id = Column(
        Integer,
        ForeignKey("villages.id")
    )

    khewat_no = Column(
        String(50),
        nullable=False
    )

    khatauni_no = Column(
        String(50)
    )

    total_area = Column(
        Float,
        default=0
    )

    status = Column(
        String(30),
        default="JOINT"
    )

    remarks = Column(
        Text
    )

    created_on = Column(
        DateTime,
        default=datetime.utcnow
    )

    village = relationship(
        "Village",
        back_populates="khewats"
    )

    ownerships = relationship(
        "Ownership",
        back_populates="khewat",
        cascade="all, delete-orphan"
    )

    khasras = relationship(
        "Khasra",
        back_populates="khewat",
        cascade="all, delete-orphan"
    )

    documents = relationship(
        "Document",
        back_populates="khewat",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"Khewat {self.khewat_no}"
        )
# =====================================================
# OWNERSHIPS
# =====================================================

class Ownership(Base):

    __tablename__ = "ownerships"

    id = Column(
        Integer,
        primary_key=True
    )

    khewat_id = Column(
        Integer,
        ForeignKey("khewats.id")
    )

    owner_id = Column(
        Integer,
        ForeignKey("owners.id")
    )

    numerator = Column(
        Integer,
        nullable=False
    )

    denominator = Column(
        Integer,
        nullable=False
    )

    khewat = relationship(
        "Khewat",
        back_populates="ownerships"
    )

    owner = relationship(
        "Owner",
        back_populates="ownerships"
    )

    @property
    def share_text(self):

        return (
            f"{self.numerator}/"
            f"{self.denominator}"
        )


# =====================================================
# KHASRAS
# =====================================================

class Khasra(Base):

    __tablename__ = "khasras"

    id = Column(
        Integer,
        primary_key=True
    )

    khewat_id = Column(
        Integer,
        ForeignKey("khewats.id")
    )

    khasra_no = Column(
        String(100)
    )

    area = Column(
        Float,
        default=0
    )

    remarks = Column(
        Text
    )

    khewat = relationship(
        "Khewat",
        back_populates="khasras"
    )

    def __repr__(self):
        return self.khasra_no


# =====================================================
# PARTITION EVENTS
# =====================================================

class PartitionEvent(Base):

    __tablename__ = "partition_events"

    id = Column(
        Integer,
        primary_key=True
    )

    source_khewat_id = Column(
        Integer
    )

    new_khewat_id = Column(
        Integer
    )

    owners_removed = Column(
        Text
    )

    removed_area = Column(
        Float
    )

    partition_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    remarks = Column(
        Text
    )


# =====================================================
# DOCUMENTS
# =====================================================

class Document(Base):

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True
    )

    khewat_id = Column(
        Integer,
        ForeignKey("khewats.id")
    )

    document_type = Column(
        String(100)
    )

    file_path = Column(
        Text
    )

    remarks = Column(
        Text
    )

    uploaded_on = Column(
        DateTime,
        default=datetime.utcnow
    )

    khewat = relationship(
        "Khewat",
        back_populates="documents"
    )