#「発言〜リアクション連鎖」 という1サイクル（1ターン）の内部構造＝ミクロなループ

from utils.utils_calc import speak_decision
from utils.utils_calc import speaker_decision
from utils.utils_calc import agree_to_speaker
from utils.utils_calc import reaction_decision
from utils.utils_calc import attitude_result
from utils.utils_calc import reactor_decision
from utils.utils_calc import update_efficacy
from utils.utils_calc import update_risk
from utils.logger import log_step
from utils.utils_calc import calc_risk_mean

#t1はouterループ（全体）の時間を持つ。　行動のステップ数(発言なしを含む)
#t2はinnerループ内の時間を持つ。　reactionの数

def run_outer_loop(agents,max_steps):
    logs = []
    t1 = 0
    #初期値に対してlogを作る（最初は誰も発言がないとする）
    log_step(t1,0,agents,None,None)
    t1 = 1
    while t1 < max_steps:
        t1 = run_inner_loop(agents,t1,logs,max_steps)  # tを渡す場合
    # return logs,t1
    return logs

def run_inner_loop(agents,t1,logs,max_steps):
    t2 = 0
    speak_dict = {}    
    for agent in agents:
        speak = speak_decision(agent.speak_probability_mean)
        speak_dict[agent.id] = speak #agent.idをキーに発言を格納
        # print(f"Agent{agent.id} ：{speak}")
    speaker_id = speaker_decision(speak_dict)
    
    #発言者がいない場合(全員　speak ==0) logとt=1を返す
    if speaker_id is None:
        log_step(t1,t2,agents,None,None)
        t1 += 1
        t2 += 1
        return t1
    speaker = next(agent for agent in agents if agent.id == speaker_id)
    #発言者がいる場合、reactionの過程に移動
    log_step(t1,t2,agents,"Speak",speaker_id)
    t1 += 1
    t2 += 1
    
    
    
    while True:
        if t1 >= max_steps: #以上を超えたら強制終了
            return t1
        # print("whileは動いています")
        # print(t2 + 1,"周目 ")
        #agree行動
        #attitude行動
        
        reaction_dict = {}
        agree_dict = {}
        attitude_dict = {}
        for agent in agents:
            agree = agree_to_speaker(agent,speaker_id,0.1)
            agree_dict[agent.id] = agree
            reaction = reaction_decision(agent,speaker_id,agree)
            reaction_dict[agent.id] = reaction
            attitude = attitude_result(agent.attitude_probability,speaker_id)
            attitude_dict[agent.id] = attitude
            
    
            # print("agent",agent.id,":agree",agree)
            # print("agent",agent.id,":reaction",reaction)
            # print("agent",agent.id,"attitude", attitude)
            
        
        reactor_id = reactor_decision(reaction_dict)
        
        if reactor_id is None:
            return t1#（Noneの時は+1しない。reactしないけどspeakする可能性があるから。）
        
        reactor = next(agent for agent in agents if agent.id == reactor_id)
        reactor_agree = list(agree_dict[reactor_id].values())[0]
        reactor_attitude = list(attitude_dict[reactor_id].values())[0]
        #学習
        _,updated_efficacy = update_efficacy(speaker,reactor,reactor_agree,0.5,0.5)
        _, updated_risk = update_risk(speaker,reactor,reactor_attitude,1/3,1/3,1/3)
        update_risk_mean = calc_risk_mean(speaker.risk)
            
        speaker.efficacy = updated_efficacy
        speaker.risk = updated_risk
        speaker.risk_mean = update_risk_mean
        
        print("agent",speaker_id,"efficacy", speaker.efficacy )
        
        # 7. 次のspeakerに交代（反応者が次の発言者）
        speaker = reactor
        speaker_id = reactor.id
        log_step(t1,t2,agents,"React",reactor_id)
        t1 += 1
        t2 += 1 
    
    # return logs

