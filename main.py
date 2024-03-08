PORT = 1234
DEBUG = True

from flask import Flask , render_template , redirect , request
from urllib.request import urlopen
from urllib.parse import quote

from rdkit import Chem
from rdkit.Chem import Draw

app = Flask(__name__)

def _get_smiles(iupac) -> str:
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + quote(iupac) + '/smiles'
        ans = urlopen(url).read().decode('utf8')
        return ans
    except:
        return '0'
    
def _also_known(iupac) -> str:
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + quote(iupac) + '/names'
        ans = urlopen(url).read().decode('utf8')
        return ans
    except:
        return 'No other names found'

@app.route("/")
def _home():
    return render_template("home.html")

@app.route("/structure/<iupac>")
def _structure(iupac):
    smiles = _get_smiles(iupac)
    if smiles != '0':
        struct = Chem.MolFromSmiles(smiles) # type: ignore

        img = Draw.MolToFile(struct , "static/request.png")

        return render_template('structure.html' , iupac=iupac , names=_also_known(iupac))
    else:
        return "<style>*{background-color: black;color: snow;}</style><h2><center>'"+iupac+"' NOT FOUND</center></h2>"

@app.route('/search' , methods=['POST'])
def search():
    query = request.form['query'].lower()
    return redirect('/structure/'+query)

app.run(port=PORT , debug=DEBUG)