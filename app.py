import pandas as pd
from pulp import *
import random
import streamlit as st

from utils import create_list

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
        loc_contraints = 0
    elif qt_meals == "Parcial tarde - 1 refeição por dia":
        meals = ['Lanche da tarde']
        loc_contraints = 0
    elif qt_meals == "Parcial manhã - 2 refeições por dia":
        meals = ['Lanche da manhã', 'Almoço']
        loc_contraints = 2
    elif qt_meals == "Parcial tarde - 2 refeições por dia":
        meals = ['Lanche da tarde', 'Jantar']
        loc_contraints = 2
    elif qt_meals == "Integral - 3 refeições por dia":
        meals = ['Lanche da manhã', 'Almoço', 'Lanche da tarde']
        loc_contraints = 4
    else:
        meals = ['Lanche da manhã', 'Almoço', 'Lanche da tarde', 'Jantar']
        loc_contraints = 4

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
            df_merge = st.session_state.df[["alimento", "preço", "refeição"]].merge(df, left_on='alimento', right_on='Alimento')
            df_result = pd.DataFrame()
            food_items = list(df_merge['Alimento'])
            food_items_copy = food_items.copy()
            for j in range(0, days):
                st.text(food_items)
                st.text(food_items_copy)
                prob = LpProblem("Simple_Diet_Problem", LpMinimize)
                df_merge_filtered = df_merge.query(f"alimento in {food_items_copy}")
                costs = dict(zip(food_items_copy, df_merge_filtered['preço']))
                energy = dict(zip(food_items_copy, df_merge_filtered['Energia (kcal)']))
                protein = dict(zip(food_items_copy, df_merge_filtered['Proteínas (g)']))
                carbs = dict(zip(food_items_copy, df_merge_filtered['Carboidratos (g)']))
                lip = dict(zip(food_items_copy, df_merge_filtered['Lipídios (g)']))
                st.text(lip)

                if rice == 'Sim':
                    for f in food_items_copy:
                        if 'Arroz' in f:
                            if ages == '4 - 5 anos':
                                qt_rice = 0.3
                            else:
                                qt_rice = 0.5
                            rice_var = f
                            food_vars_rice = LpVariable.dicts("Rice", [rice_var], lowBound=qt_rice, cat='Continuous') # ou Integer
                            break
                if bean == 'Sim':
                    for f in food_items_copy:
                        if 'Feijão' in f:
                            if ages == '4 - 5 anos':
                                qt_bean = 0.15
                            else:
                                qt_bean = 0.25
                            bean_var = f
                            food_vars_bean = LpVariable.dicts("Bean", [bean_var], lowBound=qt_bean, cat='Continuous') # ou Integer
                            break
                food_vars = LpVariable.dicts("Food", [i for i in food_items_copy if i not in [rice_var, bean_var]], lowBound=0, cat='Continuous') # ou Integer
                food_vars.update(food_vars_rice)
                food_vars.update(food_vars_bean)

                prob += lpSum([costs[i]*food_vars[i] for i in food_items_copy])

                df_contraints_age_range = df_contraints.query(f"`Faixa etaria` == '{ages}'").reset_index()
                prob += lpSum([energy[f] * food_vars[f] for f in food_items_copy]) >= df_contraints_age_range.loc[loc_contraints, 'Energia'] # limite inferior
                prob += lpSum([energy[f] * food_vars[f] for f in food_items_copy]) <= df_contraints_age_range.loc[loc_contraints + 1, 'Energia'] # limite superior

                prob += lpSum([protein[f] * food_vars[f] for f in food_items_copy]) >= df_contraints_age_range.loc[loc_contraints, 'Proteinas'] # limite inferior
                prob += lpSum([protein[f] * food_vars[f] for f in food_items_copy]) <= df_contraints_age_range.loc[loc_contraints + 1, 'Proteinas'] # limite superior

                prob += lpSum([carbs[f] * food_vars[f] for f in food_items_copy]) >= df_contraints_age_range.loc[loc_contraints, 'Carboidratos'] # limite inferior
                prob += lpSum([carbs[f] * food_vars[f] for f in food_items_copy]) <= df_contraints_age_range.loc[loc_contraints + 1, 'Carboidratos'] # limite superior

                prob += lpSum([lip[f] * food_vars[f] for f in food_items_copy]) >= df_contraints_age_range.loc[loc_contraints, 'Lipidios'] # limite inferior
                prob += lpSum([lip[f] * food_vars[f] for f in food_items_copy]) <= df_contraints_age_range.loc[loc_contraints + 1, 'Lipidios'] # limite superior
                
                df_grouped = df_merge_filtered.groupby('refeição')['alimento'].apply(create_list).reset_index()
                if df_grouped.shape[0] > 1:
                    for g, row in df_grouped.iterrows():
                        if row['refeição'] == 'Almoço' and df_grouped.shape[0] == 2:
                            ref = 2/3
                        elif row['refeição'] == 'Almoço' and df_grouped.shape[0] == 3:
                            ref = 3/7
                        elif 'Lanche' in row['refeição'] and df_grouped.shape[0] == 2:
                            ref = 1/3
                        elif 'Lanche' in row['refeição'] and df_grouped.shape[0] == 3:
                            ref = 2/7
                        prob += lpSum([energy[f] * food_vars[f] for f in row['alimento']]) >= df_contraints_age_range.loc[loc_contraints, 'Energia']*ref # limite inferior
                        prob += lpSum([energy[f] * food_vars[f] for f in row['alimento']]) <= df_contraints_age_range.loc[loc_contraints + 1, 'Energia']*ref # limite superior
                        prob += lpSum([protein[f] * food_vars[f] for f in row['alimento']]) >= df_contraints_age_range.loc[loc_contraints, 'Proteinas']*ref # limite inferior
                        prob += lpSum([protein[f] * food_vars[f] for f in row['alimento']]) <= df_contraints_age_range.loc[loc_contraints + 1, 'Proteinas']*ref # limite superior
                        prob += lpSum([carbs[f] * food_vars[f] for f in row['alimento']]) >= df_contraints_age_range.loc[loc_contraints, 'Carboidratos']*ref # limite inferior
                        prob += lpSum([carbs[f] * food_vars[f] for f in row['alimento']]) <= df_contraints_age_range.loc[loc_contraints + 1, 'Carboidratos']*ref # limite superior
                        prob += lpSum([lip[f] * food_vars[f] for f in row['alimento']]) >= df_contraints_age_range.loc[loc_contraints, 'Lipidios']*ref # limite inferior
                        prob += lpSum([lip[f] * food_vars[f] for f in row['alimento']]) <= df_contraints_age_range.loc[loc_contraints + 1, 'Lipidios']*ref # limite superior
                
                st.text(prob)

                status = prob.solve()
                st.text(f"Status -> {LpStatus[status]}")
                food_selected = []
                qtd_food_selected = []
                for v in prob.variables():
                    if v.varValue > 0:
                        food_selected.append(v.name.replace('Food', '').replace('Rice', '').replace('Bean', '').replace('_', ' ').strip())
                        qtd_food_selected.append(round(v.varValue, 4))
                obj = value(prob.objective)
                st.text(f"Custo -> {obj}")
                df_result_temp = pd.DataFrame({'alimento': food_selected, 'qtd (g)': qtd_food_selected, 'day': j})
                df_result = pd.concat([df_result, df_result_temp])
                if rice == 'Sim' and bean == 'Sim':
                    food_selected_removed = [fs for fs in food_selected if 'Arroz' not in fs and 'Feijão' not in fs]
                elif rice == 'Sim' and bean == 'Não': 
                    food_selected_removed = [fs for fs in food_selected if 'Arroz' not in fs]
                elif rice == 'Não' and bean == 'Sim':
                    food_selected_removed = [fs for fs in food_selected if 'Feijão' not in fs]
                else:
                    food_selected_removed = food_selected.copy()
                food_items_random = random.sample(food_selected_removed, 2)
                food_items_copy = food_items.copy()
                for fi in food_items_random:
                    food_items_copy.remove(fi)
            st.data_editor(df_result)
