# cd /Users/subose/testWorkspace/searchBot/
# cd to path to repo
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi
pip install "uvicorn[standard]"
uvicorn main:app --reload --port 8085