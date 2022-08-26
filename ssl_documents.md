# Secure Connection Implementation to v1.6 (SSL)

1- First we need to create keys that includes ssh protocol informations.

```bash
openssl req -x509 -nodes -new -sha256 -days 1024 -newkey rsa:2048 -keyout key.pem -out cert.pem -subj "/C=US/CN=localhost"
cat key.pem cert.pem > key_cert.pem
```

2-  Move cert.pem and keycert.pem to `example/v16`

3-   then run these scripts.

```bash
python central_system.py
python charge_point.py
```

## Change Logs
Changes On central_system.py

```python3

async def main():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    localhost_pem = pathlib.Path(__file__).with_name("key_cert.pem")
    ssl_context.load_cert_chain(localhost_pem)
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp1.6'],
        ssl=ssl_context,
    )
```

Changes On charge_point.py

```python3
async def main():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    localhost_pem = pathlib.Path(__file__).with_name("cert.pem")
    ssl_context.load_verify_locations(localhost_pem)
    async with websockets.connect(
        'wss://localhost:9000/CP_1',
        subprotocols=['ocpp1.6'],
        ssl=ssl_context,
    ) as ws:
        cp = ChargePoint('CP_1', ws)
        await asyncio.gather(cp.start(), cp.send_boot_notification())
```