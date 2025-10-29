"""Plugin management system for the Personal Assistant."""

from typing import Dict, List, Any, Type
import importlib
import inspect
from pathlib import Path
import logging

from src.core.config import Config
from src.core.plugin_base import BasePlugin
from src.utils.exceptions import PluginError

logger = logging.getLogger(__name__)


class PluginManager:
    """Manages loading and execution of plugins."""

    def __init__(self, config: Config):
        """Initialize the plugin manager.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugin_directory = Path("src/plugins")

    def load_plugins(self) -> None:
        """Discover and load all available plugins."""
        if not self.plugin_directory.exists():
            logger.warning(f"Plugin directory {self.plugin_directory} does not exist")
            return

        for plugin_file in self.plugin_directory.glob("*.py"):
            if plugin_file.name.startswith("__"):
                continue
                
            try:
                self._load_plugin_from_file(plugin_file)
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_file}: {e}")

    def _load_plugin_from_file(self, plugin_file: Path) -> None:
        """Load a plugin from a Python file.
        
        Args:
            plugin_file: Path to the plugin file
        """
        module_name = f"src.plugins.{plugin_file.stem}"
        
        try:
            module = importlib.import_module(module_name)
            
            # Find plugin classes in the module
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, BasePlugin) and 
                    obj != BasePlugin and 
                    getattr(obj, '__module__', '') == module_name):
                    
                    plugin_config = self.config.plugins.get(plugin_file.stem, {})
                    plugin_instance = obj(plugin_config)
                    
                    self.plugins[plugin_file.stem] = plugin_instance
                    logger.info(f"Loaded plugin: {name}")
                    
        except Exception as e:
            raise PluginError(f"Failed to load plugin from {plugin_file}: {e}")

    def get_plugin(self, name: str) -> BasePlugin:
        """Get a plugin by name.
        
        Args:
            name: Plugin name
            
        Returns:
            Plugin instance
            
        Raises:
            PluginError: If plugin not found
        """
        if name not in self.plugins:
            raise PluginError(f"Plugin '{name}' not found")
        return self.plugins[name]

    def list_plugins(self) -> List[str]:
        """Get list of loaded plugin names.
        
        Returns:
            List of plugin names
        """
        return list(self.plugins.keys())

    def get_capabilities(self) -> Dict[str, Any]:
        """Get capabilities of all loaded plugins.
        
        Returns:
            Dictionary of plugin capabilities
        """
        capabilities = {}
        for name, plugin in self.plugins.items():
            capabilities[name] = plugin.get_capabilities()
        return capabilities