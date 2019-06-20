# mysqldump -uroot -plt1116 hawkeye | gzip -c > /home/luotao/backup/hawkeye/`date +%d`.sql.gz

sudo -u postgres pg_dump hawkeye | gzip -c > /opt/backup/hawkeye/`date +%d`.sql.gz
