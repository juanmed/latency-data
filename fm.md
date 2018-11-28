## Experiment Date: {date}
## Experiment Name: {name}
 <table></table>
### Route

<img src = "{track_image_path}">
### Experiment

- Experiment Conditions
    - frame size : {video_res}
    - 30 fps
    - lte connection
    - gop : 1


- Experiment Results

|camera num|min|max|avg|std|
|---|---|---|---|---|
|0|{cam0_min:.2f}|{cam0_max:.2f}|{cam0_avg:.2f}|{cam0_std:.2f}|
|1|{cam1_min:.2f}|{cam1_max:.2f}|{cam1_avg:.2f}|{cam1_std:.2f}|
|2|{cam2_min:.2f}|{cam2_max:.2f}|{cam2_avg:.2f}|{cam2_std:.2f}|
|3|{cam3_min:.2f}|{cam3_max:.2f}|{cam3_avg:.2f}|{cam3_std:.2f}|
<img src = "{data_image_path}">
<!-- pagebreak -->
<img src = "{latency_cam0}">
<img src = "{latency_cam1}">
<img src = "{latency_cam2}">
<img src = "{latency_cam3}">
<img src = "{hist_cam0}">
<img src = "{hist_cam1}">
<img src = "{hist_cam2}">
<img src = "{hist_cam3}">
<!-- pagebreak -->

## Latency over Route
### Maximum Latency for all cameras
<img src = "{lat_gps_all}">
### Maximum Latency Camera 0
<img src = "{lat_gps_cam0}">
### Maximum Latency Camera 1
<img src = "{lat_gps_cam1}">
### Maximum Latency Camera 2
<img src = "{lat_gps_cam2}">
### Maximum Latency Camera 3
<img src = "{lat_gps_cam3}">

<!-- pagebreak -->
### Latency, Velocity vs Time
<img src = "{latency_speed_time}">
### Latency vs Velocity
<img src = "{latency_speed}">



