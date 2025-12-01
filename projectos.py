import streamlit as st 
import time 
import plotly.graph_objects as go 
import pandas as pd 
# ------------------ Disk Algorithms --------------------- 
def fcfs(requests, head): 
order = [head] + requests 
total = sum(abs(order[i] - order[i-1]) for i in range(1, 
len(order))) 
return order, total 
def sstf(requests, head): 
reqs = requests.copy() 
order = [head] 
current = head 
while reqs: 
nearest = min(reqs, key=lambda x: abs(x - current)) 
order.append(nearest) 
reqs.remove(nearest) 
current = nearest 
total = sum(abs(order[i] - order[i-1]) for i in range(1, 
len(order))) 
return order, total 
def scan(requests, head, disk_size=200, 
direction="right"): 
left = sorted([r for r in requests if r < head]) 
right = sorted([r for r in requests if r >= head]) 
order = [head] 
if direction == "right": 
order += right + [disk_size - 1] + left[::-1] 
else: 
order += left[::-1] + [0] + right 
total = sum(abs(order[i] - order[i-1]) for i in range(1, 
len(order))) 
return order, total 
def c_scan(requests, head, disk_size=200, 
direction="right"): 
left = sorted([r for r in requests if r < head]) 
right = sorted([r for r in requests if r >= head]) 
if direction == "right": 
order = [head] + right + [disk_size - 1, 0] + left 
else: 
order = [head] + left[::-1] + [0, disk_size - 1] + 
right[::-1] 
total = sum(abs(order[i] - order[i-1]) for i in range(1, 
len(order))) 
return order, total 
# ------------------ Animation --------------------- 
def animate(order, speed): 
st.write("###             
Disk Head Animation") 
fig = go.Figure() 
for i in range(1, len(order)): 
fig.add_trace(go.Scatter( 
x=[order[i-1], order[i]], 
y=[0, 0], 
mode="lines+markers+text", 
text=[order[i-1], order[i]], 
textposition="top center" 
)) 
st.plotly_chart(fig, width="stretch") 
time.sleep(speed) 
# ------------------ UI --------------------- 
st.title("        
Advanced Disk Scheduling Simulator") 
req_str = st.text_input("Enter Disk Requests", "82, 170, 
43, 140, 24, 16, 190") 
head = st.number_input("Starting Head Position", 0, 
500, 50) 
disk_size = st.number_input("Disk Size (Cylinders)", 100, 
1000, 200) 
# Random request generator 
if st.button("       
Generate Random Requests"): 
import random 
req_str = ", ".join(map(str, random.sample(range(0, 
disk_size), 8))) 
st.success(f"Generated Random Requests: {req_str}") 
algorithms = ["FCFS", "SSTF", "SCAN", "C-SCAN"] 
algo = st.selectbox("Select Algorithm", algorithms) 
# Direction control for SCAN / C-SCAN 
direction = "right" 
if algo == "SCAN": 
direction = st.radio("Select SCAN Direction", ["right", 
"left"]) 
elif algo == "C-SCAN": 
direction = st.radio("Select C-SCAN Direction", 
["right", "left"]) 
speed = st.slider("  
move)", 0.1, 1.0, 0.5) 
Animation Speed (seconds per 
# ------------------ Run Simulation --------------------- 
if st.button("Run Simulation"): 
requests = list(map(int, req_str.split(","))) 
if algo == "FCFS": 
order, total = fcfs(requests, head) 
elif algo == "SSTF": 
order, total = sstf(requests, head) 
elif algo == "SCAN": 
order, total = scan(requests, head, disk_size, 
direction) 
else: 
order, total = c_scan(requests, head, disk_size, 
direction) 
avg_seek = total / len(requests) 
throughput = len(requests) / total if total != 0 else 0 
st.success(f"Algorithm: {algo}") 
st.write(f"     
Sequence: {order}") 
st.write(f"      
st.write(f"    
st.write(f"        
Total Seek Time: {total}") 
Average Seek Time: {avg_seek:.2f}") 
System Throughput: {throughput:.4f} 
requests/unit time") 
animate(order, speed) 
# ------------------ Compare All Algorithms --------------------- 
if st.button("Compare All Algorithms"): 
request_list = list(map(int, req_str.split(","))) 
results = {} 
orders = {} 
results["FCFS"], orders["FCFS"] = fcfs(request_list, 
head) 
results["SSTF"], orders["SSTF"] = sstf(request_list, 
head) 
# SCAN default → right 
results["SCAN"], orders["SCAN"] = scan(request_list, 
head, disk_size, "right") 
# CSCAN default → right 
results["C-SCAN"], orders["C-SCAN"] = 
c_scan(request_list, head, disk_size, "right") 
final_results = { 
"Algorithm": [], 
"Total Seek Time": [], 
"Average Seek Time": [], 
"Throughput": [] 
} 
for name in results: 
seq, total = results[name] 
final_results["Algorithm"].append(name) 
final_results["Total Seek Time"].append(total) 
final_results["Average Seek Time"].append(total / 
len(request_list)) 
final_results["Throughput"].append(len(request_list) / 
total if total > 0 else 0) 
df = pd.DataFrame(final_results) 
st.table(df) 
csv = df.to_csv(index=False).encode('utf-8') 
st.download_button("     
Download Result CSV", csv, 
"results.csv") 
# Reset button 
if st.button("    
Reset"): 
st.rerun()