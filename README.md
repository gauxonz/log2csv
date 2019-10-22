# log2csv: Conver ROS .log file to csv based-on given regex

If you logging data with default ROS tools like:

```c++
ROS_DEBUG("cur_pose_normed_std: %f,\tcur_pose_accued_std: %f,\ttraj_length: %f,\tprecent: %f\%",
                     cur_std,
                     cur_std_accu,
                     total_traj_length,
                     100 * cur_std_accu / total_traj_length
            );
```

Then this tool convert the .log file to csv file like:

```csv
timestamp,cur_pose_normed_std,cur_pose_accued_std,traj_length,precent
1571729583.003983689,0.015855,0.015855,1.398229,1.133900
1571729583.051318895,2.039934,2.039995,2.826493,72.174088
1571729583.102845235,1.797013,2.718610,4.323514,62.879623
1571729583.157592523,1.638327,3.174106,5.872920,54.046475
```

based-on given printf-token-style pattern (`"cur_pose_normed_std: %f,\tcur_pose_accued_std: %f,\ttraj_length: %f,\tprecent: %f\%"` for example).

## Usage

```bash
log2csv.py 
-i <input log file path, default=$ROS_HOME/log/latest/rosout.log> 
-o <out csv file path, default=$ROS_HOME/log/latest/out.csv> 
-b <begin_partten, default="Node Startup"> 
-e <end_partten, default=""> 
-d <data_partten, example="cur_pose_normed_std: %d,\tcur_pose_accued_std: %f,\ttraj_length: %f,\tprecent: %f\%"> 
-t <enable_timestamp, default=True> 
```

