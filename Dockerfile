FROM postgres:17-alpine
ENV POSTGRES_DB=findthemall POSTGRES_USER=findthemall POSTGRES_PASSWORD=findthemall
COPY migrations /migrations
COPY examination-entrypoint.sh /usr/local/bin/examination-entrypoint.sh
RUN chmod +x /usr/local/bin/examination-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/examination-entrypoint.sh"]
CMD ["postgres"]
