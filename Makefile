.DEFAULT_GOAL := help


### QUICK
# ¯¯¯¯¯¯¯

install: server.install ## Install

daemon: server.daemon ## Start

stop: server.stop ## Stop


include makefiles/server.mk
include makefiles/test.mk
include makefiles/help.mk
