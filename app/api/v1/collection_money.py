from flask_login import login_required

from app.libs.red_print import RedPrint
from app.models.collection_money import CollectionMoney

api = RedPrint("collection_money")


@api.route("", methods=["GET"])
@login_required
def search_collection_money_api():
    pass
