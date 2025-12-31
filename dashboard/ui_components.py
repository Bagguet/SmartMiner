import streamlit as st
import pandas as pd


def render_kpi_section(manager_data, miners_data):
    """Renders aggregate KPIs for the entire farm."""
    # 1. Calculate aggregate statistics
    try:
        total_hashrate = sum(float(m['hashrate']) for m in miners_data)
    except:
        total_hashrate = 0
    active_workers = sum(1 for m in miners_data if m['online'])
    total_workers = len(miners_data)

    kpi1, kpi2, kpi3 = st.columns(3)
    
    # KPI 1: Mining Target
    coin_name = manager_data.get('coin', 'Waiting...') if manager_data else "Unknown"
    kpi1.metric("Mining Target", coin_name)

    # KPI 2: Total Hashrate
    label_hr = f"{total_hashrate:.2f} H/s"
    if total_hashrate > 1000: 
        label_hr = f"{total_hashrate/1000:.2f} kH/s"
    kpi2.metric("Total Hashrate", label_hr, delta=f"{active_workers}/{total_workers} Workers")
        
    # KPI 3: Estimated Profit (from manager)
    profit = f"${manager_data.get('profit_usd', 0)*total_hashrate:.2f} / day" if manager_data else "$0.00"
    kpi3.metric("Est. Farm Profit", profit)
    
    return total_hashrate

def format_time(seconds):
    if not seconds: return "0m"
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    
    if days > 0:
        return f"{days}d {hours}h"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def format_minutes(seconds):
    minutes = seconds / 60
    return minutes
    


def render_workers_list(miners_data):
    """Renders a detailed list of workers."""
    st.subheader(f"⚙️ Workers Status ({len(miners_data)})")
    
    for miner in miners_data:
        # Create a container (card) for each miner
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns([0.5, 2, 2, 2, 2, 2])
            try:
                # Status indicator
                if miner['online']:
                    col1.success("ON")
                else:
                    col1.error("OFF")
                    
                col2.write(f"**{miner['name']}**")
                col2.caption(miner['ip'])
                
                if miner['online']:
                    # Format hashrate
                    hr = miner['hashrate']
                    hr_str = f"{hr:.0f} H/s" if hr < 1000 else f"{hr/1000:.2f} kH/s"
                    col3.metric("Speed", hr_str)
                    
                    # Shares
                    acc_rate = 0
                    total_s = miner['shares_good'] + miner['shares_bad']
                    if total_s > 0:
                        acc_rate = (miner['shares_good'] / total_s) * 100
                    col4.metric("Shares", f"{miner['shares_good']} ", delta=f"{acc_rate:.1f}% Acc")
                    try:
                        col4.caption(f"{(miner['shares_good']/format_minutes(miner.get('uptime', 0))):.2f}/minute")
                    except:
                        pass

                    # Uptime and temperatures
                    sys_uptime_val = miner.get('sys_uptime', 0)
                    sys_uptime_str = format_time(sys_uptime_val)

                    miner_uptime = format_time(miner.get('uptime', 0))
                    temp_display = "N/A"
                    vrm_display = "N/A"
                    if 'sensors' in miner['raw_data']:
                        c_temp = miner['raw_data']['sensors'].get('cpu_temp', 0)
                        v_temp = miner['raw_data']['sensors'].get('vrm_temp', 0)
                        
                        temp_display = f"CPU: {c_temp:.1f} °C" if c_temp > 0 else "CPU: N/A"
                        if v_temp > 0:
                            vrm_display = f" | VRM: {v_temp:.1f} °C"
                    col5.write(f"🌡️ **{temp_display}{vrm_display}**")
                    col5.caption(f"Miner: {miner_uptime} | Sys: {sys_uptime_str}")
                    
                    # SSH command
                    ip = miner.get('ip')
                    ssh_user = miner.get('ssh_user')
                    
                    ssh_cmd = f"ssh {ssh_user}@{ip}"
                    link = f"ssh://{ssh_user}@{ip}"
                    col6.markdown(f"[🚀 Connect]({link})")
                    col6.code(ssh_cmd, language="bash")


                else:
                    col3.write("---")
                    col4.write("Connection Failed")
                    col5.write("---")
            except:
                col3.write("---")
                col4.write("Connection Failed")
                col5.write("---")
            
            st.divider()