#!/usr/bin/python3
#encoding=utf-8
import sys, getopt,os
import re
import csv


def main(argv):

    # default parameters
    log_file_path = "$ROS_HOME/log/latest/rosout.log"
    csv_file_path = "$ROS_HOME/log/latest/out.csv"

    begin_partten = 'Node Startup'
    end_partten = ''
    data_partten = 'cur_pose_normed_std: %d,\tcur_pose_accued_std: %f,\ttraj_length: %f,\tprecent: %f\%'
    enable_timestamp = True

    # get user input
    try:
      opts, args = getopt.getopt(argv,"hi:o:b:e:d:t",["ifile=","ofile=","bp","ep","dp","time"])
    except getopt.GetoptError:
        print('log2csv.py \n'
              '-i <input log file path, default=$ROS_HOME/log/latest/rosout.log> \n'
              '-o <out csv file path, default=$ROS_HOME/log/latest/out.csv> \n'
              '-b <begin_partten, default=\'Node Startup\'> \n'
              '-e <end_partten, default=\'\'> \n'
              '-d <data_partten, example=\'cur_pose_normed_std: %d,\\tcur_pose_accued_std: %f,\\ttraj_length: %f,\\tprecent: %f\%\'> \n'
              '-t <enable_timestamp, default=True> \n')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('log2csv.py \n'
                '-i <input log file path, default=$ROS_HOME/log/latest/rosout.log> \n'
                '-o <out csv file path, default=$ROS_HOME/log/latest/out.csv> \n'
                '-b <begin_partten, default=\'Node Startup\'> \n'
                '-e <end_partten, default=\'\'> \n'
                '-d <data_partten, example=\'cur_pose_normed_std: %d,\\tcur_pose_accued_std: %f,\\ttraj_length: %f,\\tprecent: %f\%\'> \n'
                '-t <enable_timestamp, default=True> \n')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            log_file_path = arg
        elif opt in ("-o", "--ofile"):
            csv_file_path = arg
        elif opt in ("-b", "--bp"):
            begin_partten = arg
        elif opt in ("-e", "--ep"):
            end_partten = arg
        elif opt in ("-d", "--dp"):
            data_partten = arg
        elif opt in ("-t", "--time"):
            enable_timestamp = arg

    log_file_path = os.path.expandvars(log_file_path)
    csv_file_path = os.path.expandvars(csv_file_path)\

    print('log_file_path：', log_file_path)
    print('csv_file_path：', csv_file_path)
    print('begin_partten：', begin_partten)
    print('end_partten：', end_partten)
    print('data_partten：', data_partten)
    print('enable_timestamp：', enable_timestamp)

    # begin convert
    begin_line_num = 0
    end_line_num = 0

    table_head = []
    for header_match in re.finditer('\w+[: =\t]', data_partten):
        header_text = header_match.group()
        header_text = re.match('\w+', header_text).group()
        table_head.append(header_text)

    row_data_len = len(table_head)

    table_data = []

    with open(log_file_path, "r") as file:
        for line_i, line in enumerate(file, 1):
            if re.search(begin_partten,line):
                begin_line_num = line_i > begin_line_num and line_i or begin_line_num
            if re.search(end_partten,line):
                end_line_num = line_i > end_line_num and line_i or end_line_num

    with open(log_file_path, "r") as file:
        for line_i, line in enumerate(file, 1):
            if line_i >= begin_line_num and line_i <= end_line_num and re.search(table_head[0],line):
                raw_line_data = []
                line_data = []
                for num_match in re.finditer('(?![A-Za-z])(([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)|([-+]?\d+))(?![A-Za-z])', line):
                    raw_line_data.append(num_match.group())
                if enable_timestamp: line_data.append(raw_line_data[0])     #timestamp
                line_data.extend(raw_line_data[-row_data_len:])
                table_data.append(line_data)

    with open(csv_file_path, 'w') as csvfile:
        try:
            writer = csv.writer(csvfile)
            field_names = table_head
            if enable_timestamp:
                field_names.insert(0,'timestamp')
            writer.writerow(field_names)
            writer.writerows(table_data)
        finally:
            csvfile.close()

    print('Convert Finished')


if __name__ == "__main__":
    main(sys.argv[1:])