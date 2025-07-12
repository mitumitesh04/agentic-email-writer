@echo off
echo Starting Email Generator Agent...
streamlit run streamlit_app.py --server.port 8501 --server.address localhost
pause
