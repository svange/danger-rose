import pytest
import pygame
import sys
import os
from pathlib import Path
from unittest.mock import patch

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="session", autouse=True)
def init_pygame_headless():
    """Initialize pygame in headless mode for CI/CD environments."""
    # Set SDL to use dummy video driver for headless operation
    os.environ["SDL_VIDEODRIVER"] = "dummy"

    # Initialize pygame modules
    pygame.init()

    # Set a dummy display for tests that require it
    try:
        pygame.display.set_mode((1, 1))
    except pygame.error:
        # If dummy driver fails, we're likely in a real headless environment
        pass

    yield

    pygame.quit()


@pytest.fixture
def mock_pygame_display():
    """Mock pygame display for tests that need display but shouldn't create windows."""
    with patch("pygame.display.set_mode") as mock_display:
        mock_surface = pygame.Surface((100, 100))
        mock_display.return_value = mock_surface
        yield mock_display


@pytest.fixture
def suppress_pygame_output():
    """Suppress pygame welcome message and other output during tests."""
    import os
    import sys

    # Redirect stdout to devnull during pygame import
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")

    yield

    sys.stdout.close()
    sys.stdout = original_stdout
