# Filename: eco_pylot.py
# Author: Daniel W. Barnette
#         Sandia National Laboratories
#         Albuquerque, NM 87185
#         dwbarne@sandia.gov
#         dwbarne@gmail.com

#                          Disclaimer of Liability
# This work of authorship was prepared as an account of work sponsored by an agency 
# of the United States Government. Accordingly, the United States Government retains 
# a nonexclusive, royalty-free license to publish or reproduce the published form of
# this contribution, or allow others to do so for United States Government purposes. 
# Neither Sandia Corporation, the United States Government, nor any agency thereof, 
# nor any of their employees makes any warranty, express or implied, or assumes any
# legal liability or responsibility for the accuracy, completeness, or usefulness of 
# any information, apparatus, product, or process disclosed, or represents that its use 
# would not infringe privately-owned rights. Reference herein to any specific commercial
# product, process, or service by trade name, trademark, manufacturer, or otherwise does 
# not necessarily constitute or imply its endorsement, recommendation, or favoring by 
# Sandia Corporation, the United States Government, or any agency thereof. The views and 
# opinions expressed herein do not necessarily state or reflect those of Sandia Corporation, 
# the United States Government or any agency thereof.

# USAGE NOTES:

#   -- the .forward file and parse_mail command line
# email input from .forward file pipe and parse_mail command line, which are
# ---------
# .forward file, used for user "mantevo_data" in directory /home/mantevo_data:
# mantevo_data,"|/home/dwbarne/Parser/parse_mail"
# NOTES:
# 1. mantevo_data -- forwards email to /var/spool/mail, the typical path
# 2. "|/home/dwbarne/Parser/parse_mail" -- sends the email to be parsed by parse_mail
# ---------
# "parse_mail" command
# #!/bin/sh
# cat "$@" | /usr/bin/python /home/dwbarne/Parser/eco_pylot.py 1> output_eco_pylot.txt 2> errors.txt
# NOTES:
# 1. cat "$@" -- repeats the email msg so that it can be piped into the input for eco_pylot.py
# 2. rest of command runs the email msg through eco_pylot.py, with standard output going to
#    "output_eco_pylot.txt" and standard error going to "errors_eco_pylot.txt"
#
# Also note that all output will be generated in the /home/mantevo_data directory, which is
# the location of the .forward file, corresponding to user 'mantevo_data'
# ---------
# Any statements beginning with 'location_' will need to be changed 
#    to reflect the user's local environment. For example, the user will need to
#    define current location of eco_pylot.conf file.
#    However, if file does not exist, eCo_Pylot will generate the file in the same
#    directory as file "module_emailParser.py", i.e., the "Modules" directory. 
#  When first generated, the filename will be "eco_pylot.conf_template"; 
#    the user must then edit the file to define its parameters and rename the
#    file "eco_pylot.conf".
#  Next, make sure the file is in the "Modules" directory so "module_emailParser.py"
#    can find it.
#  Full path names must be used; full path names 
#    depend on whether the operating system is Windows or *nix.
# Any statements using 'dwbarne' will need to be changed as well.

# Sandia National Laboratories software license with Open-Source software license
SANDIA_COPYRIGHT_NOTICE = (
    'COPYRIGHT NOTICE\n' +
    '\n' +
    'Copyright 2012 Sandia Corporation. Under the terms of Contract\n' +
    'DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government\n' +
    'retains certain rights in this software.'
    )

OPEN_SOURCE_SOFTWARE_LICENSE = (
    ' '*20 + 'OPEN SOURCE SOFTWARE LICENSE\n' +
    '\n' +
    'Redistribution and use in source and binary forms, with or without ' +
    'modification, are permitted provided that the following conditions ' +
    'are met:\n' +
    '\n' +
    '   * Redistributions of source code must retain the above copyright\n' +
    '     copyright notice, this list of conditions and the following\n' +
    '     disclaimer.\n' +
    '\n' +
    '   * Redistributions in binary form must reproduce the above\n' +
    '     copyright notice, this list of conditions, and the following\n' +
    '     disclaimer in the documentation and/or other materials provided\n' +
    '     with the distribution.\n' +
    '\n' +
    '   * Neither the name of Sandia Corporation nor the names of its\n' +
    '     contributors may be used to endorse or promote products\n' +
    '     derived from this software without specific prior written\n' +
    '     permission.\n' +
    '\n' +
    'THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ' +
    '"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,INCLUDING, BUT NOT ' +
    'LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ' +
    'A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT ' +
    'OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, ' +
    'SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT ' +
    'LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, ' +
    'DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY ' +
    'THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT ' +
    '(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE ' +
    'OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n' +
    '\n' +
    'Suggested reference wording for articles:\n' +
    '\n' +
    'D. W. Barnette, "PYLOTDB: A Python-MySQL Framework for Database Management ' +
    'and Data Analysis," Sandia National Laboratories, Albuquerque, New Mexico, 2012.'
    )
    
