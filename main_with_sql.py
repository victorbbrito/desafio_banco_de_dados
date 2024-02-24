from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column, Float
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import select
from sqlalchemy import func

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "cliente"
    # atributos
    id = Column(Integer, primary_key = True)
    nome = Column(String)
    cpf = Column(String(11), unique= True)
    endereco = Column(String(30))
    
    conta = relationship(
        "Conta", back_populates = "cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf})"

class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key = True)
    tipo = Column(String(20),default='conta corrente', nullable = False)
    agencia = Column(String(10), nullable = False)
    numero = Column(Integer, nullable = False)
    saldo = Column(Float())
    client_id = Column(Integer, ForeignKey("cliente.id"), nullable = False)
    
    cliente = relationship(
        "Cliente", back_populates = "conta"
    )
    
    def __repr__(self):
        return f"Conta(id={self.id}, agencia={self.agencia}, número={self.numero}, saldo={self.saldo})"

# conexão com o banco de dados
engine = create_engine("sqlite://")

# criando as classes como tabelas nos bancos de dados
Base.metadata.create_all(engine)

with Session(engine) as session:
    juliana = Cliente(
        nome='juliana santos da silva',
        cpf='11122233300',
        endereco='Rua sem nome, 20, cidade nova',
        conta=[Conta(
            agencia='0121',
            numero=1,
            saldo= 100.00
            )]
    )
    
    amanda = Cliente(
        nome='amanda da silva pimentel',
        cpf='11122233301',
        endereco='Rua fulana de tal, 10, nova esperanca',
        conta=[Conta(
            agencia='0121',
            numero=2,
            saldo= 1000.00
            )]
    )
    
    rogerio = Cliente(
        nome='rogerio barbosa dos santos',
        cpf='11122233302',
        endereco='Rua sem nome, 29, cidade nova',
        conta=[Conta(
            agencia='0121',
            numero=3,
            saldo= 10330.00
            )] 
    )
    
    lucas = Cliente(
        nome='lucas sampaio da silva',
        cpf='11122233303',
        endereco='Rua sem nome, 01, sao jorge',
        conta=[Conta(
            agencia='0121',
            numero=4,
            saldo= 1010.00
            )]
    )
    
    # enviando para o BD (persistência de dados)
    session.add_all([juliana,amanda,rogerio,lucas])
    session.commit()


inspetor_engine = inspect(engine)

# printando os nome das tabelas
print(inspetor_engine.get_table_names())
    
# printando o nome das tables
print(Cliente.__tablename__)
print(Conta.__tablename__)

# printando o cliente com nome juliana
stmt = select(Cliente).where(Cliente.nome.contains("juliana"))

stmt_address = select(Conta).where(Conta.client_id.in_([2]))

stmt_users_order = select(Cliente).order_by(Cliente.id.desc())

stmt_join = select(Cliente.nome, Conta.agencia).join_from(Conta, Cliente)

stmt_count = select(func.count("*")).select_from(Cliente) # type: ignore

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()

print(inspetor_engine.get_table_names())
for user in session.scalars(stmt):
    print(user)
        
for address in session.scalars(stmt_address):
    print(address)
        
for user in session.scalars(stmt_users_order):
    print(user)
        
for result in results:
    print(result)
    
print("Total de usuários: ")
for count in session.scalars(stmt_count):
    print(count)


    
