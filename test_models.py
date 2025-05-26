import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import Base, Company, Dev, Freebie


@pytest.fixture
def session():
   
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_company(session):
    company = Company(name="TechCorp", founding_year=2001)
    session.add(company)
    session.commit()
    assert company.id is not None
    assert company.name == "TechCorp"

def test_give_freebie(session):
    company = Company(name="TechCorp", founding_year=2001)
    dev = Dev(name="Alice")
    session.add_all([company, dev])
    session.commit()

    freebie = company.give_freebie(dev, "Sticker", 5, session=session)
    session.commit()

    assert freebie.item_name == "Sticker"
    assert freebie.dev == dev
    assert freebie.company == company
    assert freebie.value == 5
    assert dev.received_one("Sticker")

def test_give_away_freebie(session):
    company = Company(name="TechCorp", founding_year=2001)
    dev1 = Dev(name="Alice")
    dev2 = Dev(name="Bob")
    session.add_all([company, dev1, dev2])
    session.commit()

    freebie = company.give_freebie(dev1, "Mug", 10, session=session)
    session.commit()

    # Alice gives the freebie to Bob
    dev1.give_away(dev2, freebie)
    session.commit()

    assert freebie.dev == dev2
    assert dev2.received_one("Mug")
    assert not dev1.received_one("Mug")

def test_dev_companies_property(session):
    company1 = Company(name="TechCorp", founding_year=2001)
    company2 = Company(name="InnovateX", founding_year=1999)
    dev = Dev(name="Alice")
    session.add_all([company1, company2, dev])
    session.commit()

    company1.give_freebie(dev, "Sticker", 5, session=session)
    company2.give_freebie(dev, "T-Shirt", 15, session=session)
    session.commit()

    assert set(dev.companies) == {company1, company2}