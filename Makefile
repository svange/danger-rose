# Danger Rose - Game Development Makefile
# Supports Windows (Git Bash), macOS, and Linux

# Detect OS for platform-specific commands
ifeq ($(OS),Windows_NT)
    PYTHON := python
    RM := del /F /Q
    RMDIR := rmdir /S /Q
    SEP := \\
    CLEAR := cls
    # Use Git Bash if available
    ifdef MSYSTEM
        RM := rm -f
        RMDIR := rm -rf
        SEP := /
        CLEAR := clear
    endif
else
    PYTHON := python3
    RM := rm -f
    RMDIR := rm -rf
    SEP := /
    CLEAR := clear
endif

# Poetry command - uses poetry if available, otherwise direct python
POETRY_CHECK := $(shell command -v poetry 2> /dev/null)
ifdef POETRY_CHECK
    RUN := poetry run
else
    RUN := $(PYTHON)
endif

# Default target
.DEFAULT_GOAL := help

# Colors for output (works in most terminals)
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# Print colored output
define print_msg
	@echo "$(1)$(2)$(RESET)"
endef

.PHONY: help
help: ## Show this help message
	@echo "$(CYAN)Danger Rose - Make Commands$(RESET)"
	@echo "$(CYAN)============================$(RESET)"
	@echo ""
	@echo "$(GREEN)Game Commands:$(RESET)"
	@grep -E '^(run|debug|build).*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Development Commands:$(RESET)"
	@grep -E '^(test|lint|format|check).*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Asset Commands:$(RESET)"
	@grep -E '^(assets|sprites|validate).*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Utility Commands:$(RESET)"
	@grep -E '^(clean|install|setup).*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Kid-Friendly Commands:$(RESET)"
	@grep -E '^(kids|play|easy).*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'

# ========== GAME COMMANDS ==========

.PHONY: run
run: ## Run the game
	$(call print_msg,$(GREEN),"🎮 Starting Danger Rose...")
	$(RUN) python src/main.py

.PHONY: debug
debug: ## Run game in debug mode with FPS counter
	$(call print_msg,$(GREEN),"🐛 Starting in debug mode...")
	DEBUG=true SHOW_FPS=true $(RUN) python src/main.py

.PHONY: run-ski
run-ski: ## Run ski minigame directly
	$(call print_msg,$(GREEN),"🎿 Starting Ski minigame...")
	SCENE=ski $(RUN) python src/main.py

.PHONY: run-pool
run-pool: ## Run pool minigame directly
	$(call print_msg,$(GREEN),"🏊 Starting Pool minigame...")
	SCENE=pool $(RUN) python src/main.py

.PHONY: run-vegas
run-vegas: ## Run vegas minigame directly
	$(call print_msg,$(GREEN),"🎰 Starting Vegas minigame...")
	SCENE=vegas $(RUN) python src/main.py

.PHONY: build
build: clean test ## Build executable for current platform
	$(call print_msg,$(CYAN),"📦 Building executable...")
	$(RUN) pyinstaller danger-rose.spec
	$(call print_msg,$(GREEN),"✅ Build complete! Check dist/ folder")

.PHONY: build-all
build-all: clean test ## Build executables for all platforms
	$(call print_msg,$(CYAN),"📦 Building for all platforms...")
	$(RUN) python tools/build_all_platforms.py
	$(call print_msg,$(GREEN),"✅ All builds complete!")

# ========== DEVELOPMENT COMMANDS ==========

.PHONY: test
test: ## Run all tests
	$(call print_msg,$(CYAN),"🧪 Running tests...")
	$(RUN) pytest tests/ -v

.PHONY: test-fast
test-fast: ## Run only fast tests
	$(call print_msg,$(CYAN),"⚡ Running fast tests...")
	$(RUN) pytest tests/ -v -m fast

.PHONY: test-game
test-game: ## Run specific game tests
	$(call print_msg,$(CYAN),"🎮 Running game tests...")
	$(RUN) pytest tests/test_scenes/ tests/test_game_mechanics/ -v

.PHONY: test-visual
test-visual: ## Run visual regression tests
	$(call print_msg,$(CYAN),"👁️ Running visual tests...")
	$(RUN) pytest tests/visual/ -v

.PHONY: coverage
coverage: ## Run tests with coverage report
	$(call print_msg,$(CYAN),"📊 Running coverage...")
	$(RUN) pytest --cov=src --cov-report=html --cov-report=term
	$(call print_msg,$(GREEN),"📊 Coverage report: htmlcov/index.html")

.PHONY: lint
lint: ## Run code linting
	$(call print_msg,$(CYAN),"🔍 Checking code style...")
	$(RUN) ruff check src/ tests/

.PHONY: format
format: ## Format code with Black
	$(call print_msg,$(CYAN),"✨ Formatting code...")
	$(RUN) black src/ tests/
	$(RUN) ruff check src/ tests/ --fix

.PHONY: check
check: lint test ## Run all checks (lint + test)
	$(call print_msg,$(GREEN),"✅ All checks passed!")

# ========== ASSET COMMANDS ==========

