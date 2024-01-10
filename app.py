import pandas as pd
from pulp import *
import streamlit as st

def submit_price():
    st.session_state.price = st.session_state.price_selection
    st.session_state.price_selection = ""

st.set_page_config(page_title="Cardápio semanal", layout="wide")

df = pd.read_excel("./data/diet.xlsx")
df_contraints = pd.read_excel("./data/diet - contraints.xlsx")

# df["deletar"] = [False for i in range(df.shape[0])]

list_food = df['Foods'].sort_values().unique().tolist()

st.header("Cálculo do cardápio semanal de custo mínimo")
st.divider()

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["deletar", "alimento", "preço"])
if 'full' not in st.session_state:
    st.session_state.full = df.copy()
if 'price' not in st.session_state:
    st.session_state.price = ""

a1,a2,a3 = st.columns([5, 0.25, 2])

with st.sidebar:
    st.subheader('Inclusão de alimentos usados na escola e seus preços no dia da pesquisa')

    food = st.selectbox("Selecione o alimento:", list_food, index=None, placeholder='')

    st.text_input("Preço/Kg corrente:", key='price_selection', on_change=submit_price, placeholder='Digite...')
    price = st.session_state.price

    p_isnumber = False
    if price != "":
        try:
            price = float(price)
            p_isnumber = True
        except:
            st.error("Preço deve ser um número!")

    delete = False
    df_temp = pd.DataFrame({"deletar": [delete],
                            "alimento": [food],
                            "preço": [price]})

    if st.button("Adicionar alimento e preço") and p_isnumber == True and food != '':
        st.session_state.price = ''
        st.session_state.df = pd.concat([st.session_state.df, df_temp])
        st.toast("Adicionado.")

    if 'df' not in st.session_state:
        st.session_state.df.copy()

    if st.toggle("Mostrar os alimentos adicionados"):
        st.session_state.df = st.data_editor(st.session_state.df
                                             .drop_duplicates(subset=["alimento"], keep='last')
                                             .reset_index(drop=True),
                                             column_config={
                                                 "deletar": st.column_config.CheckboxColumn("deletar", default=False)
                                                },
                                             hide_index=True,
                                             use_container_width=True)
        st.write("Quantidade de alimentos adicionados:", st.session_state.df.shape[0])
        # Deletar os registros que não queremos mais. -> Clica duas vezes na caixinha de seleção
        st.session_state.df = st.session_state.df[st.session_state.df["deletar"] == False]

    st.subheader('Informações adicionais')

    rice = st.radio("Deve ter arroz todos os dias?", ["Sim", "Não"])
    bean = st.radio("Deve ter feijão todos os dias?", ["Sim", "Não"])

    # de acordo com a PNAE
    list_ages = ["7 - 11 meses", "1 - 3 anos", "4 - 5 anos", 
                 "6 - 10 anos", "11 - 15 anos", "16 - 18 anos"]
    ages = st.selectbox("Selecione a faixa etária:", list_ages, index=None, placeholder='')
        
    if st.button("Salvar tudo e calcular o cardápio semanal de custo mínimo."):
        st.toast("OK")
        with a1:
            df_merge = st.session_state.df[["alimento", "preço"]].merge(df, left_on='alimento', right_on='Foods')

            prob = LpProblem("Simple_Diet_Problem", LpMinimize)
            food_items = list(df_merge['Foods'])
            st.text(food_items)
            costs = dict(zip(food_items, df_merge['preço']))
            calories = dict(zip(food_items, df_merge['Calories']))
            cholesterol = dict(zip(food_items, df_merge['Cholesterol (mg)']))
            fat = dict(zip(food_items, df_merge['Total_Fat (g)']))
            protein = dict(zip(food_items, df_merge['Protein (g)']))
            fiber = dict(zip(food_items, df_merge['Dietary_Fiber (g)']))
            sodium = dict(zip(food_items, df_merge['Sodium (mg)']))
            vit_a = dict(zip(food_items, df_merge['Vit_A (IU)']))
            calcium = dict(zip(food_items, df_merge['Calcium (mg)']))
            iron = dict(zip(food_items, df_merge['Iron (mg)']))
            vit_c = dict(zip(food_items, df_merge['Vit_C (IU)']))
            carbs = dict(zip(food_items, df_merge['Carbohydrates (g)']))

            food_vars = LpVariable.dicts("Food", food_items, lowBound=0, cat='Integer') # ou Continuous
            st.text(food_vars)

            prob += lpSum([costs[i]*food_vars[i] for i in food_items])
            st.text(prob)

            prob += lpSum([calories[f] * food_vars[f] for f in food_items]) >= df_contraints.loc[0, 'Calories'] # limite inferior
            prob += lpSum([calories[f] * food_vars[f] for f in food_items]) <= df_contraints.loc[1, 'Calories'] # limite superior

            prob += lpSum([fat[f] * food_vars[f] for f in food_items]) >= df_contraints.loc[0, 'Total_Fat (g)'] # limite inferior
            prob += lpSum([fat[f] * food_vars[f] for f in food_items]) <= df_contraints.loc[1, 'Total_Fat (g)'] # limite superior

            prob += lpSum([protein[f] * food_vars[f] for f in food_items]) >= df_contraints.loc[0, 'Protein (g)'] # limite inferior
            prob += lpSum([protein[f] * food_vars[f] for f in food_items]) <= df_contraints.loc[1, 'Protein (g)'] # limite superior

            prob += lpSum([fiber[f] * food_vars[f] for f in food_items]) >= df_contraints.loc[0, 'Dietary_Fiber (g)'] # limite inferior
            prob += lpSum([fiber[f] * food_vars[f] for f in food_items]) <= df_contraints.loc[1, 'Dietary_Fiber (g)'] # limite superior

            prob += lpSum([carbs[f] * food_vars[f] for f in food_items]) >= df_contraints.loc[0, 'Carbohydrates (g)'] # limite inferior
            prob += lpSum([carbs[f] * food_vars[f] for f in food_items]) <= df_contraints.loc[1, 'Carbohydrates (g)'] # limite superior
            st.text(prob)


            status = prob.solve()
            st.text(f"Status -> {LpStatus[status]}")
            for v in prob.variables():
                if v.varValue >= 0:
                    st.text(f'{v.name} = {v.varValue:.4f}')
            obj = value(prob.objective)
            st.text(f"{obj}")
