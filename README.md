# fast-proxy
HTTP back-proxy service based on FastAPI

## Requirements
```pip install -r requirements.txt```

## Configuration
Check `src/config.py` file for runtime configs and `src/pools.yaml` for proxy pools configuration

## Run
```
cd src
uvicorn proxy:app
```
Proxy server host by default: ` http://127.0.0.1:8000`

For more details refer to https://fastapi.tiangolo.com/deployment/manually/#run-the-server-program, including extra workers for better performance.