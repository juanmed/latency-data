## Experiment Date: {date}
## Experiment Name: {name}
 <table></table>

### Route
<img src = "{track_image_path}">

(Route Followed | Markers
:-------------------------:|:-------------------------:
![]({track_image_path})  | ![](sfr.png)

### Experiment

- Experiment Conditions
    - frame size : {video_res}
    - 30 fps
    - lte connection
    - gop : 1


- Experiment Results

### GPS Latency

|camera num|min|max|avg|std|
|---|---|---|---|---|
|0|{cam0_min:.2f}|{cam0_max:.2f}|{cam0_avg:.2f}|{cam0_std:.2f}|
|1|{cam1_min:.2f}|{cam1_max:.2f}|{cam1_avg:.2f}|{cam1_std:.2f}|
|2|{cam2_min:.2f}|{cam2_max:.2f}|{cam2_avg:.2f}|{cam2_std:.2f}|
|3|{cam3_min:.2f}|{cam3_max:.2f}|{cam3_avg:.2f}|{cam3_std:.2f}|
|4|{cam4_min:.2f}|{cam4_max:.2f}|{cam4_avg:.2f}|{cam4_std:.2f}| 
<!-- pagebreak -->

### PC Clock Latency

|camera num|min|max|avg|std|
|---|---|---|---|---|
|0|{cam0_min_pc:.2f}|{cam0_max_pc:.2f}|{cam0_avg_pc:.2f}|{cam0_std_pc:.2f}|
|1|{cam1_min_pc:.2f}|{cam1_max_pc:.2f}|{cam1_avg_pc:.2f}|{cam1_std_pc:.2f}|
|2|{cam2_min_pc:.2f}|{cam2_max_pc:.2f}|{cam2_avg_pc:.2f}|{cam2_std_pc:.2f}|
|3|{cam3_min_pc:.2f}|{cam3_max_pc:.2f}|{cam3_avg_pc:.2f}|{cam3_std_pc:.2f}|
|4|{cam4_min_pc:.2f}|{cam4_max_pc:.2f}|{cam4_avg_pc:.2f}|{cam4_std_pc:.2f}| 

### Latency

<!-- pagebreak -->
<img src = "{latency_cam0}">
<img src = "{latency_cam1}">
<img src = "{latency_cam2}">
<img src = "{latency_cam3}">
<img src = "{latency_cam4}">
<!-- pagebreak -->
<img src = "{hist_cam0}">
<img src = "{hist_cam1}">
<img src = "{hist_cam2}">
<img src = "{hist_cam3}">
<img src = "{hist_cam4}">
<!-- pagebreak -->

### PC Clock Latency 
<img src = "{pc_latency_cam0}">
<img src = "{pc_latency_cam1}">
<img src = "{pc_latency_cam2}">
<img src = "{pc_latency_cam3}">
<img src = "{pc_latency_cam4}">
<!-- pagebreak -->
<img src = "{pc_hist_cam0}">
<img src = "{pc_hist_cam1}">
<img src = "{pc_hist_cam2}">
<img src = "{pc_hist_cam3}">
<img src = "{pc_hist_cam4}">
<!-- pagebreak -->

<img src = "{com_latency_cam0}">
<img src = "{com_latency_cam1}">
<img src = "{com_latency_cam2}">
<img src = "{com_latency_cam3}">
<img src = "{com_latency_cam4}">

<!-- pagebreak -->

### PC Clock Latency and Latency Difference

<img src = "{dif_latency_cam0}">
<img src = "{dif_latency_cam1}">
<img src = "{dif_latency_cam2}">
<img src = "{dif_latency_cam3}">
<img src = "{dif_latency_cam4}">

<!-- pagebreak -->

### Raw Latency

<img src = "{raw_latency_all}">

### Satellite Count 

<img src = "{satellite_all}">


<!-- pagebreak -->

## Latency over Route

### Maximum Latency for all cameras
Map | Index
:-------------------------:|:-------------------------:
![](latency_map_all.png)  | ![]({latency_map_all_colorbar})
### Maximum Latency Camera 0
Map | Index
:-------------------------:|:-------------------------:
![](latency_map_cam0.png)  | ![]({latency_map_cam0_colorbar})
<!-- pagebreak -->
### Maximum Latency Camera 1
Map | Index
:-------------------------:|:-------------------------:
![](latency_map_cam1.png)  | ![]({latency_map_cam1_colorbar})
### Maximum Latency Camera 2
Map | Index
:-------------------------:|:-------------------------:
![](latency_map_cam2.png)  |  ![]({latency_map_cam2_colorbar})
<!-- pagebreak -->
### Maximum Latency Camera 3
Map | Index
:-------------------------:|:-------------------------:
![](latency_map_cam3.png)  |  ![]({latency_map_cam3_colorbar})
### Maximum Latency Camera 4
Map | Index
:-------------------------:|:-------------------------:
![](latency_map_cam4.png)  |  ![]({latency_map_cam4_colorbar})

<!-- pagebreak -->


### Maximum PC Clock Latency for all cameras
Map | Index
:-------------------------:|:-------------------------:
![](pc_latency_map_all.png)  | ![]({pc_latency_map_all_colorbar})
### Maximum Latency Camera 0
Map | Index
:-------------------------:|:-------------------------:
![](pc_latency_map_cam0.png)  | ![]({pc_latency_map_cam0_colorbar})
<!-- pagebreak -->
### Maximum Latency Camera 1
Map | Index
:-------------------------:|:-------------------------:
![](pc_latency_map_cam1.png)  | ![]({pc_latency_map_cam1_colorbar})
### Maximum Latency Camera 2
Map | Index
:-------------------------:|:-------------------------:
![](pc_latency_map_cam2.png)  |  ![]({pc_latency_map_cam2_colorbar})
<!-- pagebreak -->
### Maximum Latency Camera 3
Map | Index
:-------------------------:|:-------------------------:
![](pc_latency_map_cam3.png)  |  ![]({pc_latency_map_cam3_colorbar})
### Maximum Latency Camera 4
Map | Index
:-------------------------:|:-------------------------:
![](pc_latency_map_cam4.png)  |  ![]({pc_latency_map_cam4_colorbar})

<!-- pagebreak -->
### Satellite Count Map
Map | Index
:-------------------------:|:-------------------------:
![](satellite_map.png)  | ![]({satellite_map_colorbar})


<!-- pagebreak -->
### Latency, Speed vs Time
<img src = "{latency_speed_time}">
### Latency vs Speed
<img src = "{latency_speed}">
### Latency vs Speed Histogram
<img src = "{latency_speed_hist}">
<!-- pagebreak -->
### Latency vs Antennas inside various radii
<img src = "{latency_antenna_in_radius_r0}">
<img src = "{latency_antenna_in_radius_r1}">
<img src = "{latency_antenna_in_radius_r2}">
<img src = "{latency_antenna_in_radius_r3}">
<img src = "{latency_antenna_in_radius_r4}">


