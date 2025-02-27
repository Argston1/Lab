from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Таблица Team
class Team(Base):
    __tablename__ = 'Team'
    TeamId = Column(Integer, primary_key=True)
    Name = Column(String)
    DivisionId = Column(Integer, ForeignKey('Division.DivisionId'))

    division = relationship('Division', back_populates='teams')

# Таблица Division
class Division(Base):
    __tablename__ = 'Division'
    DivisionId = Column(Integer, primary_key=True)
    Name = Column(String)

    teams = relationship('Team', back_populates='division')

# Таблица Match
class Match(Base):
    __tablename__ = 'Match'
    MatchId = Column(Integer, primary_key=True)
    HomeTeamId = Column(Integer, ForeignKey('Team.TeamId'))
    AwayTeamId = Column(Integer, ForeignKey('Team.TeamId'))
    Date = Column(DateTime)
    HomeScore = Column(Integer)
    AwayScore = Column(Integer)

    home_team = relationship('Team', foreign_keys=[HomeTeamId])
    away_team = relationship('Team', foreign_keys=[AwayTeamId])

# Настройка базы данных
def setup_database(database_path="sqlite:///sports_league.sqlite"):
    engine = create_engine(database_path)
    Base.metadata.create_all(engine)
    return engine

# Создание сессии
def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()