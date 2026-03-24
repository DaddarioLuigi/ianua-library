"""Environment-backed config service."""

from ianuacare.core.config.env import EnvConfigService


def test_env_config_reads_prefixed_env(monkeypatch) -> None:
    monkeypatch.setenv("IANUA_DB_HOST", "localhost")
    cfg = EnvConfigService()
    assert cfg.get("db_host") == "localhost"


def test_env_config_prefers_explicit_settings(monkeypatch) -> None:
    monkeypatch.setenv("IANUA_DB_HOST", "localhost")
    cfg = EnvConfigService(settings={"db_host": "remote"})
    assert cfg.get("db_host") == "remote"
