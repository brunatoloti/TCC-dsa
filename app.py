import pandas as pd
from pulp import *
import streamlit as st

def submit_price():
    st.session_state.price = st.session_state.price_selection
    st.session_state.price_selection = ""

st.set_page_config(page_title="Cardápio semanal", layout="wide")

df = pd.read_excel("./data/alimentos.xlsx")
df_contraints = pd.read_excel("./data/alimentos_restricoes.xlsx")

list_food = df['Alimento'].sort_values().unique().tolist()

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
    st.subheader('Seleção de alimentos usados na escola e seus preços no dia da pesquisa')

    # de acordo com a PNAE
    list_ages = ["4 - 5 anos", "6 - 10 anos", "11 - 15 anos", "16 - 18 anos"]
    ages = st.selectbox("Selecione a faixa etária:", list_ages, index=None, placeholder='Selecione...')
    meals_period = ["Parcial manhã - 1 refeição por dia", "Parcial tarde - 1 refeição por dia",
                    "Parcial manhã - 2 refeições por dia", "Parcial tarde - 2 refeições por dia",
                    "Integral - 3 refeições por dia", "Integral - 4 refeições por dia"]

    qt_meals = st.selectbox("Selecione o período e a quantidade de refeições diárias:",
                            meals_period,
                            index=None, placeholder='Selecione...')
    
    if qt_meals == "Parcial manhã - 1 refeição por dia":
        meals = ['Lanche da manhã']
    elif qt_meals == "Parcial tarde - 1 refeição por dia":
        meals = ['Lanche da tarde']
    elif qt_meals == "Parcial manhã - 2 refeições por dia":
        meals = ['Lanche da manhã', 'Almoço']
    elif qt_meals == "Parcial tarde - 2 refeições por dia":
        meals = ['Lanche da tarde', 'Jantar']
    elif qt_meals == "Integral - 3 refeições por dia":
        meals = ['Lanche da manhã', 'Almoço', 'Lanche da tarde']
    else:
        meals = ['Lanche da manhã', 'Almoço', 'Lanche da tarde', 'Jantar']

    food = st.selectbox("Selecione os alimentos usados na escola:", list_food, 
                        index=None, placeholder='Selecione...', key='food_selection')

    if food in list_food:
        meal_type_selection = st.selectbox("Selecione a refeição para qual esse alimento será usado:", meals,
                                           index=None, placeholder='', key='meal_selection')
        st.text_input("Preço/100g corrente:", key='price_selection', on_change=submit_price, placeholder='Digite...')
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
                                "preço": [price],
                                "refeição": [meal_type_selection]})

        if st.button("Adicionar alimento e preço") and p_isnumber == True and food != '':
            st.session_state.price = ''
            st.session_state.df = pd.concat([st.session_state.df, df_temp])
            st.toast("Adicionado.")

    if 'df' not in st.session_state:
        st.session_state.df.copy()

    if st.toggle("Mostrar os alimentos adicionados"):
        st.session_state.df = st.data_editor(st.session_state.df
                                             .drop_duplicates(subset=["alimento", "refeição"], keep='last')
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

    rice = st.radio("Deve ter arroz todos os dias?", ["Sim", "Não"], horizontal=True)
    rice_var = ''
    food_vars_rice = {}
    bean = st.radio("Deve ter feijão todos os dias?", ["Sim", "Não"], horizontal=True)
    bean_var = ''
    food_vars_bean = {}
    days = st.selectbox("Quantidade de dias para calcular o cardápio:", [1, 2, 3, 4, 5], index=None, placeholder='')
        
    if st.button("Salvar tudo e calcular o cardápio semanal de custo mínimo."):
        st.toast("OK")
        with a1:
            df_merge = st.session_state.df[["alimento", "preço"]].merge(df, left_on='alimento', right_on='Alimento')

            prob = LpProblem("Simple_Diet_Problem", LpMinimize)
            food_items = list(df_merge['Alimento'])
            st.text(food_items)
            costs = dict(zip(food_items, df_merge['preço']))
            energy = dict(zip(food_items, df_merge['Energia (kcal)']))
            protein = dict(zip(food_items, df_merge['Proteínas (g)']))
            carbs = dict(zip(food_items, df_merge['Carboidratos (g)']))
            lip = dict(zip(food_items, df_merge['Lipídios (g)']))

            if rice == 'Sim':
                for f in food_items:
                    if 'Arroz' in f:
                        rice_var = f
                        food_vars_rice = LpVariable.dicts("Rice", [rice_var], lowBound=0.5, cat='Continuous') # ou Integer
                        break
                st.text(food_vars_rice)
            if bean == 'Sim':
                for f in food_items:
                    if 'Feijão' in f:
                        bean_var = f
                        food_vars_bean = LpVariable.dicts("Bean", [bean_var], lowBound=0.17, cat='Continuous') # ou Integer
                        break
            food_vars = LpVariable.dicts("Food", [i for i in food_items if i not in [rice_var, bean_var]], lowBound=0, cat='Continuous') # ou Integer
            st.text(food_vars)
            food_vars.update(food_vars_rice)
            food_vars.update(food_vars_bean)
            st.text(food_vars)

            prob += lpSum([costs[i]*food_vars[i] for i in food_items])
            st.text(prob)

            prob += lpSum([energy[f] * food_vars[f] for f in food_items]) >= df_contraints.loc[0, 'Energia'] # limite inferior
            prob += lpSum([energy[f] * food_vars[f] for f in food_items]) <= df_contraints.loc[1, 'Energia'] # limite superior

            prob += lpSum([protein[f] * food_vars[f] for f in food_items]) >= df_contraints.loc[0, 'Proteinas'] # limite inferior
            prob += lpSum([protein[f] * food_vars[f] for f in food_items]) <= df_contraints.loc[1, 'Proteinas'] # limite superior

            prob += lpSum([carbs[f] * food_vars[f] for f in food_items]) >= df_contraints.loc[0, 'Carboidratos'] # limite inferior
            prob += lpSum([carbs[f] * food_vars[f] for f in food_items]) <= df_contraints.loc[1, 'Carboidratos'] # limite superior

            prob += lpSum([lip[f] * food_vars[f] for f in food_items]) >= df_contraints.loc[0, 'Lipidios'] # limite inferior
            prob += lpSum([lip[f] * food_vars[f] for f in food_items]) <= df_contraints.loc[1, 'Lipidios'] # limite superior
            st.text(prob)


            status = prob.solve()
            st.text(f"Status -> {LpStatus[status]}")
            for v in prob.variables():
                if v.varValue > 0:
                    st.text(f'{v.name} = {v.varValue:.4f}')
            obj = value(prob.objective)
            st.text(f"{obj}")
