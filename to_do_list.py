import psycopg2.extras
import pandas as pd


def todo_list():
    print('Welcome to your to-do list creator')
    name = input("Enter your name: ")
    cond = int(input("Do you wish to create your to-do list\n1 -- Yes\n2 -- No\n-> "))
    if cond == 1:
        conn = None
        try:
            with psycopg2.connect(
                database='postgres',
                user='postgres',
                password='23gbe9fcmb.',
                port=5432
            ) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    cur.execute("DROP TABLE IF EXISTS todo_list")

                    create_script = '''CREATE TABLE IF NOT EXISTS todo_list (
                    order_todo  int PRIMARY KEY,
                    task        varchar(100) NOT NULL,
                    time_todo   varchar(100) NOT NULL,
                    reply       varchar(40) NOT NULL
                    )'''
                    cur.execute(create_script)
                    print('Table created')

                    insert_script = 'INSERT INTO todo_list (order_todo, task, time_todo, reply) VALUES (%s, %s, %s, %s)'
                    quest = ''
                    count = 0
                    # Creating your to-do list
                    while quest != 'quit':
                        t_ask = input("Enter task:\n-> ").title()
                        time_to_do = input("Enter time set to complete the task\n-> ")
                        count += 1
                        print(count)
                        insert_value = (count, t_ask, time_to_do, 'NOT DONE')
                        cur.execute(insert_script, insert_value)
                        quest = input("To continue hit 'ENTER'\nTo stop type 'quit'")
                    if quest == 'quit':
                        view = int(input("View your to-do list?\n1 -- Yes\n2 -- No\n-> "))
                        # Viewing your to-do list
                        if view == 1:
                            # I felt that since I returned the 'fetchall' as a dictionary I would be able to
                            # View it as a pandas DataFrame, but it kept referencing 'sqlAlchemy'
                            # I am not in an environment that allows me to install whatever module was needed.
                            # So I left it as it is.
                            info = pd.read_sql_query('''SELECT * FROM todo_list''', conn)
                            df = pd.DataFrame(info, index=None)
                            print(df)
                        else:
                            pass

                    ques = int(input("Done with the task\n1 -- Yes\n2 -- No\n-> "))
                    if ques == 1:
                        cur.execute("SELECT task FROM todo_list")
                        for i in cur.fetchall():
                            for j in i:
                                print(j)
                        updat_e = int(input('Update task?\n1 -- Yes\n2 -- No\n-> '))
                        if updat_e == 1:
                            # UPDATING TASK REPLY TO DONE
                            tas = input("What task?\n-> ").title()
                            cur.execute("SELECT task FROM todo_list")
                            for record in cur.fetchall():
                                for i in record:
                                    print(i)
                                if tas == i:
                                    update_script = f"UPDATE todo_list SET reply = DONE WHERE task = {tas}"
                                    cur.execute(update_script)

        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    else:
        print(f"Come back when you are ready {name}.")
