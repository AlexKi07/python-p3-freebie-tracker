from models import Base, Company, Dev, Freebie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use this path if you don't already have a separate setup file
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

# Clear and seed
session.query(Freebie).delete()
session.query(Company).delete()
session.query(Dev).delete()

dev1 = Dev(name='Alice')
dev2 = Dev(name='Bob')
company1 = Company(name='TechCorp', founding_year=2001)
company2 = Company(name='InnovateX', founding_year=1999)

freebie1 = Freebie(item_name='Sticker', value=1, dev=dev1, company=company1)
freebie2 = Freebie(item_name='T-Shirt', value=10, dev=dev1, company=company2)
freebie3 = Freebie(item_name='Mug', value=5, dev=dev2, company=company1)


session.add_all([dev1, dev2, company1, company2, freebie1, freebie2, freebie3])
session.commit()

print("✅ Seeded database!")
