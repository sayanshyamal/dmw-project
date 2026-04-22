"""Plotly chart helper functions for MediCharge Analytics."""
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ===== COLOR PALETTE =====
GREEN_PALETTE = ['#2E7D5E', '#43A77D', '#6BC4A0', '#A3DFC5', '#D4F0E3']
GREEN_PRIMARY = '#2E7D5E'
GREEN_DARK = '#1B5E40'
GREEN_LIGHT = '#E8F5E9'
BG_COLOR = '#F4FAF7'
RED_ACCENT = '#E53935'

CHART_LAYOUT = dict(
    paper_bgcolor='white',
    plot_bgcolor=BG_COLOR,
    font=dict(family='Inter, Segoe UI, sans-serif', color='#374151'),
    margin=dict(l=40, r=20, t=50, b=40),
    hoverlabel=dict(bgcolor='white', font_size=13, font_family='Inter'),
)


def _apply_layout(fig, title='', height=400):
    fig.update_layout(**CHART_LAYOUT, title=dict(text=title, font=dict(size=16, color=GREEN_DARK)), height=height)
    fig.update_xaxes(gridcolor='#E0E0E0', zeroline=False)
    fig.update_yaxes(gridcolor='#E0E0E0', zeroline=False)
    return fig


# ===== PAGE 2 — EDA CHARTS =====

def histogram(df, col, title):
    fig = px.histogram(df, x=col, nbins=30, color_discrete_sequence=[GREEN_PRIMARY])
    fig.update_traces(marker_line_color='white', marker_line_width=1)
    return _apply_layout(fig, title, 360)


def categorical_bar(df, col, title):
    counts = df[col].value_counts().reset_index()
    counts.columns = [col, 'count']
    fig = px.bar(counts, x=col, y='count', color_discrete_sequence=[GREEN_PRIMARY], text='count')
    fig.update_traces(textposition='outside', marker_line_color='white', marker_line_width=1)
    return _apply_layout(fig, title, 360)


def avg_charge_bar(df, col, title):
    avg = df.groupby(col)['charges'].mean().reset_index()
    colors = [GREEN_DARK if v == avg['charges'].max() else GREEN_PRIMARY for v in avg['charges']]
    fig = go.Figure(go.Bar(x=avg[col], y=avg['charges'], marker_color=colors,
                           text=[f'₹{v:,.0f}' for v in avg['charges']], textposition='outside'))
    fig.update_layout(xaxis_title=col.capitalize(), yaxis_title='Avg Charges (₹)')
    return _apply_layout(fig, title, 380)


def scatter_smoker(df, x_col, title):
    fig = px.scatter(df, x=x_col, y='charges', color='smoker',
                     color_discrete_map={'yes': RED_ACCENT, 'no': GREEN_PRIMARY},
                     opacity=0.65, hover_data=['age', 'bmi', 'region'])
    return _apply_layout(fig, title, 400)


def scatter_basic(df, x_col, title):
    fig = px.scatter(df, x=x_col, y='charges', color_discrete_sequence=[GREEN_PRIMARY], opacity=0.6)
    return _apply_layout(fig, title, 400)


def box_smoker(df):
    fig = px.box(df, x='smoker', y='charges', color='smoker',
                 color_discrete_map={'yes': RED_ACCENT, 'no': GREEN_PRIMARY},
                 category_orders={'smoker': ['no', 'yes']})
    fig.update_layout(showlegend=False)
    return _apply_layout(fig, 'Charges: Smokers vs Non-Smokers', 420)


# ===== PAGE 3 — INSIGHT CHARTS =====

def correlation_heatmap(df):
    corr = df[['age', 'bmi', 'children', 'charges']].corr()
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.columns,
        colorscale=[[0, 'white'], [0.5, '#A3DFC5'], [1, GREEN_DARK]],
        text=np.round(corr.values, 2), texttemplate='%{text}', textfont=dict(size=14),
        hovertemplate='%{x} vs %{y}: %{z:.2f}<extra></extra>'
    ))
    fig = _apply_layout(fig, 'Correlation Heatmap', 450)
    fig.update_layout(margin=dict(l=70, r=20, t=50, b=70))
    return fig


