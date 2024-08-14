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

st.header("Cardápios formulados")
st.divider()

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["deletar", "alimento", "preço"])
if 'full' not in st.session_state:
    st.session_state.full = df.copy()
if 'price' not in st.session_state:
    st.session_state.price = ""

a1,a2,a3 = st.columns([5, 0.25, 0.1])

with st.sidebar:
    st.subheader('Seleção e preenchimento de informações para formulação de cardápios de custo mínimo')

    # de acordo com a PNAE
    list_ages = ["4 - 5 anos", "6 - 10 anos", "11 - 15 anos", "16 - 18 anos"]
    ages = st.selectbox("Selecione a faixa etária:", list_ages, index=None, placeholder='Selecione...')
    meals_period = ["Parcial manhã - 1 refeição por dia", "Parcial tarde - 1 refeição por dia",
                    "Parcial manhã - 2 refeições por dia", "Parcial tarde - 2 refeições por dia",
                    "Integral - 3 refeições por dia"]

    qt_meals = st.selectbox("Selecione o período e a quantidade de refeições diárias:",
                            meals_period,
                            index=None, placeholder='Selecione...', disabled=not ages)
    
    if qt_meals == "Parcial manhã - 1 refeição por dia":
        meals = ['Lanche da manhã']
        loc_contraints = 0
    elif qt_meals == "Parcial tarde - 1 refeição por dia":
        meals = ['Lanche da tarde']
        loc_contraints = 0
    elif qt_meals == "Parcial manhã - 2 refeições por dia":
        meals = ['Lanche da manhã', 'Almoço ou Jantar']
        loc_contraints = 2
    elif qt_meals == "Parcial tarde - 2 refeições por dia":
        meals = ['Lanche da tarde', 'Almoço ou Jantar']
        loc_contraints = 2
    elif qt_meals == "Integral - 3 refeições por dia":
        meals = ['Lanche da manhã', 'Almoço ou Jantar', 'Lanche da tarde']
        loc_contraints = 4

    food = st.selectbox("Selecione os alimentos usados na escola:", list_food, 
                        index=None, placeholder='Selecione...', key='food_selection',
                        disabled=not (qt_meals and ages))

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
    rice_options_selected = [r for r in st.session_state.df['alimento'].unique() if 'Arroz' in r]
    rice = st.radio("Deve ter arroz todos os dias?", ["Sim", "Não"], horizontal=True, disabled=not rice_options_selected)
    rice_var = ''
    food_vars_rice = {}
    bean_options_selected = [r for r in st.session_state.df['alimento'].unique() if 'Feijão' in r]
    bean = st.radio("Deve ter feijão todos os dias?", ["Sim", "Não"], horizontal=True, disabled=not bean_options_selected)
    bean_var = ''
    food_vars_bean = {}
    days = st.selectbox("Quantidade de dias para calcular o cardápio:", [1, 2, 3, 4, 5], 
                        index=None, placeholder='', disabled=st.session_state.df.empty)
    
    if st.button("Salvar tudo e formular o(s) cardápio(s) de custo mínimo.", disabled=st.session_state.df.empty):
        st.toast("OK")
        with a1:
            df_merge = st.session_state.df[["alimento", "preço", "refeição"]].merge(df, left_on='alimento', right_on='Alimento')
            df_merge['alimento'] = df_merge['alimento'] + df_merge['refeição']
            df_result = pd.DataFrame()
            df_costs_status = pd.DataFrame()
            food_items = list(df_merge['alimento'])
            food_items_copy = food_items.copy()
            for j in range(1, days + 1):
                prob = LpProblem("Simple_Diet_Problem", LpMinimize)
                df_merge_filtered = df_merge.query(f"alimento in {food_items_copy}")
                costs = dict(zip(food_items_copy, df_merge_filtered['preço']))
                energy = dict(zip(food_items_copy, df_merge_filtered['Energia (kcal)']))
                protein = dict(zip(food_items_copy, df_merge_filtered['Proteínas (g)']))
                carbs = dict(zip(food_items_copy, df_merge_filtered['Carboidratos (g)']))
                lip = dict(zip(food_items_copy, df_merge_filtered['Lipídios (g)']))

                for f in food_items_copy:
                    if 'Arroz' in f:
                        qt_rice = 0.5
                        rice_var = f
                        food_vars_rice = LpVariable.dicts("Rice", [rice_var], lowBound=qt_rice, upBound=qt_rice, cat='Continuous')
                        break
                for f in food_items_copy:
                    if 'Feijão' in f:
                        qt_bean = 0.25
                        bean_var = f
                        food_vars_bean = LpVariable.dicts("Bean", [bean_var], lowBound=qt_bean, upBound=qt_bean, cat='Continuous')
                        break
                food_vars = LpVariable.dicts("Food", [i for i in food_items_copy if i not in [rice_var, bean_var]], lowBound=0, cat='Continuous')
                food_vars.update(food_vars_rice)
                food_vars.update(food_vars_bean)

                prob += lpSum([costs[i]*food_vars[i] for i in food_items_copy])

                df_contraints_age_range = df_contraints.query(f"`Faixa etaria` == '{ages}'").reset_index()
                
                df_grouped = df_merge_filtered.groupby('refeição')['alimento'].apply(create_list).reset_index()
                for g, row in df_grouped.iterrows():
                    if df_grouped.shape[0] == 1 and '1' in qt_meals:
                        ref = 1
                    elif (row['refeição'] == 'Almoço ou Jantar' and df_grouped.shape[0] == 2 and '2' in qt_meals) or row['refeição'] == 'Almoço ou Jantar' and df_grouped.shape[0] == 1 and '2' in qt_meals:
                        ref = 2/3
                    elif (row['refeição'] == 'Almoço ou Jantar' and df_grouped.shape[0] == 3 and '3' in qt_meals) or (row['refeição'] == 'Almoço ou Jantar' and df_grouped.shape[0] == 2 and '3' in qt_meals) or (row['refeição'] == 'Almoço ou Jantar' and df_grouped.shape[0] == 1 and '3' in qt_meals):
                        ref = 3/7
                    elif ('Lanche' in row['refeição'] and df_grouped.shape[0] == 2 and '2' in qt_meals) or ('Lanche' in row['refeição'] and df_grouped.shape[0] == 1 and '2' in qt_meals):
                        ref = 1/3
                    elif ('Lanche' in row['refeição'] and df_grouped.shape[0] == 3 and '3' in qt_meals) or ('Lanche' in row['refeição'] and df_grouped.shape[0] == 2 and '3' in qt_meals) or ('Lanche' in row['refeição'] and df_grouped.shape[0] == 1 and '3' in qt_meals):
                        ref = 2/7
                    prob += lpSum([energy[f] * food_vars[f] for f in row['alimento']]) >= int(round(df_contraints_age_range.loc[loc_contraints, 'Energia']*ref, 0)) # limite inferior
                    prob += lpSum([energy[f] * food_vars[f] for f in row['alimento']]) <= int(round(df_contraints_age_range.loc[loc_contraints + 1, 'Energia']*ref, 0)) # limite superior
                    prob += lpSum([protein[f] * food_vars[f] for f in row['alimento']]) >= int(round(df_contraints_age_range.loc[loc_contraints, 'Proteinas']*ref, 0)) # limite inferior
                    prob += lpSum([protein[f] * food_vars[f] for f in row['alimento']]) <= int(round(df_contraints_age_range.loc[loc_contraints + 1, 'Proteinas']*ref, 0)) # limite superior
                    prob += lpSum([carbs[f] * food_vars[f] for f in row['alimento']]) >= int(round(df_contraints_age_range.loc[loc_contraints, 'Carboidratos']*ref, 0)) # limite inferior
                    prob += lpSum([carbs[f] * food_vars[f] for f in row['alimento']]) <= int(round(df_contraints_age_range.loc[loc_contraints + 1, 'Carboidratos']*ref, 0)) # limite superior
                    prob += lpSum([lip[f] * food_vars[f] for f in row['alimento']]) >= int(round(df_contraints_age_range.loc[loc_contraints, 'Lipidios']*ref, 0)) # limite inferior
                    prob += lpSum([lip[f] * food_vars[f] for f in row['alimento']]) <= int(round(df_contraints_age_range.loc[loc_contraints + 1, 'Lipidios']*ref, 0)) # limite superior
                solver = get_solver('CPLEX_PY')
                status = prob.solve(solver)
                status = LpStatus[status]
                food_selected = []
                qtd_food_selected = []
                for v in prob.variables():
                    if v.varValue > 0:
                        food_selected.append(v.name.replace('Food', '').replace('Rice', '').replace('Bean', '').replace('_', ' ').strip())
                        qtd_food_selected.append(f"{str(round(v.varValue * 100, 3)).replace('.', ',')}g")
                obj = f"R$ {str(value(prob.objective)).replace('.', ',')}"
                df_result_temp = pd.DataFrame({'alimento': food_selected, 'qtd (g)': qtd_food_selected, 'dia': f"dia {j}"})
                df_result = pd.concat([df_result, df_result_temp])
                df_costs_status_temp = pd.DataFrame({'dia': f"dia {j}", 'custo': [obj], 'status': status.replace('Infeasible', 'Inviável').replace('Optimal', 'Ótimo')})
                df_costs_status = pd.concat([df_costs_status, df_costs_status_temp])
                if rice == 'Sim' and bean == 'Sim':
                    food_selected_removed = [fs for fs in food_selected if 'Arroz' not in fs and 'Feijão' not in fs]
                elif rice == 'Sim' and bean == 'Não': 
                    food_selected_removed = [fs for fs in food_selected if 'Arroz' not in fs]
                elif rice == 'Não' and bean == 'Sim':
                    food_selected_removed = [fs for fs in food_selected if 'Feijão' not in fs]
                else:
                    food_selected_removed = food_selected.copy()
                # st.text(f"food_selected_removed -> {food_selected_removed}")

                food_selected_removed_lunch_dinner = [i for i in df_merge_filtered.query("refeição == 'Almoço ou Jantar'")['alimento'].tolist() if i in food_selected_removed]
                if food_selected_removed_lunch_dinner:
                    try:
                        food_items_random_lunch_dinner = random.sample(food_selected_removed_lunch_dinner, 2)
                    except:
                        food_items_random_lunch_dinner = random.sample(food_selected_removed_lunch_dinner, 1)
                else:
                    food_items_random_lunch_dinner = []
                food_selected_removed_coffee_1 = [i for i in df_merge_filtered.query("refeição == 'Lanche da manhã'")['alimento'].tolist() if i in food_selected_removed]
                if food_selected_removed_coffee_1:
                    food_items_random_coffee_1 = random.sample(food_selected_removed_coffee_1, 1)
                else:
                    food_items_random_coffee_1 = []
                food_selected_removed_coffee_2 = [i for i in df_merge_filtered.query("refeição == 'Lanche da tarde'")['alimento'].tolist() if i in food_selected_removed]
                if food_selected_removed_coffee_2:
                    food_items_random_coffee_2 = random.sample(food_selected_removed_coffee_2, 1)
                else:
                    food_items_random_coffee_2 = []
                food_items_random = food_items_random_lunch_dinner + food_items_random_coffee_1 + food_items_random_coffee_2
                food_items_copy = food_items.copy()
                # st.text(f"food_items_random -> {food_items_random}")
                for fi in food_items_random:
                    food_items_copy.remove(fi)
            
            df_result = df_result.merge(df_merge[['alimento', 'refeição']], on='alimento').sort_values(by=['dia', 'refeição'])
            df_result['alimento'] = df_result.apply(lambda x: x['alimento'].replace(x['refeição'], '').strip(), axis=1)
            for meal in list(df_result['refeição'].unique()):
                st.subheader(f"Cardápio para o {meal.lower()}")
                st.data_editor(df_result.query(f"refeição == '{meal}'").pivot(index='alimento', columns='dia', values='qtd (g)').fillna('-'))
            st.subheader(f"Custo do cardápio por aluno e status do cálculo por dia")
            st.data_editor(pd.concat([df_costs_status.pivot(columns='dia', values='custo').rename(index={0: 'Custo'}),
                                        df_costs_status.pivot(columns='dia', values='status').rename(index={0: 'Status'})]).fillna('-'))
            st.text('Se o status não for igual a Ótimo, tente adicionar mais alimentos na seleção ou adapte o cardápio gerado para aquele dia da forma que preferir.')

    st.divider()
    with open("data/manual_utilizacao.pdf", "rb") as pdf_file:
        document = pdf_file.read()
        st.download_button(
            label="Baixar manual de utilização da plataforma",
            data=document,
            file_name='manual_plataforma.pdf',
            mime='application/pdf',
        )
