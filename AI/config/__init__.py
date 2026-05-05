from config.environment import Settings, get_settings

settings: Settings = get_settings()
settings.export_to_os_environ()

__all__ = ["Settings", "get_settings", "settings"]