.PHONY: assets-validate
assets-validate: ## Validate all game assets
	$(call print_msg,$(CYAN),"🎨 Validating assets...")
	$(RUN) python tools/validate_assets.py

.PHONY: sprites-cut
sprites-cut: ## Cut sprite sheets into frames
	$(call print_msg,$(CYAN),"✂️ Cutting sprite sheets...")
	$(RUN) python tools/cut_sprites.py

.PHONY: assets-optimize
assets-optimize: ## Optimize all assets for size
	$(call print_msg,$(CYAN),"📦 Optimizing assets...")
	$(RUN) python tools/optimize_assets.py

.PHONY: assets-download
assets-download: ## Download required free assets
	$(call print_msg,$(CYAN),"⬇️ Downloading assets...")
	$(RUN) python tools/download_assets.py

# ========== UTILITY COMMANDS ==========

.PHONY: install
install: ## Install all dependencies
	$(call print_msg,$(CYAN),"📦 Installing dependencies...")
	poetry install

.PHONY: install-dev
install-dev: ## Install with dev dependencies
	$(call print_msg,$(CYAN),"📦 Installing dev dependencies...")
	poetry install --with dev

.PHONY: setup
setup: install assets-download ## Complete project setup
	$(call print_msg,$(GREEN),"✅ Setup complete! Run 'make play' to start!")

.PHONY: clean
clean: ## Clean build artifacts and cache
	$(call print_msg,$(CYAN),"🧹 Cleaning up...")
	$(RMDIR) build dist __pycache__ .pytest_cache htmlcov .coverage 2>nul || true
	$(RMDIR) src$(SEP)__pycache__ tests$(SEP)__pycache__ 2>nul || true
	$(RM) *.pyc *.pyo *.spec 2>nul || true
	$(call print_msg,$(GREEN),"✨ Clean complete!")

.PHONY: clean-saves
clean-saves: ## Delete all save files (warning!)
	$(call print_msg,$(YELLOW),"⚠️  Deleting save files...")
	$(RMDIR) saves 2>nul || true
	$(call print_msg,$(GREEN),"🗑️ Save files deleted!")

# ========== KID-FRIENDLY COMMANDS ==========

.PHONY: play
play: ## Start the game (same as 'run')
	@$(MAKE) run

.PHONY: kids
kids: ## Run in kid-friendly mode
	$(call print_msg,$(GREEN),"👶 Starting kid-friendly mode...")
	KID_MODE=true $(RUN) python src/main.py

.PHONY: easy-test
easy-test: ## Run simple tests with fun output
	$(call print_msg,$(GREEN),"🌈 Running fun tests...")
	$(RUN) pytest tests/ -v --tb=short -q

.PHONY: help-me
help-me: ## Get help with an error
	$(call print_msg,$(CYAN),"💡 Opening help guide...")
	$(RUN) python tools/error_helper.py

# ========== DEVELOPMENT TOOLS ==========

.PHONY: create-scene
create-scene: ## Create a new game scene
	$(call print_msg,$(CYAN),"🎬 Creating new scene...")
	@read -p "Scene name: " scene; \
	$(RUN) python tools/create_scene.py $$scene

.PHONY: create-test
create-test: ## Create a test file
	$(call print_msg,$(CYAN),"🧪 Creating test file...")
	@read -p "Test name: " test; \
	$(RUN) python tools/create_test.py $$test

.PHONY: profile
profile: ## Profile game performance
	$(call print_msg,$(CYAN),"📊 Profiling performance...")
	PROFILE=true $(RUN) python src/main.py

.PHONY: memory
memory: ## Check memory usage
	$(call print_msg,$(CYAN),"🧠 Checking memory...")
	MEMORY_PROFILE=true $(RUN) python src/main.py

# ========== CI/CD COMMANDS ==========

.PHONY: ci
ci: check coverage ## Run CI pipeline locally
	$(call print_msg,$(GREEN),"✅ CI checks passed!")

.PHONY: release
release: ## Prepare a new release
	$(call print_msg,$(CYAN),"🚀 Preparing release...")
	$(RUN) python tools/prepare_release.py

# ========== SPECIAL COMMANDS ==========

.PHONY: celebrate
celebrate: ## Celebrate your progress! 🎉
	$(call print_msg,$(GREEN),"🎉 Great job! You're awesome! 🎉")
	$(call print_msg,$(YELLOW),"⭐ ⭐ ⭐ ⭐ ⭐")
	$(call print_msg,$(CYAN),"Keep coding and having fun!")

.PHONY: family-mode
family-mode: ## Enable family development mode
	$(call print_msg,$(GREEN),"👨‍👩‍👧‍👦 Family mode activated!")
	$(call print_msg,$(CYAN),"- Simple error messages enabled")
	$(call print_msg,$(CYAN),"- Visual feedback enhanced")
	$(call print_msg,$(CYAN),"- Learning helpers active")
	FAMILY_MODE=true $(RUN) python src/main.py

# Windows-specific warning
ifeq ($(OS),Windows_NT)
ifndef MSYSTEM
.PHONY: windows-warning
windows-warning:
	$(call print_msg,$(YELLOW),"⚠️  Note: Some commands work better in Git Bash on Windows")
endif
endif