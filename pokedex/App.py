from flask import Flask, render_template, redirect, url_for, flash
import requests


class Pokedex():
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'pwnedglowcode'
        self.api = 'https://pokeapi.co/api/v2/type/'
        self.pokemon_api = 'https://pokeapi.co/api/v2/pokemon/'
        self.routes()

    def pokemones_stats(self, nombre):
        response = requests.get(f'{self.pokemon_api}{nombre}')

        if response.status_code == 200:
            informacion_completa = response.json()
            idPokemon = informacion_completa['id']
            nombre = informacion_completa['name']
            photo = informacion_completa['sprites']['front_default']
            altura = informacion_completa['height']
            peso = informacion_completa['weight']
            experiencia = informacion_completa['base_experience']
            
            tipos = informacion_completa['types']
            tipoPokemon = tipos[0]['type']['name']
            tipoPokemon2 = tipos[1]['type']['name'] if len(tipos) > 1 else None

            return render_template('pokemon.html', 
                                   informacion_completa=informacion_completa, 
                                   nombre=nombre, 
                                   photo=photo, 
                                   idPokemon=idPokemon, 
                                   tipoPokemon=tipoPokemon, 
                                   tipoPokemon2=tipoPokemon2, 
                                   altura=altura, 
                                   peso=peso,
                                   experiencia = experiencia)
            
        else:
            flash('Lo siento, no se pudo obtener información de ese pokemon')
            return redirect(url_for('categorias'))



    def routes(self):
        @self.app.route('/', methods=['POST', 'GET'])
        def index():
            return render_template('index.html')



        @self.app.route('/categorias', methods=['GET'])
        def categorias():
            tipos = ["fire", "water", "grass", "electric", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dark", "dragon", "steel", "fairy"]
            return render_template('categorias.html', tipos=tipos)


        @self.app.route('/pokemones/<tipo>', methods=['GET', 'POST'])
        def pokemones(tipo):
            response = requests.get(f'{self.api}{tipo}')
            data = response.json()
            pokemones = [pokemon['pokemon']['name'] for pokemon in data['pokemon']]
            total = len(pokemones)
            return render_template('pokemones.html', pokemones=pokemones, tipo=tipo, total=total)


        @self.app.route('/pokemon_info/<nombre>', methods=['GET', 'POST'])
        def pokemon_info(nombre):
            return self.pokemones_stats(nombre)
        
        
        
        @self.app.errorhandler(404)
        def page_not_found(e):
            return render_template('404.html'), 404


        @self.app.errorhandler(500)
        def internal_server_error(e):
            return render_template('500.html'), 500
    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    pokedex = Pokedex()
    pokedex.run()
