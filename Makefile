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
	@echo "  make run-ski      Run ski minigame directly"
	@echo "  make run-pool     Run pool minigame directly"
	@echo "  make run-vegas    Run vegas minigame directly"
	@echo "  make kids         Run in kid-friendly mode"
	@echo ""
	@echo "Build Commands:"
	@echo "  make build        Build executable for current platform"
	@echo "  make build-all    Build for all platforms"
	@echo "  make clean-build  Clean build artifacts only"
	@echo ""
	@echo "Development Commands:"
	@echo "  make test         Run unit tests"
	@echo "  make test-game    Run game tests only"
	@echo "  make test-all     Run all tests including integration"
	@echo "  make test-visual  Run visual debug tools"
	@echo "  make coverage     Run tests with coverage report"
	@echo "  make check        Run all checks (lint + test)"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         Check code style"
	@echo "  make format       Auto-format code"
	@echo "  make security     Run security checks"
	@echo ""
	@echo "Asset Management:"
	@echo "  make assets-check Validate all game assets"
	@echo "  make sprites      Generate sprite test output"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean        Clean all artifacts"
	@echo "  make profile      Profile game performance"
	@echo "  make celebrate    Celebrate achievements!"
	@echo ""

# ========== GAME COMMANDS ==========

.PHONY: run
run: ## Run the game
	@echo "🎮 Starting Danger Rose..."
	@ python src/main.py

.PHONY: debug
debug: ## Run the game in debug mode
	@echo "🐛 Starting in debug mode..."
	@DEBUG=true poetry run python src/main.py

.PHONY: run-ski
run-ski: ## Run ski minigame directly
	@echo "⛷️  Starting ski minigame..."
	@SCENE=ski poetry run python src/main.py

.PHONY: run-pool
run-pool: ## Run pool minigame directly
	@echo "🏊 Starting pool minigame..."
	@SCENE=pool poetry run python src/main.py

.PHONY: run-vegas
run-vegas: ## Run vegas minigame directly
	@echo "🎰 Starting Vegas minigame..."
	@SCENE=vegas poetry run python src/main.py

.PHONY: kids
kids: ## Run in kid-friendly mode
	@echo "👶 Starting in kid-friendly mode..."
	@KID_MODE=true poetry run python src/main.py

.PHONY: build
build: ## Build standalone executable
	@echo "📦 Building executable..."
	@ pyinstaller danger-rose.spec --noconfirm
	@echo "✅ Build complete! Check dist/ folder"

.PHONY: build-all
build-all: ## Build for all platforms
	@echo "📦 Building for all platforms..."
	@echo "Note: Cross-platform builds require platform-specific builders"
	@ pyinstaller danger-rose.spec --noconfirm
	@echo "✅ Current platform build complete!"

.PHONY: clean-build
clean-build: ## Clean build artifacts only
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build dist *.spec 2>/dev/null || true
	@echo "✨ Build artifacts cleaned!"

# ========== DEVELOPMENT COMMANDS ==========

.PHONY: test
test: ## Run unit tests
	@echo "🧪 Running unit tests..."
	@ pytest tests/unit -v

.PHONY: test-game
test-game: ## Run game tests only
	@echo "🎮 Running game-specific tests..."
	@ pytest tests/unit tests/integration -v -k "not test_visual"

.PHONY: test-all
test-all: ## Run all tests including integration
	@echo "🧪 Running all tests..."
	@ pytest tests/ -v

.PHONY: coverage
coverage: ## Run tests with coverage report
	@echo "📊 Running coverage analysis..."
	@ pytest tests/unit --cov=src --cov-report=html --cov-report=term
	@echo "📊 Coverage report generated in htmlcov/"

.PHONY: check
check: lint test ## Run all checks (lint + test)
	@echo "✅ All checks passed!"

.PHONY: lint
lint: ## Run code linting
	@echo "🔍 Checking code style..."
	@ ruff check src/ tests/

.PHONY: format
format: ## Format code
	@echo "💅 Formatting code..."
	@ ruff format src/ tests/
	@ ruff check src/ tests/ --fix

.PHONY: security
security: ## Run security checks
	@echo "🔒 Running security checks..."
	@ bandit -r src/ -ll
	@ safety check --json

.PHONY: clean
clean: ## Clean all artifacts
	@echo "🧹 Cleaning up..."
	@rm -rf build dist __pycache__ .pytest_cache htmlcov .coverage .mypy_cache .ruff_cache test-artifacts *.spec .coverage.* 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "✨ Clean!"

# ========== SPECIAL COMMANDS ==========

.PHONY: assets-check
assets-check: ## Validate all game assets exist
	@echo "🎨 Checking assets..."
	@ python tools/check_assets.py

.PHONY: test-visual
test-visual: ## Run visual debug tools
	@echo "👁️ Running visual tests..."
	@ python tools/visual/test_sprite_cutting.py
	@echo "Check test-artifacts/ directory for results"

.PHONY: sprites
sprites: ## Generate sprite test output
	@echo "🖼️ Generating sprite tests..."
	@ python tools/visual/test_sprite_cutting.py
	@ python tools/visual/test_attack_character.py
	@echo "✅ Sprite tests complete! Check test-artifacts/"

.PHONY: profile
profile: ## Profile game performance
	@echo "⚡ Profiling game..."
	@ python -m cProfile -o profile.stats src/main.py
	@echo "Profile saved to profile.stats"

.PHONY: celebrate
celebrate: ## Celebrate achievements!
	@echo "🎉 Celebration time!"
	@ python tools/celebrate.py