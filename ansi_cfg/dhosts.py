#!/pythonvenv/bin/python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    'sqlite:////yx/Pyprojects/PyWeb/DJ_ansible/db.sqlite3',
    encoding="utf8",
)

Base = declarative_base()
Session = sessionmaker(bind=engine)


class HostGroup(Base):
    __tablename__ = "webadmin_hostgroup"
    id = Column(Integer, primary_key=True)
    groupname = Column(String(50), unique=True)


class Host(Base):
    __tablename__ = "webadmin_host"
    id = Column(Integer, primary_key=True)
    hostname = Column(String(50))
    ip_addr = Column(String(15))
    group_id = Column(Integer, ForeignKey('webadmin_hostgroup.id'))


if __name__ == '__main__':
    session = Session()
    result = {}
    qset = session.query(HostGroup.groupname, Host.ip_addr).join(Host)
    for group, host in qset:
        if not result.get(group):
            result[group] = {}
            result[group]['hosts'] = []
        result[group]['hosts'].append(host)
    print(result)
