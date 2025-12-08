import streamlit as st
import pandas as pd
import ast 
from src.recomendador import (
    cargar_dataset,
    obtener_recomendaciones_df,
    obtener_lista_generos
)

# --- Configuración Inicial ---
st.set_page_config(
    page_title="Recomendador de Películas", 
    layout="wide" 
)

# Inicialización de Session State (para mantener el estado de los filtros)
if 'show_results' not in st.session_state:
    st.session_state['show_results'] = False
if 'generos' not in st.session_state:
    st.session_state['generos'] = []
if 'perfil' not in st.session_state:
    st.session_state['perfil'] = 'mainstream'
if 'orden' not in st.session_state:
    st.session_state['orden'] = 'Weighted Rating (Default)'


# Cargar los datos una sola vez y cachearlos
@st.cache_data
def load_data_once():
    return cargar_dataset()

# --- NUEVA FUNCIÓN CACHEADA PARA CARGAR GÉNEROS ---
@st.cache_data
def load_genres_once():
    return obtener_lista_generos()

data = load_data_once()
generos_disponibles_dataset = load_genres_once() # <-- CARGAMOS LA LISTA COMPLETA
# ----------------------------------------------------


# --- Título y Descripción ---
st.title("Recomendador de Películas")
st.write("Selecciona tus preferencias para obtener recomendaciones.")
st.markdown("---")


# --- Controles de Filtro (Sección Superior) ---

col_genero, col_popularidad, col_orden = st.columns([1.5, 1, 1]) 

with col_genero:
    generos_seleccionados = st.multiselect(
        label="Selecciona género(s):",
        options=generos_disponibles_dataset, # <-- USAMOS GÉNEROS DINÁMICOS
        default=st.session_state['generos'],
        key="generos_select" 
    )

with col_popularidad:
    popularidad_perfil = st.radio(
        label="Popularidad:",
        options=['Mainstream', 'Mixed', 'Niche'],
        horizontal=True,
        index=['Mainstream', 'Mixed', 'Niche'].index(st.session_state['perfil'].capitalize()) if st.session_state['perfil'] in ['mainstream', 'mixed', 'niche'] else 0,
        key="perfil_radio" 
    )
    perfil_seleccionado_lower = popularidad_perfil.lower()

with col_orden:
    criterio_orden = st.selectbox(
        label="Ordenar por:",
        options=[
            'Weighted Rating (Default)', 
            'Año de Estreno (Reciente)', 
            'Número de Votos'
        ],
        index=['Weighted Rating (Default)', 'Año de Estreno (Reciente)', 'Número de Votos'].index(st.session_state['orden']),
        key="orden_select"
    )

col_buscar, col_limpiar, col_espacio = st.columns([1, 1, 3])

with col_buscar:
    if st.button("Buscar películas", type="primary", use_container_width=True):
        st.session_state['show_results'] = True
        st.session_state['generos'] = generos_seleccionados
        st.session_state['perfil'] = perfil_seleccionado_lower
        st.session_state['orden'] = criterio_orden 
        st.rerun() 

with col_limpiar:
    if st.button("Limpiar Filtros", use_container_width=True):
        st.session_state['show_results'] = False
        st.session_state['generos'] = []
        st.session_state['perfil'] = 'mainstream'
        st.session_state['orden'] = 'Weighted Rating (Default)' 
        st.rerun()
        
# ----------------------------------------------------------------------
# --- SECCIÓN DE RESULTADOS ---
# ----------------------------------------------------------------------

if st.session_state.get('show_results', False):
    
    st.markdown("---")
    st.subheader("🎬 Recomendaciones para ti")
    
    perfil_script = st.session_state['perfil']
    generos_seleccionados_state = st.session_state['generos']
    criterio_orden_state = st.session_state.get('orden', 'Weighted Rating (Default)') 
    
    resultados_df = obtener_recomendaciones_df(
        generos_seleccionados_state,
        perfil_script, 
        data,
        orden=criterio_orden_state
    )

    if resultados_df.empty:
        st.warning("No se encontraron películas con esos filtros. Intenta con otras opciones.")
    else:
        # --- ESTILO CSS INYECTADO PARA LA ALINEACIÓN Y DISEÑO DE TARJETA ---
        st.markdown("""
        <style>
        .recommendation-container {
            display: flex;
            align-items: center; /* Centrado vertical de la imagen */
            gap: 20px; /* Espacio entre imagen y texto */
            padding: 15px;
            border: 1px solid #333;
            border-radius: 5px;
            margin-bottom: 10px;
            background-color: #1E1E1E; /* Fondo oscuro de la tarjeta */
        }
        .poster-column {
            flex-basis: 150px; /* Ancho fijo para la imagen */
            display: flex;
            justify-content: center; /* Centrado horizontal de la imagen */
            align-items: center; 
        }
        .text-column {
            flex-grow: 1;
        }
        </style>
        """, unsafe_allow_html=True)
        # ------------------------------------------------------------------


        for index, row in resultados_df.iterrows():
            
            # Obtiene y formatea los valores
            year_display = int(row['year']) if not pd.isna(row.get('year')) else 'N/A'
            wr_display = row.get('wr')
            votes_display = row.get('votes')
            poster_url = row.get('poster_url') 

            # Formateo de géneros
            genres_value = row['genres']
            try:
                # Intenta evaluar si es una cadena con formato de lista de Python
                genres_list = ast.literal_eval(genres_value)
            except (ValueError, TypeError, SyntaxError):
                genres_list = genres_value

            if isinstance(genres_list, str):
                genres_to_display = [genres_list] 
            elif isinstance(genres_list, list):
                genres_to_display = genres_list
            else:
                genres_to_display = [str(genres_list)]

            # Generación del contenido HTML/Markdown (TEXTO)
            genres_html = f"**Géneros:** {', '.join(genres_to_display)}"
            
            votes_html = ""
            if votes_display is not None and not pd.isna(votes_display):
                 votes_html = f"**Votos:** {int(votes_display):,}"
            
            rating_html = ""
            if wr_display is not None and not pd.isna(wr_display):
                 rating_html = f"**Rating (WR):** **{wr_display:.2f}** / 10"
            else:
                 rating_html = f"**Rating (WR):** N/A"


            # Construcción del HTML de la tarjeta para usar el CSS personalizado
            html_content = f"""
            <div class="recommendation-container">
                <div class="poster-column">
                    <img src="{poster_url or 'https://via.placeholder.com/120x180?text=No+Poster'}" 
                         width="120" 
                         style="border-radius: 4px;">
                </div>
                <div class="text-column">
                    <h4>{row['primaryTitle']} ({year_display})</h4>
                    <p>{genres_html}</p>
                    <p>{votes_html}</p>
                    <p>{rating_html}</p>
                </div>
            </div>
            """
            
            # Renderizar la tarjeta
            st.markdown(html_content, unsafe_allow_html=True)