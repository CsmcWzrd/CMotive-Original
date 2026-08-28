# CMotive Lang-Examples Makefile
# Expected layout:
#   CMotive/
#     tools/cmotive.py
#     tools/cmotivepp.py
#     Lang-Examples/Makefile
#
# Override CMOTIVE_ROOT, CMOTIVE, or CMOTIVEPP if your layout differs.

SHELL := /bin/sh
CMOTIVE_ROOT ?= ..
PYTHON ?= python3
CMOTIVE ?= $(CMOTIVE_ROOT)/tools/cmotive.py
CMOTIVEPP ?= $(CMOTIVE_ROOT)/tools/cmotivepp.py
TIMEOUT ?= 5

.PHONY: all compile objects run check preprocess manifest clean list help debug-symbols vs-validate

all: compile

help:
	@printf '%s\n' 'CMotive Lang-Examples targets:'
	@printf '%s\n' '  make compile     Compile all manifest examples to build/bin'
	@printf '%s\n' '  make objects     Compile all manifest examples with -c to build/obj'
	@printf '%s\n' '  make run         Compile and execute all manifest examples'
	@printf '%s\n' '  make check       Manifest + object generation + run verification'
	@printf '%s\n' '  make preprocess  Run cmotivepp over all examples into build/pp'
	@printf '%s\n' '  make clean       Remove Lang-Examples build outputs'
	@printf '%s\n' '  make debug-symbols Build example 150 with -g3 -O2 and verify .syms output'
	@printf '%s\n' '  make list        List manifest examples'
	@printf '%s\n' '  make vs-validate Validate VS2022 package project inputs'

manifest:
	@$(PYTHON) tools/example_build.py manifest

compile:
	@$(PYTHON) tools/example_build.py compile --compiler '$(CMOTIVE)'

objects:
	@$(PYTHON) tools/example_build.py objects --compiler '$(CMOTIVE)'

preprocess:
	@$(PYTHON) tools/example_build.py preprocess --preprocessor '$(CMOTIVEPP)'

run:
	@$(PYTHON) tools/example_build.py run --compiler '$(CMOTIVE)' --timeout '$(TIMEOUT)'

check:
	@$(PYTHON) tools/example_build.py check --compiler '$(CMOTIVE)' --timeout '$(TIMEOUT)'

list:
	@$(PYTHON) tools/example_build.py list

debug-symbols:
	@$(PYTHON) tools/example_build.py debug-symbols --compiler '$(CMOTIVE)'

vs-validate:
	@$(PYTHON) tools/vs2022_build_packages.py --mode validate --examples-root . --cmotive-root '$(CMOTIVE_ROOT)'

clean:
	@$(PYTHON) tools/example_build.py clean
