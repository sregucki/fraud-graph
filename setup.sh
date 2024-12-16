git lfs fetch --all
git lfs pull
mkdir -p ./.neo4j/import
cp ./data/*.csv ./.neo4j/import/
docker compose -f ./db/docker-compose.yml up -d
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
while ! curl localhost:7687; do sleep 5;done
python3 db/data_import.py
