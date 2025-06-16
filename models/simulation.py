#「発言〜リアクション連鎖」 という1サイクル（1ターン）の内部構造＝ミクロなループ

from utils.utils_calc import speak_decision
from utils.utils_calc import speaker_decision
from utils.utils_calc import agree_to_speaker
from utils.utils_calc import reaction_decision
from utils.utils_calc import attitude_result
from utils.utils_calc import reactor_decision
from utils.utils_calc import update_efficacy
from utils.utils_calc import update_risk


def run_inner_loop(agents):
    logs = []
    
    speak_dict = {}    
    for agent in agents:
        speak = speak_decision(agent.speak_probability_mean)
        speak_dict[agent.id] = speak #agent.idをキーに発言を格納
        print(f"Agent{agent.id} ：{speak}")
    speaker_id = speaker_decision(speak_dict)
    speaker = next(agent for agent in agents if agent.id == speaker_id)
    
    
    t=0
    while True:
        print("whileは動いています")
        print(t+1,"周目 ")
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
    
            print("agent",agent.id,":agree",agree)
            print("agent",agent.id,":reaction",reaction)
            print("agent",agent.id,"attitude", attitude)
        
        reactor_id = reactor_decision(reaction_dict)
        if reactor_id is None:
            return logs
        reactor = next(agent for agent in agents if agent.id == reactor_id)
        reactor_agree = list(agree_dict[reactor_id].values())[0]
        reactor_attitude = list(attitude_dict[reactor_id].values())[0]
        #学習
        _,updated_efficacy = update_efficacy(speaker,reactor,reactor_agree,0.5,0.5)
        _, updated_risk = update_risk(speaker,reactor,reactor_attitude,0.5,0.5,0.5)
            
        speaker.efficacy = updated_efficacy
        speaker.risk = updated_risk
        
        logs.append({
            "speaker_id": speaker_id,
            "reactor_id": reactor_id,
            "agree": reactor_agree,
            "attitude": reactor_attitude,
            "efficacy": updated_efficacy[reactor_id],
            "risk": updated_risk[reactor_id]
        })
        
        # 7. 次のspeakerに交代（反応者が次の発言者）
        speaker = reactor
        speaker_id = reactor.id
        
        t = t + 1
    
    # return logs

