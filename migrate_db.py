import sqlite3

def run_migration():
    con = sqlite3.connect('adoptnshop.db')
    cur = con.cursor()
    cols = [c[1] for c in cur.execute('PRAGMA table_info(pets)').fetchall()]
    print('Existing cols in pets:', cols)

    new_cols = [
        ('state', "VARCHAR(100) DEFAULT 'Maharashtra'"),
        ('contact_phone', "VARCHAR(20)"),
        ('rehoming_fee', "FLOAT DEFAULT 0.0"),
        ('additional_images', "TEXT"),
        ('approval_status', "VARCHAR(20) DEFAULT 'approved'"),
        ('approval_notes', "TEXT")
    ]

    for col_name, col_def in new_cols:
        if col_name not in cols:
            print(f"Adding column {col_name}...")
            cur.execute(f"ALTER TABLE pets ADD COLUMN {col_name} {col_def}")

    # Set existing pets to 'approved'
    cur.execute("UPDATE pets SET approval_status = 'approved' WHERE approval_status IS NULL")
    cur.execute("UPDATE pets SET state = 'Maharashtra' WHERE state IS NULL")
    cur.execute("UPDATE pets SET rehoming_fee = 0.0 WHERE rehoming_fee IS NULL")

    con.commit()
    updated_cols = [c[1] for c in cur.execute('PRAGMA table_info(pets)').fetchall()]
    print('Migration complete. Current cols in pets:', updated_cols)
    con.close()

if __name__ == '__main__':
    run_migration()
