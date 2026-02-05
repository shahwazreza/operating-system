#!/usr/bin/bash
# Reza Shahwaz
# CS 380-BX1

# Part I: The Clallenges
# Processes and Daemons

# 1. List a specific process (nginx)
ps aux | grep nginx

# 2. Kill by name
pkill -f  my_script.sh

# 3. Background execution
nohup ./backup.sh &

# 4. Find PID (sshd daemon)
pidof sshd

# 5. Process Hierarchy
pstree -p

# 6. Open file by PID 1234
lsof - p 1234

# 7. Check docker daemon status
systemctl status docker

# 8. Run heavy_cals.sh with lowest priority
nice -n 19 ./heavy_calc.sh


# Files, Copying and Archiving


# 9. Recursive Copy
cp -r /var/www/html /backup/html

# 10. Preserve Attributes
cp -p secret.key/tmp

# 11. Sync Directories
rsync -av --ignore-existing src/dest/

# 12. Update Copy
cd -u dir1/* dir2/

# 13. Remote Copy
scp app.conf user@192.168.1.50:/etc/

# 14. Archive and Compress
tar -czvf var_log.tar.gz /var/log


# The find Command


# 15. Size Search
find /home -type f -size +500M

# 16. Time Search
find /var/log -type f -mtime -7

#17. User Search
find /tmp -type f -user jenkins

#18. Find and Delete
find /data -type d -empty -exec rmdir {} \;

# 19. Permission Search
find . -type f -perm 0777

# 20. Find and Copy
find . -type f -name "*.jpg" -exec cp {} /images/ \;


# Regular Expressions (Grep, Sed, Awk)


# 21. Email Extraction
grep -E -o "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}" contacts.txt

# 22. Case Insensitive Search
grep -i "error" syslog

# 23. Line Start Anchor
grep "^root" config.ini

# 24. Invert Match
grep -v "192.168.1.1" access.log

#25. Recursive Grep
grep -r "TODO" *.txt

#26. Sed Replace
sed -i 's/localhost/127.0.0.1/g' hosts.txt

#27. Comment Removal
grep -v "^#" config.ini

# 28. IP validation
grep -E "^([0-9]{1,3}\.){3}[0-9]{1,3}$" file.txt


# Complex and Combinations


# 29. Process and Regex
ps aux | grep "^root"

# 30. Find, Regex and Execute
find . -type f -name "*.log" -exec grep -l "Critical" {} \;

