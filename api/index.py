from flask import Flask, jsonify  
import psycopg2  
  
app = Flask(__name__)  
  
# URI de connexion Neon PostgreSQL  
uri = "postgresql://neondb_owner:npg_LxkwF2RzD7uf@ep-late-mouse-aem21m36-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"  
  
def get_conn():  
    return psycopg2.connect(uri)  

def create_table_if_not_exists():  
    conn = get_conn()  
    cur = conn.cursor()  
    cur.execute("""  
        SELECT EXISTS (  
            SELECT FROM information_schema.tables   
            WHERE table_name = 'ping'  
        );  
    """)  
    exists = cur.fetchone()[0]  
  
    if not exists:  
        cur.execute("""  
            CREATE TABLE ping (  
                id SERIAL PRIMARY KEY,  
                message TEXT NOT NULL  
            );  
        """)  
        cur.execute("""  
            INSERT INTO ping (message) VALUES (%s);  
        """, ("ping reussi",))  
        conn.commit()  
        print("Table 'ping' créée et message inséré.")  
    else:  
        print("Table 'ping' existe déjà, rien à faire.")  
  
    cur.close()  
    conn.close()  
  
@app.route("/")  
def show_pings():  
    conn = get_conn()  
    cur = conn.cursor()  
    cur.execute("SELECT id, message FROM ping ORDER BY id;")  
    rows = cur.fetchall()  
    cur.close()  
    conn.close()  
    data = [{"id": r[0], "message": r[1]} for r in rows]  
    return jsonify(data)  
  
# Appelle la création de la table au démarrage de l'app (au premier import)
create_table_if_not_exists()
