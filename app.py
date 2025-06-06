from flask import Flask, request, jsonify
from recommandation import recommander_shops_svd, algo, favoris_df

app = Flask(__name__)

@app.route("/recommander", methods=["GET"])
def recommander():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id manquant"}), 400

    try:
        recommandations = recommander_shops_svd(algo, user_id, favoris_df, n=5)
        return jsonify({"user_id": user_id, "recommandations": recommandations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5001)
