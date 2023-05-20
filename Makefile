# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - Makefile                              #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Thu May 18 16:36:50 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

DATA	= ./docker
TARGET	= docker-compose.yml
FLAGS	= --no-deps --build
SILENT	= > /dev/null 2>&1
NOERR	= | true
IDC		= $(SILENT) $(NOERR)

########################################

r: run
run: folder
	@docker-compose -f $(TARGET) up -d

b: build
build: stop folder
	@docker-compose -f $(TARGET) up $(FLAGS) -d

s: stop
stop:
	@docker-compose -f $(TARGET) down

c: clean
clean: stop folderclean
	@docker rm -f $(shell docker ps -aq) $(IDC)
	@docker rmi -f $(shell docker images -aq) $(IDC)
	@docker volume rm $(shell docker volume ls -q) $(IDC)

f: folder
folder:
	@mkdir -p $(DATA)/data
	@mkdir -p $(DATA)/log

fc: folderclean
folderclean:
	@rm -Rf $(DATA)/data
	@rm -Rf $(DATA)/log

re: remake
remake: clean build

########################################

.DEFAULT_GOAL = run
.PHONY: \
	all build run \
	clean folderclean \
	stop remake