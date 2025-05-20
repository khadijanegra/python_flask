import pandas as pd

# Charger le fichier users.csv
users_path = "/home/ordione/Téléchargements/test.users_ahawa.csv"
users_df = pd.read_csv(users_path)

# Afficher les premières lignes pour analyse

# ✅ Vérification des données manquantes
print("🔍 Données manquantes par colonne :")
print(users_df.isnull().sum())

# ✅ Supprimer les doublons (si des lignes sont identiques)
avant = users_df.shape[0]
users_df.drop_duplicates(inplace=True)
après = users_df.shape[0]
print(f"🧹 Doublons supprimés : {avant - après}")

# ✅ (Optionnel) Supprimer les utilisateurs sans aucun favori
# D'abord reconstruire la colonne _favoris si ce n'est pas encore fait
favoris_cols = [col for col in users_df.columns if col.startswith('favoris')]
users_df['_favoris'] = users_df[favoris_cols].values.tolist()
users_df['_favoris'] = users_df['_favoris'].apply(lambda x: [i for i in x if pd.notna(i)])

# Supprimer les lignes sans aucun favori
users_df = users_df[users_df['_favoris'].str.len() > 0]
print(f"✅ Utilisateurs restants après suppression de ceux sans favoris : {len(users_df)}")

users_df.head()

# Extraire toutes les colonnes qui contiennent des favoris
favoris_cols = [col for col in users_df.columns if col.startswith('favoris')]

# Fusionner toutes les colonnes de favoris en une seule liste par ligne
users_df['_favoris'] = users_df[favoris_cols].values.tolist()

# Enlever les valeurs manquantes (NaN) de chaque ligne
users_df['_favoris'] = users_df['_favoris'].apply(lambda x: [i for i in x if pd.notna(i)])

# ✅ Affichage des 5 premières lignes pour vérification
print("✅ Fusion des favoris en une seule colonne :")
print(users_df[['_favoris']].head())

# ✅ (Optionnel) Afficher un exemple complet avec user_id
print("\n📌 Exemple complet (avec user_id) :")
print(users_df[['_id', '_favoris']].head())

from sklearn.preprocessing import MultiLabelBinarizer

# Encoder les favoris (1 si le shop est aimé par l'utilisateur, 0 sinon)
mlb = MultiLabelBinarizer()
favoris_matrix = mlb.fit_transform(users_df['_favoris'])

# Construire un DataFrame où les lignes sont les utilisateurs et les colonnes les shops
favoris_df = pd.DataFrame(favoris_matrix, index=users_df['_id'], columns=mlb.classes_)

favoris_df.head()

from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
import pandas as pd

# 🟢 Étape 1 : construire le DataFrame (user_id, shop_id, rating)
data_list = []

for user_id, row in favoris_df.iterrows():
    for shop_id, liked in row.items():
        if liked == 1:
            data_list.append((user_id, shop_id, 1))

df_surprise = pd.DataFrame(data_list, columns=["userID", "itemID", "rating"])

# 🟢 Étape 2 : chargement des données avec Surprise
reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(df_surprise, reader)

# 🟢 Étape 3 : split en train/test
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# 🟢 Étape 4 : utilisation du modèle SVD
algo = SVD()


# 🟢 Étape 4 : entrainment du modèle SVD
algo.fit(trainset)

# 🟢 Étape 5 : prédiction sur le testset
predictions = algo.test(testset)

# 🟢 Étape 6 : évaluer la performance (RMSE)
rmse = accuracy.rmse(predictions)

def recommander_shops_svd(algo, user_id, favoris_df, n=5):
    shops_aimés = set(favoris_df.loc[user_id][favoris_df.loc[user_id] == 1].index)
    tous_les_shops = set(favoris_df.columns)
    shops_à_prédire = list(tous_les_shops - shops_aimés)

    prédictions = [algo.predict(user_id, shop_id) for shop_id in shops_à_prédire]
    prédictions_ordinées = sorted(prédictions, key=lambda x: x.est, reverse=True)
    top_shops = [pred.iid for pred in prédictions_ordinées[:n]]

    print(f"\n🔮 Shops recommandés pour l'utilisateur {user_id} :")
    for shop_id in top_shops:
        print(f" - {shop_id}")

    return top_shops
liste = recommander_shops_svd(algo, "67f1791bd4b37eec7256fe0a", favoris_df)

