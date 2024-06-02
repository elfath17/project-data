conda create --name dashboard python=3.11.4
conda activate dashboard
pip install -r requirements.txt

streamlit run dashboard.py