# Sandia National Laboratories software license with Open-Source software license attached
licenseSandia = (
    ' '*5 + 'COPYRIGHT NOTICE AND OPEN SOURCE LICENSE\n' +
    '\n' +
    'Copyright 2012 Sandia Corporation. Under the terms of Contract ' +
    'DE-AC04-94AL85000 with Sandia Corporation, the U.S. ' +
    'Government retains certain rights in this software.\n' +
    '\n' +
    'Redistribution and use in source and binary forms, with or without ' +
    'modification, are permitted provided that the following conditions ' +
    'are met:\n' +
    '\n' +
    '   * Redistributions of source code must retain the above copyright\n' +
    '     copyright notice, this list of conditions and the following\n' +
    '     disclaimer.\n' +
    '\n' +
    '   * Redistributions in binary form must reproduce the above\n' +
    '     copyright notice, this list of conditions, and the following\n' +
    '     disclaimer in the documentation and/or other materials provided\n' +
    '     with the distribution.\n' +
    '\n' +
    '   * Neither the name of Sandia Corporation nor the names of its\n' +
    '     contributors may be used to endorse or promote products\n' +
    '     derived from this software without specific prior written\n' +
    '     permission.\n' +
    '\n' +
    'THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ' +
    '"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT ' +
    'LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ' +
    'A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT ' +
    'OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, ' +
    'SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT ' +
    'LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, ' +
    'DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY ' +
    'THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT ' +
    '(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE ' +
    'OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n' +
    '\n' +
    'Suggested reference wording for articles:\n' +
    '\n' +
    'D. W. Barnette, "PYLOTDB: A Python-MySQL Framework for Database Management ' +
    'and Data Analysis," Sandia National Laboratories, Albuquerque, New Mexico, 2012.'
    )

#=================================================

# imports
# ... for platform characteristics
import sys
# ... for time stamps
import time

# constants for debugging
PRINT_eCO_PYLOT_MAIN = 1        # =1, verbose output

# module search path for...
opsys = sys.platform[:3]

# define where modules reside; usual location is within Modules directory
#   which is located in directory containing eCo_Pylot.py
# ... windows
if opsys == 'win':
    sys.path.append('.\\Modules')
# ... *nix
else:
    sys.path.append('/home/dwbarne/Parser/Modules')
    
if opsys == 'win':
    location_eco_pylot_dot_conf_file = (
        './eco_pylot.conf'
        )    
else:
    location_eco_pylot_dot_conf_file = (
        '/home/dwbarne/Parser/Modules/eco_pylot.conf'
        )
location_eco_pylot_dot_conf_template_file = location_eco_pylot_dot_conf_file
    
# import module(s)
import module_emailParser

localDateTime = time.ctime()

# output file
fileOut = open('./eco_pylot_Out.txt','w')
fileOut.write('eCo_Pylot is running at time = %s' % localDateTime)

if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nReading msg from stdin ...')
msg = sys.stdin.read()
if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nEmail has been read as follows:\n\n')
    fileOut.write('----- START EMAIL -----\n')
    fileOut.write(msg)
    fileOut.write('\n----- END EMAIL -----\n')

# check if msg is a proper email msg
if len(msg) > 0:
# instantiate class
    if PRINT_eCO_PYLOT_MAIN:
        fileOut.write('\nCalling module_emailParser.EmailParser(msg)')
        
# instantiate the EmailParser class in module module_emailParser
    email2db = module_emailParser.EmailParser(
        msg,
        location_eco_pylot_dot_conf_file,
        location_eco_pylot_dot_conf_template_file
        )
# if any error msgs, tell user via email and quit
#    if PRINT_eCO_PYLOT_MAIN:
#        fileOut.write('\nCalling email2db.exit_eCo_Pylot(\'EmailParser\')')
#    email2db.exit_eCo_Pylot('EmailParser')
    
# msg length is zero
else:
    if PRINT_eCO_PYLOT_MAIN:
        fileOut.write(
            '\nERROR: zero email length\n' +
            ' Email length sent to eCo-Pylot is zero.\n' +
            ' eCo-Pylot is unable to continue, so program is stopping.\n\n'
            )
    sys.exit()


# ... read configure file
#if PRINT_eCO_PYLOT_MAIN:
#    fileOut.write('\nCalling email2db.readConfigureFileForEcoPylot()')
email2db.readConfigureFileForEcoPylot()
#if PRINT_eCO_PYLOT_MAIN:
#    fileOut.write('\nCalling email2db.exit_eCo_Pylot(\'readConfigureFileForEcoPylot\')')
##email2db.exit_eCo_Pylot('readConfigureFileForEcoPylot')
    
# ... parse email
if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nCalling email2db.parse()')
email2db.parse()
if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nCalling email2db.exit_eCo_Pylot(\'parse\')')
##email2db.exit_eCo_Pylot('parse')

# ... connect to MySQL database
if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nCalling email2db.mySQLConnect()')
email2db.mySQLConnect()
if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nCalling email2db.exit_eCo_Pylot(\'mySQLConnect\')')
email2db.exit_eCo_Pylot('mySQLConnect')

# ... send data and files to database
if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nCalling email2db.send2db()')
email2db.send2db()
if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nCalling email2db.exit_eCo_Pylot(\'send2db\')')
email2db.exit_eCo_Pylot('send2db')

# ... send some email to user
if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nCalling email2db.email2user()')
email2db.email2user()
if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nCalling email2db.exit_eCo_Pylot(\'email2user\')')
email2db.exit_eCo_Pylot('email2user')
    
# ... track usage
if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nCalling email2db.trackUsage()')
email2db.trackUsage()
if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nCalling email2db.exit_eCo_Pylot(\'trackUsage\')')
email2db.exit_eCo_Pylot('trackUsage')

# ... finish
if PRINT_eCO_PYLOT_MAIN:
    fileOut.write('\nCalling email2db.exit_eCo_Pylot(\'finished\')')
email2db.exit_eCo_Pylot('finished')


