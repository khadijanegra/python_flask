@app.route("/recommander", methods=["GET"])
def recommander():
    user_id = request.args.get("user_id")
    print(f"user_id reçu : {user_id}")  # pour confirmer que tu reçois bien le paramètre
    if not user_id:
        return jsonify({"error": "user_id manquant"}), 400

    try:
        recommandations = recommander_shops_svd(algo, user_id, favoris_df, n=5)
        return jsonify({"user_id": user_id, "recommandations": recommandations})
    except Exception as e:
        # Affiche l’erreur complète dans les logs Flask
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Exception : {str(e)}"}), 500
