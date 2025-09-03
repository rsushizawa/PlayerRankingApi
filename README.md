## On VM
```
git clone https://github.com/rsushizawa/PlayerRankingApi.git
```

```
sudo apt install python3-venv
```

```
python3 -m venv venv
source venv/bin/activate
pip install FastApi pydantic uvicorn
uvicor main:app --host 0.0.0.0 --port 3000
```

## With Docker

```
docker-compose up --build -d

docker-compose logs -f

docker-compose down

```
