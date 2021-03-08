import psycopg2

from main import logger

con = psycopg2.connect(
    database="new_part4_2",
    user="part4",
    password="part4_GfhjkzYtn321",
    # user="zapchasty",
    # password="zapchasty_GfhjkzYtn321",
    # host="116.203.219.63",
    host="localhost",
    port="5432"
)

cur = con.cursor()


def i_request(q):
    try:
        cur.execute(q)
        data = cur.fetchall()
    except psycopg2.DatabaseError as err:
        if err.pgerror:
            logger.error(q)
            print("Error: ", err)
    else:
        return data
    finally:
        con.commit()
