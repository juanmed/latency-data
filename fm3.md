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
|All|{GPS Latency All Cameras_min:.2f}|{GPS Latency All Cameras_max:.2f}|{GPS Latency All Cameras_avg:.2f}|{GPS Latency All Cameras_std:.2f}|
|0|{Camera 0 GPS Latency_min:.2f}|{Camera 0 GPS Latency_max:.2f}|{Camera 0 GPS Latency_avg:.2f}|{Camera 0 GPS Latency_std:.2f}|
|1|{Camera 1 GPS Latency_min:.2f}|{Camera 1 GPS Latency_max:.2f}|{Camera 1 GPS Latency_avg:.2f}|{Camera 1 GPS Latency_std:.2f}|
|2|{Camera 2 GPS Latency_min:.2f}|{Camera 2 GPS Latency_max:.2f}|{Camera 2 GPS Latency_avg:.2f}|{Camera 2 GPS Latency_std:.2f}|
|3|{Camera 3 GPS Latency_min:.2f}|{Camera 3 GPS Latency_max:.2f}|{Camera 3 GPS Latency_avg:.2f}|{Camera 3 GPS Latency_std:.2f}|
|4|{Camera 4 GPS Latency_min:.2f}|{Camera 4 GPS Latency_max:.2f}|{Camera 4 GPS Latency_avg:.2f}|{Camera 4 GPS Latency_std:.2f}|
|5|{Camera 5 GPS Latency_min:.2f}|{Camera 5 GPS Latency_max:.2f}|{Camera 5 GPS Latency_avg:.2f}|{Camera 5 GPS Latency_std:.2f}| 
<!-- pagebreak -->

### PC Clock Latency

|camera num|min|max|avg|std|
|---|---|---|---|---|
|All|{PC Clock Latency All Cameras_min:.2f}|{PC Clock Latency All Cameras_max:.2f}|{PC Clock Latency All Cameras_avg:.2f}|{PC Clock Latency All Cameras_std:.2f}|
|0|{Camera 0 PC Clock Latency_min:.2f}|{Camera 0 PC Clock Latency_max:.2f}|{Camera 0 PC Clock Latency_avg:.2f}|{Camera 0 PC Clock Latency_std:.2f}|
|1|{Camera 1 PC Clock Latency_min:.2f}|{Camera 1 PC Clock Latency_max:.2f}|{Camera 1 PC Clock Latency_avg:.2f}|{Camera 1 PC Clock Latency_std:.2f}|
|2|{Camera 2 PC Clock Latency_min:.2f}|{Camera 2 PC Clock Latency_max:.2f}|{Camera 2 PC Clock Latency_avg:.2f}|{Camera 2 PC Clock Latency_std:.2f}|
|3|{Camera 3 PC Clock Latency_min:.2f}|{Camera 3 PC Clock Latency_max:.2f}|{Camera 3 PC Clock Latency_avg:.2f}|{Camera 3 PC Clock Latency_std:.2f}|
|4|{Camera 4 PC Clock Latency_min:.2f}|{Camera 4 PC Clock Latency_max:.2f}|{Camera 4 PC Clock Latency_avg:.2f}|{Camera 4 PC Clock Latency_std:.2f}|
|5|{Camera 5 PC Clock Latency_min:.2f}|{Camera 5 PC Clock Latency_max:.2f}|{Camera 5 PC Clock Latency_avg:.2f}|{Camera 5 PC Clock Latency_std:.2f}| 
<!-- pagebreak -->

### Latency

<img src = "{GPS_Latency_All_Cameras}">
<img src = "{Camera_0_GPS_Latency}">
<img src = "{Camera_1_GPS_Latency}">
<img src = "{Camera_2_GPS_Latency}">
<img src = "{Camera_3_GPS_Latency}">
<img src = "{Camera_4_GPS_Latency}">
<img src = "{Camera_5_GPS_Latency}">

<!-- pagebreak -->
<img src = "{hist_cam0}">
<img src = "{hist_cam1}">
<img src = "{hist_cam2}">
<img src = "{hist_cam3}">
<img src = "{hist_cam4}">
<!-- pagebreak -->

### PC Clock Latency 
<img src = "{PC_Clock_Latency_All_Cameras}">
<img src = "{Camera_0_PC_Clock_Latency}">
<img src = "{Camera_1_PC_Clock_Latency}">
<img src = "{Camera_2_PC_Clock_Latency}">
<img src = "{Camera_3_PC_Clock_Latency}">
<img src = "{Camera_4_PC_Clock_Latency}">
<img src = "{Camera_5_PC_Clock_Latency}">
<!-- pagebreak -->
### PC Clock Latency Histogram
<img src = "{pc_hist_cam0}">
<img src = "{pc_hist_cam1}">
<img src = "{pc_hist_cam2}">
<img src = "{pc_hist_cam3}">
<img src = "{pc_hist_cam4}">
<!-- pagebreak -->

# GPS Latency and PC Clock Latency
<img src = "{GPS_Latency_PC_Clock_Latency}">
<img src = "{Camera_0_GPS_Latency_Camera_0_PC_Clock_Latency}">
<img src = "{Camera_1_GPS_Latency_Camera_1_PC_Clock_Latency}">
<img src = "{Camera_2_GPS_Latency_Camera_2_PC_Clock_Latency}">
<img src = "{Camera_3_GPS_Latency_Camera_3_PC_Clock_Latency}">
<img src = "{Camera_4_GPS_Latency_Camera_4_PC_Clock_Latency}">
<img src = "{Camera_5_GPS_Latency_Camera_5_PC_Clock_Latency}">

<!-- pagebreak -->

### PC Clock Network Latency 
<img src = "{pc_network_latency}">

### PC Clock Network Latency and Latency
<img src = "{pc_network_latency_with_latency}">

### PC Clock Network Latency minus Latency
<img src = "{pc_network_latency_minus_latency}">
<!-- pagebreak -->

### PC Clock Latency and Latency Difference

<img src = "{PC_Clock_Latency_minus_GPS_Latency}">
<img src = "{Camera_0_PC_Clock_Latency_minus_GPS_Latency}">
<img src = "{Camera_1_PC_Clock_Latency_minus_GPS_Latency}">
<img src = "{Camera_2_PC_Clock_Latency_minus_GPS_Latency}">
<img src = "{Camera_3_PC_Clock_Latency_minus_GPS_Latency}">
<img src = "{Camera_4_PC_Clock_Latency_minus_GPS_Latency}">
<img src = "{Camera_5_PC_Clock_Latency_minus_GPS_Latency}">

<!-- pagebreak -->

### Raw Latency

<img src = "{raw_latency_all}">

### Satellite Count 

<img src = "{satellite_all}">


<!-- pagebreak -->

## Latency over Route

<img src = "latency_height_map.png">


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

<img src = "pc_latency_height_map.png">


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


### PC Clock Latency and Latency Difference

<img src = "dif_latency_height_map.png">


<!-- pagebreak -->
### GPS Satellite Count Map
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


