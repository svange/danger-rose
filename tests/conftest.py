import pytest
import pygame
import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    """Initialize pygame for all tests."""
    pygame.init()
    yield
    pygame.quit()