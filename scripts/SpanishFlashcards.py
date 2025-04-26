# GUI-based Spanish to English Flashcard App
import tkinter as tk
from tkinter import ttk
import random

# Spanish to English vocabulary
flashcards = {'Las citas': 'The appointments', 'El doctor': 'The doctor', 'El dentista': 'The dentist', 'La oficina': 'The office', 'La cita de trabajo': 'The work appointment', 'La peluquería': 'The hair salon', 'La visita': 'The visit', 'La visita médica': 'The medical visit', 'Estar disponible': 'To be available', 'Tomar una cita': 'To take an appointment', 'Reprogramar la cita': 'To reschedule the appointment', 'Estar atrasado/a': 'To be late', 'Estar en anticipo': 'To be early', 'Disponible': 'Available', 'Perro': 'Dog', 'Gato': 'Cat', 'Computadora': 'Computer', 'Programar': 'To program', 'Aprender': 'To learn', 'Enseñar': 'To teach', 'La ropa': 'Clothing', 'El vestido': 'Dress', 'La camisa': 'Shirt', 'La camiseta': 'T-shirt', 'Los pantalones': 'Pants', 'Los pantalones cortos': 'Shorts', 'La ropa interior': 'Underwear', 'La blusa': 'Blouse', 'La falda': 'Skirt', 'El traje': 'Suit', 'El traje de baño': 'Swimsuit', 'El calcetín': 'Sock', 'El suéter': 'Sweater', 'La corbata': 'Tie', 'Los zapatos': 'Shoes', 'Las botas': 'Boots', 'Las zapatillas': 'Sneakers', 'El sombrero': 'Hat', 'El bolso': 'Purse/Bag', 'El cinturón': 'Belt', 'El abrigo': 'Coat', 'El centro comercial': 'Shopping mall', 'Ir de compras': 'To go shopping', 'Probar': 'To try on', 'El clima': 'The weather', 'Hace calor': 'It is hot', 'Hace frío': 'It is cold', 'Hace buen tiempo': 'The weather is nice', 'Hace mal tiempo': 'The weather is bad', 'Hace sol': 'It is sunny', 'Nublado': 'Cloudy', 'Soleado': 'Sunny', 'Hay viento': 'It is windy', 'La nieve': 'The snow', 'Está nevando': 'It is snowing', 'La lluvia': 'The rain', 'Está lluvioso': 'It is rainy', 'La tormenta': 'The storm', 'Está tormentoso': 'It is stormy', 'Las nubes': 'The clouds', 'El trueno': 'The thunder', 'El relámpago': 'The lightning', 'La primavera': 'Spring', 'El verano': 'Summer', 'El otoño': 'Autumn/Fall', 'El invierno': 'Winter', 'El sol': 'The sun', 'La luna': 'The moon', '¿Qué tiempo hace hoy?': 'What is the weather like today?', '¿Cómo está el clima hoy?': 'How is the weather today?', 'Las indicaciones': 'Directions', 'Lugares': 'Places', 'La tienda': 'The store', 'La escuela': 'The school', 'La biblioteca': 'The library', 'El supermercado': 'The supermarket', 'El edificio': 'The building', 'Estación de tren': 'Train station', 'Estación de autobús': 'Bus station', 'La playa': 'The beach', 'El restaurante': 'The restaurant', 'El parque': 'The park', 'La iglesia': 'The church', 'El cine': 'The cinema', 'El correo': 'The post office', 'La esquina': 'The corner', 'A lado de': 'Next to', 'A la izquierda de': 'To the left of', 'A la derecha de': 'To the right of', 'Detrás de': 'Behind', 'Primero': 'First', 'Luego': 'Then', 'Girar': 'Turn', 'Cruzar': 'Cross', 'Sigue derecho': 'Go straight', 'Entre': 'Between', 'En frente': 'In front', 'Delante de': 'In front of', '¿Dónde está…?': 'Where is…?', '¿Adónde vas?': 'Where are you going?', 'El cuerpo': 'The body', 'La cabeza': 'The head', 'La cara': 'The face', 'Los ojos': 'The eyes', 'Las orejas': 'The ears', 'El pecho': 'The chest', 'Los brazos': 'The arms', 'Las piernas': 'The legs', 'Los pies': 'The feet', 'Las manos': 'The hands', 'Los dedos': 'The fingers', 'Los dedos de pies': 'The toes', 'La espalda': 'The back', 'La rodilla': 'The knee', 'El codo': 'The elbow', 'El hombro': 'The shoulder', 'El tobillo': 'The ankle', 'Los dientes': 'The teeth', 'El estómago': 'The stomach', 'La cadera': 'The hip', 'El pelo': 'The hair', 'El cabello': 'The hair (on head)', 'La muñeca': 'The wrist', 'Tocar': 'To touch', 'Emociones': 'Emotions', 'Feliz': 'Happy', 'Triste': 'Sad', 'Emocionado/a': 'Excited', 'Cansado/a': 'Tired', 'Enfadado/a': 'Angry', 'Enojado/a': 'Angry', 'Preocupado/a': 'Worried', 'Aburrido/a': 'Bored', 'Confundido/a': 'Confused', 'Enamorado/a': 'In love', 'Asustado/a': 'Scared', 'Frustrado/a': 'Frustrated', 'Sorprendido/a': 'Surprised', 'Cómodo/a': 'Comfortable', 'Incómodo/a': 'Uncomfortable', 'Avergonzado/a': 'Embarrassed', 'Tímido/a': 'Shy', 'Nervioso/a': 'Nervous', 'Ansioso/a': 'Anxious', 'Sentirse': 'To feel', 'Los animales': 'The animals', 'El gato': 'The cat', 'El perro': 'The dog', 'El pájaro': 'The bird', 'El elefante': 'The elephant', 'El león': 'The lion', 'El oso': 'The bear', 'El caballo': 'The horse', 'El tigre': 'The tiger', 'El toro': 'The bull', 'La tortuga': 'The turtle', 'El cerdo': 'The pig', 'La vaca': 'The cow', 'La oveja': 'The sheep', 'El pato': 'The duck', 'Correr': 'To run', 'Caminar': 'To walk', 'Saltar': 'To jump', 'Rápido': 'Fast', 'Despacio': 'Slow'}

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spanish Flashcards")
        
        self.main_frame = ttk.Frame(self.root, padding="30 30 30 30")
        self.main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.spanish_label = ttk.Label(self.main_frame, text="Press 'Next' to start!", font=('Helvetica', 18))
        self.spanish_label.grid(column=0, row=0, columnspan=2, pady=20)
        
        self.translation_label = ttk.Label(self.main_frame, text="", font=('Helvetica', 18))
        self.translation_label.grid(column=0, row=1, columnspan=2, pady=20)
        
        self.next_button = ttk.Button(self.main_frame, text="Next", command=self.next_flashcard)
        self.next_button.grid(column=0, row=2, pady=20)
        
        self.reveal_button = ttk.Button(self.main_frame, text="Reveal", command=self.reveal_translation)
        self.reveal_button.grid(column=1, row=2, pady=20)
    
    def next_flashcard(self):
        self.spanish_word, self.english_translation = random.choice(list(flashcards.items()))
        self.spanish_label.config(text=self.spanish_word)
        self.translation_label.config(text="")
    
    def reveal_translation(self):
        self.translation_label.config(text=self.english_translation)

def main():
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
