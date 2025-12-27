import time
import streamlit as st
import config
import data_provider as dp
import ui_components as ui

st.set_page_config(
    page_title="SmartMiner Farm",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def live_data_section():
    manager_data = dp.get_manager_status()
    miners_data = dp.get_all_miners_stats()

    # Rendering UI components
    ui.render_kpi_section(manager_data, miners_data)
    st.divider()
    ui.render_workers_list(miners_data)

def main():
    st.title("⛏️ SmartMiner Farm Dashboard")
    
    refresh_rate = st.sidebar.number_input("Refresh rate (seconds):", 
                                         min_value=10, 
                                         max_value=60, 
                                         value=config.REFRESH_RATE_SECONDS,
                                         key="refresh_rate")
    
    live_data_section()
    
    if st.sidebar.button("Refresh Now"):
        st.rerun()
    
    time.sleep(refresh_rate)
    st.rerun()

if __name__ == "__main__":
    main()