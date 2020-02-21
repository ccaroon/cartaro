from flask import Blueprint

notes = Blueprint('notes', __name__)

@notes.route('/<id>')
def view(id):
    return {
        "id": 0xdeadbeef,
        "title": "How Tu Kung Fu",
        "tags": ['howto', 'karate'],
        "favorite": False,
        "body": """
        lakdsf lkadsf l;akdfj lakdsjf al;kdsjf alksdjf 
        al;dkjfa;lkdsjf a;lkdsfj al;kdsjf a;lkdsfj al;ksdjf alksdjf
        a;lkdfj;aldskjf
        fdlk

        a;dlkfa;ldskfja;ldskfjadsf

        ad;lfkjads;flkjad;sflkj
        """
    }
