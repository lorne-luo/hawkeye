/home/luotao/venv/hawkeye/bin/python /opt/hawkeye/manage.py dumpdata --indent 4 | gzip -c > /opt/backup/hawkeye/`date +%d`.json.gz
