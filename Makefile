# Danger Rose - Game Development Makefile
# Simple commands for Windows, macOS, and Linux

# Default target
.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help message
	@echo "Danger Rose - Make Commands"
	@echo "==========================="
	@echo ""
	@echo "Game Commands:"
	@echo "  make run          Run the game"
	@echo "  make debug        Run in debug mode"
	@echo "  make build        Build executable"
	@echo ""
	@echo "Development Commands:"
	@echo "  make test         Run all tests"
	@echo "  make coverage     Run tests with coverage"
	@echo "  make lint         Check code style"
	@echo "  make format       Auto-format code"
	@echo "  make clean        Clean build artifacts"
	@echo ""

# ========== GAME COMMANDS ==========

.PHONY: run
run: ## Run the game
	@echo "🎮 Starting Danger Rose..."
	@python src/main.py

.PHONY: debug
debug: ## Run the game in debug mode
	@echo "🐛 Starting in debug mode..."
	@DEBUG=true python src/main.py

.PHONY: build
build: ## Build standalone executable
	@echo "📦 Building executable..."
	@pyinstaller danger-rose.spec --noconfirm
	@echo "✅ Build complete! Check dist/ folder"

# ========== DEVELOPMENT COMMANDS ==========

.PHONY: test
test: ## Run all tests
	@echo "🧪 Running tests..."
	@pytest tests/unit -v

.PHONY: test-all
test-all: ## Run all tests including integration
	@echo "🧪 Running all tests..."
	@pytest tests/ -v

.PHONY: coverage
coverage: ## Run tests with coverage report
	@echo "📊 Running coverage analysis..."
	@pytest tests/unit --cov=src --cov-report=html --cov-report=term
	@echo "📊 Coverage report generated in htmlcov/"

.PHONY: lint
lint: ## Run code linting
	@echo "🔍 Checking code style..."
	@ruff check src/ tests/

.PHONY: format
format: ## Format code
	@echo "💅 Formatting code..."
	@ruff format src/ tests/
	@ruff check src/ tests/ --fix

.PHONY: clean
clean: ## Clean build artifacts
	@echo "🧹 Cleaning up..."
	@python -c "import shutil, os; [shutil.rmtree(d, ignore_errors=True) for d in ['build', 'dist', '__pycache__', '.pytest_cache', 'htmlcov', '.coverage', '.mypy_cache', '.ruff_cache']]; [os.remove(f) for f in ['*.spec'] if os.path.exists(f)]"
	@echo "✨ Clean!"

# ========== SPECIAL COMMANDS ==========

.PHONY: assets-check
assets-check: ## Validate all game assets exist
	@echo "🎨 Checking assets..."
	@python tools/check_assets.py

.PHONY: test-visual
test-visual: ## Run visual debug tools
	@echo "👁️ Running visual tests..."
	@python tools/visual/test_sprite_cutting.py
	@echo "Check test-artifacts/ directory for results"

.PHONY: profile
profile: ## Profile game performance
	@echo "⚡ Profiling game..."
	@python -m cProfile -o profile.stats src/main.py
	@echo "Profile saved to profile.stats"