#!/bin/bash

LOGFILE="server.log"

# Create a dummy log file

cat <<EOF > $LOGFILE
Serverstarted successfully
Error: Connection failed
User logged in
Error: Disk not found
Error: timeout occured
EOF

COUNT=$(grep -c "Error" "$LOGFILE")
echo "Number of lines containing 'Error': $COUNT"
