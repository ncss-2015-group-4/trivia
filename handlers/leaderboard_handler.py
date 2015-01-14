from templating import render_template
from db.models import User,Score
from . import template_paths


def leaderboard_handler(request):
    scores = Score.find_all()
    variables={"score_list":[]}
    scores_per_person={}
    for score in scores:
        percentage= (score.num_correct/score.num_answered)*100
        person=User.find(user_id=score.user_id)
        name=person.username
        #variables["score_list"].append([name,percentage])
        if name not in scores_per_person:
            scores_per_person[name]=percentage
        else:
            scores_per_person[name]=(scores_per_person[name] + percentage)/2
        
    score_list = list(scores_per_person.items())
    score_list.sort(key=lambda score_entry: score_entry[1], reverse=True)
    
    new_score_list=[]
    for score_entry in score_list:
        score_entry=list(score_entry)
        score_entry[1] = str(round(score_entry[1],2))+"%"
        new_score_list.append(score_entry)
    
    variables['score_list'] = new_score_list

    names = ["John", "Jack", "Kenni", "Ben", "Tony"]
    
    u_id = request.get_secure_cookie ('user_id')
    u_name = ""
    if u_id is not None:
        u_id = u_id.decode("UTF-8")
        u_name = User.find(user_id=u_id)
        u_name = u_name.username
    variables['user_name'] = u_name
    leaderboard = render_template(template_paths["leaderboard"], variables)
    request.write(leaderboard)
