from db.models import User, Game 
def game_handler(request):
    category_id = request.get_field("category_id")
    difficulty = request.get_field("difficulty")


