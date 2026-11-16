"""Vista local con fixture temporal; nunca usa datos ni configuración escolar."""
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / 'tests'))
from test_auditoria import SistemaTest, api

if __name__ == '__main__':
    fixture = SistemaTest()
    fixture.setUp()
    api.app.config.update(SESSION_COOKIE_SECURE=False, TESTING=False)
    print('Vista ficticia: http://127.0.0.1:8765. Cuentas definidas en tests/test_auditoria.py.')
    try:
        api.app.run(host='127.0.0.1', port=8765, use_reloader=False)
    finally:
        fixture.doCleanups()
