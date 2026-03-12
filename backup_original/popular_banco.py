import sqlite3, random
from datetime import datetime, timedelta
orgs=['Pref SP','Pref BH','Pref Curitiba','UFMG','HC Porto Alegre','Pref Recife','Sec Educ RJ','Pref Brasilia','IFSP']
objs=[('Cadeiras escolares',120000),('Material escolar',85000),('Reforma escolas',450000),('Cozinha industrial',180000),('Uniformes',95000),('Cobertura metalica',320000),('Notebooks',580000),('Material limpeza',45000),('Estrutura metalica',890000),('Reforma saude',650000),('Playground',78000),('Cimento',125000),('Energia solar',420000),('Fogao industrial',65000),('Manutencao',95000)]
conn=sqlite3.connect('banco.db')
cur=conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS licitacoes(id INTEGER PRIMARY KEY,orgao TEXT,objeto TEXT,valor REAL,margem REAL,fonte TEXT,link TEXT,data_publicacao TEXT,data_captura TEXT DEFAULT CURRENT_TIMESTAMP,status TEXT DEFAULT "nova")')
hoje=datetime.now()
for i in range(20):
 obj,val=random.choice(objs);v=val*random.uniform(0.8,1.2);d=(hoje-timedelta(days=random.randint(0,5))).strftime('%Y-%m-%d')
 cur.execute('INSERT INTO licitacoes (orgao,objeto,valor,margem,fonte,link,data_publicacao,status) VALUES (?,?,?,?,?,?,?,?)',(random.choice(orgs),obj,round(v,2),0.25,'DEMO','https://demo.com/'+str(i),d,'nova'))
conn.commit();cur.execute('SELECT COUNT(*) FROM licitacoes');print('✅',cur.fetchone()[0],'licitações inseridas!');conn.close()