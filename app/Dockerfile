# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - Dockerfile                            #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Thu May 18 17:12:23 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

FROM python:3.11-bullseye
RUN apt-get install -y openssh-client git

WORKDIR /app
RUN git clone -b dev --single-branch https://github.com/BlankRose/ProjectDisMaid.git . \
	&& pip3.11 install --no-cache-dir -r requirements.txt
COPY configs.json .

CMD [ "python3.11", "run.py" ]