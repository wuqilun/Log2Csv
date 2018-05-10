#！/usr/bin env python3
"""
date: 2018-04-01
autho: dengyong.ai@gmailc.com 
"""
__author__="dengyong"

import pandas as pd
import numpy as np
import traceback


import re

def parse_teamname(rcg_path="./20180311233034-Alice_0-vs-HfutEngine2017_1.rcg"):
    t_name_exp='-(.*?)_'
    t_name=re.findall(t_name_exp,rcg_path)
    l_name=t_name[0]	
    r_name=t_name[1][3:]
    log_name_exp='(\d+-.*?).rcg'
    log_name=re.findall(log_name_exp,rcg_path)[0]+".csv"
    print(l_name,r_name,log_name)
    return l_name,r_name,"./csv/"+log_name



class Log2Csv:
    def __init__(self,rcg_path,rcl_path):
        self.rcg_path=rcg_path
        self.rcl_path=rcl_path
        self.l_name,self.r_name,self.csv_name=parse_teamname(self.rcg_path)
        self.game_id=self.csv_name[:-4]
    def rcg_2_df(self):
        rcg=open(self.rcg_path,"r")
        player_dict={}
        last_time=None
        for (count,i) in enumerate(rcg):
            if "show" in i:
                cycle_exp = "show (\d+) "
                cycle_time = re.search(cycle_exp,i)
                time = cycle_time.group(1)
                if last_time==time:
#                     print(last_time,time)
                    continue
                last_time=time
                self.seg_rcg_2_df(i,self.l_name,self.r_name,player_dict)

        rcg_df=pd.DataFrame(player_dict)
    
        rcg_df.to_csv(self.csv_name,index=False)
        
        
    def seg_rcg_2_df(self,test_rcg_seg, l_name, r_name,player_dict):
        cycle_exp = "show (\d+) "
        cycle_time = re.search(cycle_exp, test_rcg_seg)
        time = cycle_time.group(1)
        time

        # In[29]:

        ball_state_exp = "b\) (.*?)\)"
        ball_state = re.search(ball_state_exp, test_rcg_seg)
        ball_state = ball_state.group(1).split(" ")

        ball_x, ball_y, ball_vel_x, ball_vel_y = ball_state[0], ball_state[1], ball_state[2], ball_state[3]

        # In[38]:

        segle_player_exp = "\(\(((l|r).*?)\)\)"
        all_side = re.findall(segle_player_exp, test_rcg_seg)
        all_side[0]

        # In[51]:
        for (count, i) in enumerate(all_side):
            side = i[1]
            player_info_exp = "(l|r)(.*?)\("
            player_info = re.search(player_info_exp, i[0]).group(0)
            player_info = player_info.replace(")", "").split()

            name_pre = None
            if side == "l":
                name_pre = l_name
            else:
                name_pre = r_name

            #init
            
            if len(player_dict)<1:
                player_dict["cycle"] = [time]
                player_dict["ball_x"] = [ball_x]
                player_dict["ball_y"] = [ball_y]
                player_dict["ball_vx"] = [ball_vel_x]
                player_dict["ball_vy"] = [ball_vel_y]
#                 player_dict["player_side"] = [player_info[0]]
                player_dict["team_name"] = [name_pre]
                player_dict["player_num"] =[ player_info[1]]
                player_dict['team_side']=[side]
                
#                 player_dict["player_type"] = [player_info[2]]
#                 player_dict["player_state"] = [player_info[3]]
                player_dict["player_x"] = [player_info[4]]
                player_dict["player_y"] = [player_info[5]]
                player_dict["player_vx"] = [player_info[6]]
                player_dict["player_vy"] = [player_info[7]]

            else:
                player_dict["cycle"].append(time)
                player_dict["ball_x"].append(ball_x)
                player_dict["ball_y"].append(ball_y)
                player_dict["ball_vx"].append(ball_vel_x)
                player_dict["ball_vy"].append(ball_vel_y)
                player_dict["team_name"].append(name_pre)
                player_dict["player_num"].append(player_info[1])
                player_dict['team_side'].append(side)
                player_dict["player_x"].append(player_info[4])
                player_dict["player_y"].append(player_info[5])
                player_dict["player_vx"].append(player_info[6])
                player_dict["player_vy"].append(player_info[7])

import os
if __name__=="__main__":
    Log2Csv(os.sys.argv[1],os.sys.argv[2]).rcg_2_df()

