import sqlite3

def dump_and_load():
    conn_src = sqlite3.connect('website/db.sqlite3')
    conn_dst = sqlite3.connect('db.sqlite3')
    
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    
    cur_src.execute('SELECT * FROM main_partner')
    rows = cur_src.fetchall()
    
    # Get column names
    col_names = [f'"{description[0]}"' for description in cur_src.description]
    
    # Clear destination table first
    cur_dst.execute('DELETE FROM main_partner')
    
    # Insert rows
    placeholders = ', '.join(['?'] * len(col_names))
    insert_sql = f'INSERT INTO main_partner ({", ".join(col_names)}) VALUES ({placeholders})'
    
    for row in rows:
        cur_dst.execute(insert_sql, row)
        
    conn_dst.commit()
    print(f'Successfully copied {len(rows)} partners.')
    
    conn_src.close()
    conn_dst.close()

if __name__ == '__main__':
    dump_and_load()
