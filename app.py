from flask import Flask, request, jsonify
from recommandation import recommander_shops_svd, algo, favoris_df

app = Flask(__name__)

@app.route("/recommander", methods=["GET"])
def recommander():
    user_id = request.args.get("user_id")
    print(f"✅ user_id reçu : {user_id}")
    
    if not user_id:
        return jsonify({"error": "user_id manquant"}), 400

    try:
        recommandations = recommander_shops_svd(algo, user_id, favoris_df, n=5)
        return jsonify({"user_id": user_id, "recommandations": recommandations})
    
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404

  except Exception as e:
    import traceback
    traceback.print_exc()
    return jsonify({"error": f"Erreur depuis le serveur Flask : {str(e)}"}), 500

@app.route("/utilisateurs", methods=["GET"])
def utilisateurs_valides():
    try:
        users = list(favoris_df.index)
        return jsonify({"utilisateurs_valides": users})
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des IDs : {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
