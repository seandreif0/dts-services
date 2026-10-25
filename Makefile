SERVICES := $(notdir $(wildcard services/*))

.PHONY: test
test:
	@set -e; for s in $(SERVICES); do echo "== $$s"; (cd services/$$s && python -m pytest -q); done
