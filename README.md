PYLOTDB
=======

PYLOTDB -- Python &amp; MySQL framework for database creation, management, and analysis

This software consists of

1. PylotDB - the main program that allows database creation, management, 
and analysis; easily creates databases and tables without knowledge of MySQL; 
presents tables in row/column format with indexed headers and rows that 
allow users to select fields for graphing and statistics. A pre-formatted
table called 'sandbox' is created with just a couple of clicks, ready to 
receive data from Co-PylotDB as explained below. Once you can login
and access a MySQL database, PylotDB allows you to perform many tasks with 
tables and fields that were difficult to do under MySQL command lines alone.

2. Co-PylotDB - a one-window gui that allows users to send text files of data,
preferably in yaml format, to a designated database table. Other data is
captured and sent to the table as well, such as date, user, file 
directory, user comments, etc. The data is sent to an awaiting database 
table (by default called 'sandbox') created using PylotDB.

3. eCo-PylotDB - a specialized script, not a gui, to be used with Microsoft 
Outlook corporate servers. Script mods will be needed for other servers. In
general, the script is designed to intercept emails sent to a specific address,
extract one or more attached datafiles, parse the email for user and database
information, and insert the information into a database table. Each attached
datafile inserts into separate table rows. The target database is specified
in the username. The target database table is specified in the subject line.
The body of the email is inserted as user comments in the database table.
Finally, an email is sent to the user indicating whether the contents sent by 
the user were successfully inserted into the designated table. Transferring 
files to a database via email represents an extremely easy and intuitive method 
for moving data into a database. In addition, if the database server is public, 
files can be sent to a particular database from anywhere in the world, given 
an email client compatible with the parsing method used in eCo-PylotDB. The 
parsing method, of course, can be modified by someone familiar with email
formats, the code, and Python. Though easy and intuitive (most people are 
familiar with emailing), eCo-PylotDB does not capture as much information as 
the Co-Pylot interface. Users should compare descriptions between eCo-PylotDB 
and Co-PylotDB to determine which approach best fits their needs.
