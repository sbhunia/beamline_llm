import requests

def check_ollama_health(base_url="http://127.0.0.1:11434"):
    try:
        resp = requests.get(f"{base_url}/api/tags", timeout=5)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            print(f"✅ Ollama is running. Available models: {models}")
            return True
        else:
            print(f"⚠️ Ollama responded with status {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama not reachable: {e}")
        return False


if __name__ == "__main__":
    check_ollama_health()
