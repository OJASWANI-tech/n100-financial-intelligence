load:
	python src/etl/loader.py

ratios:
	python src/ratios/compute_ratios.py

test:
	pytest -v

report:
	python src/reports/generate_reports.py

dashboard:
	streamlit run src/dashboard/app.py

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache