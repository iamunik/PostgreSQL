import numpy as np
import pandas as pd
import psycopg2.extras
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

saeun = "A a B b C c D d E e F f G g H h I i L l J j K k M m N n O o P p Q q R r S s T t U u v V w W X x Y y Z z"\
    "1 2 3 4 5 6 7 8 9 0 ! @ # * . ,"
seun_id = saeun.split()


def create_table():
    try:
        with psycopg2.connect(
                database='postgres',
                user='postgres',
                password='12345',
                port=5432
        ) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("DROP TABLE IF EXISTS billboard")
                create_script = '''CREATE TABLE IF NOT EXISTS billboard (
                                    id        varchar(25) PRIMARY KEY,
                                    artist    varchar(100) NOT NULL,
                                    song      varchar(100) NOT NULL,
                                    genre     varchar(100) NOT NULL,
                                    ranking   int
                                    )'''
                cur.execute(create_script)
                print('Table Created')
    except Exception as error:
        print(error)
    finally:
        conn.close()
        print("Task be completed")


def insert_into_table():
    with psycopg2.connect(
                database='postgres',
                user='postgres',
                password='12345',
                port=5432) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            new_script = "INSERT INTO billboard (id, artist, song, genre, ranking) VALUES (%s, %s, %s, %s, %s)"
            d = ''

            while d != ".":
                random_alpha_num_sym = [np.random.choice(seun_id, 5)]
                random_id = "id_" + "".join(random_alpha_num_sym[0])
                print("Enter the details below")
                song = input("The Song\n-> ").title()
                artist = input("The Artist\n-> ").title()
                genre = input('The Genre\n-> ').title()
                if song in check_for_existing_song() and artist in check_for_existing_artist():
                    print("Cannot add to billboard\nArtist and song already exists")
                    d = input("Press enter to continue\nPress '.' to terminate\n-> ")
                    if d == '.':
                        print("Insertion Terminated!!!.")
                else:
                    ranking = 30
                    new_value = (random_id, artist, song, genre, ranking)
                    cur.execute(new_script, new_value)
                    d = input("Press enter to continue\nPress '.' to terminate\n-> ")
                    print("Details added\nInsertion Completed!!!")
    conn.close()


def view_in_pandas():
    with psycopg2.connect(
            database='postgres',
            user='postgres',
            password='12345',
            port=5432) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            new_script = "SELECT * FROM billboard"
            cur.execute(new_script)
            collon = [i[0] for i in cur.description]
            read = pd.read_sql_query("SELECT * FROM billboard", conn)
            cur.close()
            info = pd.DataFrame(read, columns=collon, index=None)
            print(info)
    conn.close()


def view_columns():
    with psycopg2.connect(
            database='postgres',
            user='postgres',
            password='12345',
            port=5432) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            new_script = "SELECT * FROM billboard"
            cur.execute(new_script)
            coll = [i[0] for i in cur.description]
            for i in coll:
                print(i)
    conn.close()


def update_vote(vote, i_d):     # Condition to ask if user wants to vote function should be placed in code
    with psycopg2.connect(
            database='postgres',
            user='postgres',
            password='12345',
            port=5432) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            if vote == 1:
                update_script = f"UPDATE billboard SET ranking = (ranking+10) WHERE id = '{i_d}'"
                cur.execute(update_script)
            else:
                print("Thanks for your time")


def top_10():
    with psycopg2.connect(
            database='postgres',
            user='postgres',
            password='12345',
            port=5432) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            view_script = "SELECT * FROM billboard ORDER BY ranking DESC LIMIT 10"
            cur.execute(view_script)
            read = pd.read_sql_query(view_script, conn)
            cur.close()
            collon = [i[0] for i in cur.description]
            info = pd.DataFrame(read, columns=collon, index=None)
            print(info)


