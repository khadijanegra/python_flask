from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://khadijanegra2:RqP99wOOdNa5dFB6@cluster0.hpiy1.mongodb.net/")
db = client["test"]
collection = db["users"]

@app.route('/recommander', methods=['GET'])
def recommander():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({"error": "user_id manquant"}), 400

        user = collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "Utilisateur non trouvé"}), 404

        user_df = pd.DataFrame([user])
        user_df['loyalty_score'] = user_df['loyalty_score'].fillna(0)
        user_df['frequency_score'] = user_df['frequency_score'].fillna(0)

        user_df['recommandation_score'] = (
            0.5 * user_df['loyalty_score'] +
            0.3 * user_df['frequency_score'] +
            0.2 * user_df['panier_moyen']
        )

        recommandations = user_df.sort_values(by='recommandation_score', ascending=False)

        return jsonify({"recommandations": recommandations.to_dict(orient="records")})
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erreur depuis le serveur Flask : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