def region_smoker_bar(df):
    avg = df.groupby(['region', 'smoker'])['charges'].mean().reset_index()
    fig = px.bar(avg, x='region', y='charges', color='smoker', barmode='group',
                 color_discrete_map={'yes': RED_ACCENT, 'no': GREEN_PRIMARY},
                 text_auto='.0f')
    fig.update_traces(texttemplate='₹%{y:,.0f}', textposition='outside')
    fig.update_layout(yaxis_title='Avg Charges (₹)')
    return _apply_layout(fig, 'Average Charge by Region & Smoker Status', 420)


def bmi_category_bar(df):
    df = df.copy()
    bins = [0, 18.5, 25, 30, 100]
    labels = ['Underweight', 'Normal', 'Overweight', 'Obese']
    df['bmi_cat'] = pd.cut(df['bmi'], bins=bins, labels=labels)
    avg = df.groupby('bmi_cat', observed=False)['charges'].mean().reset_index()
    colors = [GREEN_DARK if v == avg['charges'].max() else GREEN_PRIMARY for v in avg['charges']]
    fig = go.Figure(go.Bar(x=avg['bmi_cat'], y=avg['charges'], marker_color=colors,
                           text=[f'₹{v:,.0f}' for v in avg['charges']], textposition='outside'))
    fig.update_layout(xaxis_title='BMI Category', yaxis_title='Avg Charges (₹)')
    return _apply_layout(fig, 'Average Charges by BMI Category', 400)


def age_group_bar(df):
    df = df.copy()
    bins = [17, 35, 50, 100]
    labels = ['Young (18-35)', 'Middle (36-50)', 'Senior (51+)']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)
    avg = df.groupby('age_group', observed=False)['charges'].mean().reset_index()
    colors = [GREEN_DARK if v == avg['charges'].max() else GREEN_PRIMARY for v in avg['charges']]
    fig = go.Figure(go.Bar(x=avg['age_group'], y=avg['charges'], marker_color=colors,
                           text=[f'₹{v:,.0f}' for v in avg['charges']], textposition='outside'))
    fig.update_layout(xaxis_title='Age Group', yaxis_title='Avg Charges (₹)')
    return _apply_layout(fig, 'Average Charges by Age Group', 400)


# ===== PAGE 4 — PREDICTOR CHARTS =====

def gauge_chart(predicted_charge):
    fig = go.Figure(go.Indicator(
        mode='gauge+number',
        value=predicted_charge,
        number=dict(prefix='₹', font=dict(size=28, color=GREEN_DARK)),
        gauge=dict(
            axis=dict(range=[1000, 65000], tickprefix='₹', tickfont=dict(size=11)),
            bar=dict(color=GREEN_DARK),
            bgcolor='white',
            steps=[
                dict(range=[1000, 10000], color='#E8F5E9'),
                dict(range=[10000, 25000], color='#FFF8E1'),
                dict(range=[25000, 65000], color='#FFEBEE'),
            ],
            threshold=dict(line=dict(color=RED_ACCENT, width=3), thickness=0.8, value=predicted_charge)
        )
    ))
    gauge_layout = {**CHART_LAYOUT, 'margin': dict(l=30, r=30, t=30, b=10)}
    fig.update_layout(**gauge_layout, height=300)
    return fig


def comparison_bar(predicted, avg_charge, max_charge):
    categories = ['Your Prediction', 'Dataset Average', 'Dataset Maximum']
    values = [predicted, avg_charge, max_charge]
    colors = [GREEN_DARK, GREEN_PRIMARY, '#A3DFC5']
    fig = go.Figure(go.Bar(x=categories, y=values, marker_color=colors,
                           text=[f'₹{v:,.0f}' for v in values], textposition='outside'))
    fig.update_layout(yaxis_title='Charges (₹)', showlegend=False)
    return _apply_layout(fig, 'Charge Comparison', 340)


def feature_importance_bar(model, feature_names):
    coefs = model.coef_
    sorted_idx = np.argsort(np.abs(coefs))
    fig = go.Figure(go.Bar(
        y=[feature_names[i] for i in sorted_idx],
        x=[coefs[i] for i in sorted_idx],
        orientation='h',
        marker_color=[RED_ACCENT if coefs[i] < 0 else GREEN_PRIMARY for i in sorted_idx],
        text=[f'{coefs[i]:,.1f}' for i in sorted_idx],
        textposition='outside'
    ))
    fig.update_layout(xaxis_title='Coefficient Value', yaxis_title='')
    return _apply_layout(fig, 'Key Factors Affecting Charge (Model Coefficients)', 400)


# We need pandas for bmi_category_bar / age_group_bar
import pandas as pd
