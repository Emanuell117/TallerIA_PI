import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images from the media/movie/images/ folder"

    def handle(self, *args, **kwargs):
        # 📥 Ruta de la carpeta de imágenes
        images_folder = 'media/movie/images/'

        # ✅ Verifica si la carpeta existe
        if not os.path.exists(images_folder):
            self.stderr.write(f"Images folder '{images_folder}' not found.")
            return

        # ✅ Obtener todas las películas
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        updated_count = 0

        for movie in movies:
            try:
                # 📖 Construir el nombre del archivo de imagen basado en el título
                # El formato esperado es: m_{movie_title}.png
                image_filename = f"m_{movie.title}.png"
                image_path_full = os.path.join(images_folder, image_filename)

                # ✅ Verificar si el archivo de imagen existe
                if os.path.exists(image_path_full):
                    # ❗ Aquí debes actualizar la ruta de la imagen de la película
                    movie.image = os.path.join('movie/images', image_filename)
                    movie.save()
                    updated_count += 1

                    self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
                else:
                    self.stderr.write(f"Image not found for: {movie.title}")

            except Exception as e:
                self.stderr.write(f"Failed to update {movie.title}: {str(e)}")

        # ✅ Al finalizar, muestra cuántas películas se actualizaron
        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies with images from folder."))
