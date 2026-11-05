.PHONY: install test sample run gold all docker-build docker-run clean

SEMESTERS ?= 2025-01 2025-02
export PYTHONPATH := src
export LAKEHOUSE_ROOT ?= $(CURDIR)/lakehouse

install:
	pip install -r requirements.txt

test:
	pytest -q

sample:            ## landing -> bronze -> silver com a amostra (offline)
	python -m anp_lakehouse.pipeline --sample

run:               ## landing -> bronze -> silver com dados reais da ANP
	python -m anp_lakehouse.pipeline --semesters $(SEMESTERS)

gold:              ## silver -> gold (dbt: modelos + testes)
	mkdir -p $(LAKEHOUSE_ROOT)/gold
	cd dbt && dbt build --profiles-dir .

all: test sample gold

docker-build:
	docker build -t anp-lakehouse .

docker-run:
	docker run --rm -v $(CURDIR)/lakehouse:/app/lakehouse anp-lakehouse

clean:
	rm -rf lakehouse spark-warehouse metastore_db dbt/target dbt/logs
