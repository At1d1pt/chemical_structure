PORT = 1234
DEBUG = True

import concurrent.futures
from flask import Flask , render_template , redirect , request
from urllib.request import urlopen
from urllib.parse import quote

from rdkit import Chem
from rdkit.Chem import Draw

app = Flask(__name__)
   
def _get_smiles_also_names(iupac):
    def fetch_url(url):
        try:
            return urlopen(url).read().decode('utf8')
        except:
            return '0'
    
    url1 = f'http://cactus.nci.nih.gov/chemical/structure/{quote(iupac)}/smiles'
    url2 = f'http://cactus.nci.nih.gov/chemical/structure/{quote(iupac)}/names'
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        a1= executor.submit(fetch_url, url1)
        b1 = executor.submit(fetch_url, url2)
        
        a= a1.result()
        b= b1.result()
    
    if a == '0':
        return '0', 'No other names found'
    
    b = "   ->".join(b.split("\n"))
    return a, b

     
@app.route("/")
def _home():
        return render_template("home.html")

@app.route("/structure/<iupac>")
def _structure(iupac):
            a,b=_get_smiles_also_names(iupac)
            smiles =a

            if smiles != '0':
                struct = Chem.MolFromSmiles(smiles) # type: ignore

                img = Draw.MolToFile(struct , "static/request.png")

                return render_template('structure.html' , iupac=iupac , names=b)
            else:
                return "<style>*{background-color: black;color: snow;}</style><h2><center>'"+iupac+"' NOT FOUND</center></h2>"
@app.route('/search' , methods=['POST'])
def search():
            query = request.form['query'].lower()
            return redirect('/structure/'+query)

app.run(port=PORT , debug=DEBUG)