FROM veckiina/pbrt-v3-spectral:Yichao_Deng

RUN apk add --no-cache bash \
   python3 \
 && apk add --update \
 && pip3 install --upgrade pip\
 && pip3 install flywheel-sdk \
 && rm -rf /var/cache/apk/*
ENTRYPOINT ["python run.py"] 