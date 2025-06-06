import asyncio
from fastmcp import Client
client = Client("nlp_server.py")
import sqlite3

async def call_tool(nl_query: str):
    print("0")
    async with client:
        
        result = await client.call_tool("nl_to_sql", {"nl_query": nl_query})
        print("result :", result)
        print("------------------------------------------------------")
        query = result[0].text.split('\n')[0].replace('SQL Query: ', '')
        print("query:", query)
        print("------------------------------------------------------")
        
        
        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        rows = cursor.fetchall()
        for row in rows:
            print("------------------------------------------------------")
            print(row)
        print("------------------------------------------------------")

# asyncio.run(call_tool("show me all data from student"))
# asyncio.run(call_tool("add a Neha to the student list with enrollment EN1234, standard 10th, subject Physics, city Navsari and she likes to watch movies"))
# asyncio.run(call_tool("add a Ayush to the student list with enrollment EN1234, standard 10th, subject Physics, city Navsari and she likes to watch movies"))
# asyncio.run(call_tool("give all students who are in 10th standard and name starts with N"))
# asyncio.run(call_tool("delete all data"))
asyncio.run(call_tool("update Neha to Pratik  where city Navsari"))



query="SELECT * FROM students ;"
connection = sqlite3.connect("student.db")
cursor = connection.cursor()
cursor.execute(query)
rows = cursor.fetchall()
for row in rows:
    print(row)
print("------------------------------------------------------")