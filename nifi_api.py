"""Cliente da NiFi REST API (single-user / JWT).

NiFi 2.x com single-user provider: o login nao e via header Basic,
e via POST em /nifi-api/access/token (form username/password) que
retorna um JWT. Esse modulo encapsula isso e expoe os endpoints
mais uteis para inspecionar/gerenciar o fluxo.

Uso rapido (linha de comando):
    python3 nifi_api.py status
    python3 nifi_api.py flows
    python3 nifi_api.py processors
"""

import json
import sys

import requests

NIFI_URL = "https://localhost:8443/nifi-api"
USERNAME = "admin"
PASSWORD = "SenhaForte123!"


def get_token() -> str:
    """Autentica e retorna o JWT (validade ~1h neste NiFi)."""
    r = requests.post(
        f"{NIFI_URL}/access/token",
        data={"username": USERNAME, "password": PASSWORD},  # form-encoded
        verify=False,          # certificado self-signed do container
        timeout=10,
    )
    if r.status_code != 201:
        raise RuntimeError(f"Login falhou (HTTP {r.status_code}): {r.text}")
    return r.text.strip()


class NifiApi:
    def __init__(self, url: str = NIFI_URL, token: str | None = None):
        self.url = url.rstrip("/")
        self.token = token or get_token()
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers["Authorization"] = f"Bearer {self.token}"

    def _get(self, path: str) -> dict:
        r = self.session.get(f"{self.url}/{path.lstrip('/')}", timeout=15)
        if r.status_code == 401:
            # token expirou -> renova e tenta de novo
            self.token = get_token()
            self.session.headers["Authorization"] = f"Bearer {self.token}"
            r = self.session.get(f"{self.url}/{path.lstrip('/')}", timeout=15)
        return {"status": r.status_code, "json": _safe_json(r)}

    # ---- endpoints mais uteis -------------------------------------------
    def root_process_group(self):
        """Arvore do fluxo (root group)."""
        return self._get("flow/process-groups/root")

    def process_groups(self):
        """Lista de grupos de processo."""
        return self._get("process-groups")

    def controller_services(self):
        """Controller services criados (ex.: DatabaseConnection)."""
        return self._get("controller-services")

    def flow_files_queued(self, processor_id: str):
        """Quantidade de FlowFiles parados em cada conexao de um processador."""
        return self._get(f"process-groups/root/process-processors/{processor_id}/queued")


def _safe_json(r) -> dict | list:
    try:
        return r.json()
    except ValueError:
        return {"raw": r.text}


def main():
    requests.packages.urllib3.disable_warnings()  # silencia aviso do self-signed cert
    api = NifiApi()

    if len(sys.argv) > 1 and sys.argv[1] == "status":
        g = api.root_process_group()["json"]
        grp = g.get("processGroup", {})
        print(f"NiFi acessivel. FlowFiles no root: {grp.get('flowFilesQueued')}")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "flows":
        g = api.root_process_group()["json"]
        for pg in [g["processGroup"]] + g.get("childProcessGroups", []):
            print(f"  grupo: {pg['name']} (id={pg['id']})")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "processors":
        g = api.root_process_group()["json"]
        for p in g.get("processProcessors", []):
            print(f"  {p['name']} [{p['componentType']}] estado={p.get('state')}")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "services":
        r = api.controller_services()["json"]
        for s in r.get("controllerServices", []):
            print(f"  {s['name']} [{s['componentType']}]")
        return

    print(json.dumps(api.root_process_group()["json"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    main()