if [ "$1" != "" ]; then
    mkdir -p data/$1
    ssh -t luotao@luotao "cd /opt/hawkeye/data/$1/ && zip csv.zip -qr csv/"
    scp luotao@luotao:/opt/hawkeye/data/$1/csv.zip ./data/$1/
    ssh -t luotao@luotao "rm -rf /opt/hawkeye/data/$1/csv.zip"
    scp luotao@luotao:/opt/hawkeye/data/$1/result.csv ./data/$1/result.csv
    unzip -qo data/$1/csv.zip -d data/$1/
    rm -rf data/$1/csv.zip
fi
