import json
import os
import requests
from django.conf import settings
from django.utils.text import slugify
from .models import Product, Review, Category
from django.contrib.auth.models import User
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Load the environment variables
from dotenv import load_dotenv
load_dotenv()
file_path = os.getenv('FILE_PATH')

# Load the data and perform clustering
products = pd.read_json(file_path)

if 'description' in products.columns and 'category' in products.columns:
    products['combined'] = products['category'] + ' ' + products['description']
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_df=0.95, min_df=2)
    X = vectorizer.fit_transform(products['combined'])
    kmeans = KMeans(n_clusters=10, random_state=42)
    kmeans.fit(X)
    products['cluster'] = kmeans.labels_

def recommend_products_service(search_words):
    search_vector = vectorizer.transform([search_words])
    cluster_centroids = kmeans.cluster_centers_
    similarities = cosine_similarity(search_vector, cluster_centroids)
    most_similar_cluster = np.argmax(similarities)
    recommended_products = products[products['cluster'] == most_similar_cluster].head(4)
    recommended_list = recommended_products[['id', 'title', 'category', 'price', 'rating', 'description', 'image',"reviews"]].to_dict(orient='records')
    return recommended_list

def import_data_service():
    try:
        default_user = User.objects.get(username=os.getenv('ADMIN'))
        with open(file_path, 'r') as file:
            data = json.load(file)

        for item in data:
            category, created = Category.objects.get_or_create(name=item['category'])
            for review in item.get('reviews', []):
                reviewer, created = User.objects.get_or_create(
                    email=review['reviewerEmail'],
                    defaults={'username': review['reviewerName'], 'first_name': review['reviewerName'].split()[0], 'last_name': ' '.join(review['reviewerName'].split()[1:])}
                )

            product = Product.objects.create(
                id=item['id'],
                title=item['title'],
                description=item['description'],
                category=category,
                price=item['price'],
                rating=item['rating'],
                stock=item['stock'],
                user=default_user,
                image=item['image'],
            )

            for review in item.get('reviews', []):
                Review.objects.create(
                    product=product,
                    rating=review['rating'],
                    comment=review['comment'],
                    reviewer=reviewer
                )

    except Exception as e:
        return str(e)
    return "Data imported successfully!"
