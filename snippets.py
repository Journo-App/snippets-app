import argparse
import sys
import logging
import psycopg2

# Set the log output file, and the log level

# The filename argument describes where you want the log to be saved. 
# In this case, it will write to a file called "snippets.log" in the current directory. 
# The level argument sets the log level. The logging module splits log messages into one 
# of five severity levels: debug, info, error, warning, critical. 

# When you set the log level to DEBUG all of the messages will be logged. 
# If it is set to WARNING 
# only log messages with a severity of WARNING or higher will be logged. 


logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets'")
logging.debug("Database connection established.")

def put(name, snippet):
#Store a snippet with an associated name 
    
    with connection, connection.cursor() as cursor:
    
        logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
        cursor = connection.cursor()
        command = "insert into snippets values (%s, %s)"
        try:
            command = "insert into snippets values (%s, %s)"
            cursor.execute(command, (name, snippet))
        except psycopg2.IntegrityError as e:
            connection.rollback()
            command = "update snippets set message=%s where keyword=%s"
            cursor.execute(command, (snippet, name))
            connection.commit()
            logging.debug("Snippet stored successfully.")
            return name, snippet
   

"""When called, this function will report in the log exactly that the put feature doesn't exist yet. Using the well-recognized tag FIXME identifies the problem both in the source and the log. Formatting the strings with the !r modifier means that the repr() function will be run over the data to provide the output. (repr() returns a string containing a printable representation of an object.) This ensures that the log is clean and readable, no matter what string is provided."""

def get(name):
    with connection, connection.cursor() as cursor:
         cursor.execute("select message from snippets where keyword=%s", (name,))
         row = cursor.fetchone()
         connection.commit()
    print type(row)


    if not row:
        # No snippet was found with that name.
        logging.error("Sorry but there's no matching snippet  - get({!r})".format(name))
        print "Sorry but there's no matching snippet"
        print (row) 
        return row 
    return row 

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")

    #subparser for the get command 
    get_parser = subparsers.add_parser("get", help="Retrieve the snippet")
    get_parser.add_argument("name", help="The name of the snippet")


    arguments = parser.parse_args(sys.argv[1:])
    
# Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))


if __name__ == "__main__":
     main()