# Conditions for voting it returns your selected ID this will be stored in a variable and put into the update function
def condition_id(i_d):
    with psycopg2.connect(
            database='postgres',
            user='postgres',
            password='12345',
            port=5432
    ) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            show_script = "SELECT id from billboard ORDER BY ranking DESC LIMIT 10"
            cur.execute(show_script)
            print('Number: ')
            if i_d == 1:
                i_d = cur.fetchall()[0]
                return i_d
            elif i_d == 2:
                i_d = cur.fetchall()[1]
                return i_d
            elif i_d == 3:
                i_d = cur.fetchall()[2]
                return i_d
            elif i_d == 4:
                i_d = cur.fetchall()[3]
                return i_d
            elif i_d == 5:
                i_d = cur.fetchall()[4]
                return i_d
            elif i_d == 6:
                i_d = cur.fetchall()[5]
                return i_d
            elif i_d == 7:
                i_d = cur.fetchall()[6]
                return i_d
            elif i_d == 8:
                i_d = cur.fetchall()[7]
                return i_d
            elif i_d == 9:
                i_d = cur.fetchall()[8]
                return i_d
            elif i_d == 10:
                i_d = cur.fetchall()[9]
                return i_d
            else:
                return "Wrong Selection"


def visualize():
    with psycopg2.connect(
            database='postgres',
            user='postgres',
            password='12345',
            port=5432
    ) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            select_script = "SELECT * FROM billboard"
            cur.execute(select_script)
            columns = [i[0] for i in cur.description]
            print(columns)
            x_axis = input("Select an x axis from the column\n-> ")
            if x_axis != 'ranking':
                y_axis = "ranking"
            elif x_axis == 'ranking':
                y_axis = input("Select a y axis from the column\n-> ")
            read = pd.read_sql_query(select_script, conn)
            sns.barplot(x=f'{x_axis}', y=f'{y_axis}', data=read)
            return plt.show()


def check_for_existing_song():
    with psycopg2.connect(
            database='postgres',
            user='postgres',
            password='12345',
            port=5432) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            new_script = "SELECT song from billboard"
            cur.execute(new_script)
            fetch = cur.fetchall()
            song = [i[0] for i in fetch]
            return song


def check_for_existing_artist():
    with psycopg2.connect(
            database='postgres',
            user='postgres',
            password='12345',
            port=5432) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            new_script = "SELECT artist from billboard"
            cur.execute(new_script)
            fetch = cur.fetchall()
            artist = [i[0] for i in fetch]
            return artist


selection = int(input("""-----------------------------------------
WELCOME TO THE BILLBOARD VOTING SIMULATOR
-----------------------------------------
In this simulation you will be able to do a few things like
- View all songs that already have votes
- View the columns necessary incase you want to add your song and vote for it
- Add your song to the chart and vote for it
- Vote for a song of your choice (each vote carries 5 points)
- View the top 10 songs and their votes when you are done with the program
- Visualize the data to know which carries the highest point (bar chart)
-----------------------------------------------------------------------------------
To view the complete data-set               Press 1
To add your song to the data-set            Press 2
To vote for your preferred song/artist      Press 3
To visualize the data (bar chart)           Press 4
To quit                                     Press 5
-----------------------------------------------------------------------------------\n-> """))

# Having a little issue with sql_alchemy, I am still working on understanding its implementation
# Once I fully grasp it, I will make necessary changes to the project file.

if selection == 5:
    print("Thanks for at least viewing it")
elif selection == 1:
    view_in_pandas()  # Function defined to view the database with pandas.

# Function defined to insert into the table || Condition to check of songs exists has been implemented
elif selection == 2:
    insert_into_table()

elif selection == 3:
    up_vote = int(input(f"Pick your condition number...\n{top_10()}\n->"))  # Work In Progress
    c = condition_id(up_vote)
    print(c[0])
    update_vote(1, c[0])

elif selection == 4:
    visualize()     # Brief visualization with seaborn.

else:
    print("Wrong selection")
