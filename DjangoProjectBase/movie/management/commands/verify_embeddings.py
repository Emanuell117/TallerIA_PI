import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
import random

class Command(BaseCommand):
    help = "Verify stored embeddings by displaying embeddings of a random movie"

    def handle(self, *args, **kwargs):
        # Get all movies
        movies = Movie.objects.all()
        
        if not movies.exists():
            self.stderr.write("No movies found in the database.")
            return
        
        # ✅ Select a random movie
        random_movie = random.choice(movies)
        
        self.stdout.write(f"Selected movie: '{random_movie.title}'")
        self.stdout.write(f"Description: '{random_movie.description[:100]}...'")
        
        # Retrieve and display the embedding
        try:
            embedding_vector = np.frombuffer(random_movie.emb, dtype=np.float32)
            self.stdout.write(f"Embedding shape: {embedding_vector.shape}")
            self.stdout.write(f"First 10 values: {embedding_vector[:10]}")
            self.stdout.write(f"Last 10 values: {embedding_vector[-10:]}")
            self.stdout.write(f"Min value: {np.min(embedding_vector):.6f}")
            self.stdout.write(f"Max value: {np.max(embedding_vector):.6f}")
            self.stdout.write(f"Mean value: {np.mean(embedding_vector):.6f}")
            
            self.stdout.write(self.style.SUCCESS("Embedding verified successfully."))
            
        except Exception as e:
            self.stderr.write(f"Error retrieving embedding: {e}")
