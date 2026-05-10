import streamlit as st

# ─── Renk paleti ───────────────────────────────────────────────
BG       = "#0b0f19"
SIDEBAR  = "#0d1424"
CARD     = "#111827"
BORDER   = "#1a2540"
BORDER2  = "#243050"
TEXT1    = "#f1f5f9"
TEXT2    = "#94a3b8"
TEXT3    = "#64748b"
BLUE     = "#3b82f6"
GREEN    = "#10b981"
RED      = "#ef4444"
ORANGE   = "#f59e0b"

def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    #MainMenu, footer {{ visibility: hidden !important; }}
    [data-testid="stHeader"] {{ background: transparent !important; border: none !important; }}
    [data-testid="stDecoration"] {{ display: none !important; }}

    /* ── App ── */
    .stApp {{
        background: {BG} !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: {SIDEBAR} !important;
        border-right: 1px solid {BORDER} !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{ padding-top: 0 !important; }}

    [data-testid="stSidebarNav"] {{ padding: 4px 10px !important; }}
    [data-testid="stSidebarNav"] a {{
        border-radius: 8px !important;
        color: {TEXT3} !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        padding: 9px 12px !important;
        margin: 1px 0 !important;
        transition: all 0.12s !important;
    }}
    [data-testid="stSidebarNav"] a:hover {{
        background: rgba(59,130,246,0.08) !important;
        color: #93c5fd !important;
    }}
    [data-testid="stSidebarNav"] a[aria-selected="true"] {{
        background: rgba(59,130,246,0.12) !important;
        color: {BLUE} !important;
        font-weight: 600 !important;
    }}

    /* ── İçerik alanı ── */
    .block-container {{
        padding: 24px 32px 48px 32px !important;
        max-width: 100% !important;
    }}

    /* ── Başlıklar ── */
    h1 {{
        color: {TEXT1} !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        background: none !important;
        -webkit-text-fill-color: {TEXT1} !important;
        margin-bottom: 0 !important;
        line-height: 1.2 !important;
    }}
    h2 {{ color: {TEXT1} !important; font-size: 1rem !important; font-weight: 600 !important; margin: 0 !important; }}
    h3 {{ color: {TEXT2} !important; font-size: 0.95rem !important; font-weight: 600 !important; margin: 0 !important; }}
    p  {{ color: {TEXT3}; margin: 0 !important; }}
    label {{ color: {TEXT2} !important; font-size: 0.82rem !important; font-weight: 500 !important; }}

    /* ── Metric ── */
    [data-testid="metric-container"] {{
        background: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
        padding: 20px 22px !important;
        box-shadow: none !important;
    }}
    [data-testid="metric-container"]:hover {{
        transform: none !important;
        box-shadow: none !important;
        border-color: {BORDER} !important;
    }}
    [data-testid="metric-container"] label,
    [data-testid="stMetricLabel"] {{
        color: {TEXT1} !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
    }}
    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricLabel"] div,
    [data-testid="stMetricLabel"] span {{
        color: {TEXT1} !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
    }}
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] *,
    [data-testid="stMetricValue"] p,
    [data-testid="stMetricValue"] div {{
        color: {TEXT1} !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricDelta"] {{
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }}
    [data-testid="stMetricDelta"] svg {{ display: none !important; }}

    /* ── Input'lar ── */
    [data-testid="stSelectbox"] > div[data-baseweb] > div,
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stPasswordInput"] input {{
        background: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
        color: {TEXT1} !important;
        font-size: 0.9rem !important;
    }}
    [data-testid="stSelectbox"] > div[data-baseweb] > div:hover {{
        border-color: {BORDER2} !important;
    }}
    [data-testid="stTextInput"] input:focus,
    [data-testid="stPasswordInput"] input:focus,
    [data-testid="stNumberInput"] input:focus {{
        border-color: {BORDER} !important;
        box-shadow: none !important;
        outline: none !important;
    }}
    [data-testid="stTextInput"] input,
    [data-testid="stPasswordInput"] input,
    [data-testid="stNumberInput"] input {{
        box-shadow: none !important;
        outline: none !important;
    }}
    [aria-invalid="true"] {{
        border-color: {BORDER} !important;
        box-shadow: none !important;
    }}
    [data-testid="stPasswordInput"] [data-baseweb="input"],
    [data-testid="stTextInput"] [data-baseweb="input"],
    [data-testid="stNumberInput"] [data-baseweb="input"] {{
        border-color: {BORDER} !important;
        box-shadow: none !important;
    }}
    [data-baseweb="popover"] > div {{
        background: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
    }}
    [role="option"] {{ background: {CARD} !important; color: {TEXT1} !important; }}
    [role="option"]:hover {{ background: rgba(59,130,246,0.1) !important; }}

    /* ── Butonlar ── */
    [data-testid="baseButton-primary"],
    button[kind="primary"] {{
        background: {BLUE} !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }}
    [data-testid="baseButton-primary"]:hover,
    button[kind="primary"]:hover {{
        background: #2563eb !important;
        transform: none !important;
        box-shadow: none !important;
    }}
    [data-testid="baseButton-primary"] p,
    button[kind="primary"] p {{
        color: white !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }}
    /* ── Form submit butonları ── */
    [data-testid="stFormSubmitButton"] button,
    button[kind="primaryFormSubmit"] {{
        background: {BLUE} !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }}
    [data-testid="stFormSubmitButton"] button:hover,
    button[kind="primaryFormSubmit"]:hover {{
        background: #2563eb !important;
    }}
    [data-testid="stFormSubmitButton"] button p,
    button[kind="primaryFormSubmit"] p {{
        color: white !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }}

    [data-testid="baseButton-secondary"],
    button[kind="secondary"] {{
        background: transparent !important;
        border: 1px solid {BORDER2} !important;
        border-radius: 8px !important;
        color: {TEXT2} !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
    }}
    [data-testid="baseButton-secondary"]:hover,
    button[kind="secondary"]:hover {{
        border-color: #334155 !important;
        color: {TEXT1} !important;
        transform: none !important;
        box-shadow: none !important;
        background: rgba(255,255,255,0.03) !important;
    }}

    /* ── Tabs ── */
    [data-baseweb="tab-list"] {{
        background: transparent !important;
        gap: 0 !important;
        padding: 0 !important;
        border-bottom: 1px solid {BORDER} !important;
    }}
    [data-baseweb="tab"] {{
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        color: {TEXT3} !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 10px 20px !important;
        margin-bottom: -1px !important;
    }}
    [data-baseweb="tab"][aria-selected="true"] {{
        background: transparent !important;
        border-bottom: 2px solid {BLUE} !important;
        color: {BLUE} !important;
        font-weight: 600 !important;
    }}

    /* ── Expander ── */
    [data-testid="stExpander"] {{
        background: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
    }}
    [data-testid="stExpander"] summary {{
        color: {TEXT2} !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        padding: 12px 16px !important;
    }}

    /* ── Alerts ── */
    [data-testid="stAlert"] {{ border-radius: 8px !important; }}
    .stSuccess {{ background: rgba(16,185,129,0.08) !important; border-left: 3px solid {GREEN} !important; color: #6ee7b7 !important; }}
    .stError   {{ background: rgba(239,68,68,0.08)  !important; border-left: 3px solid {RED}   !important; color: #fca5a5 !important; }}
    .stWarning {{ background: rgba(245,158,11,0.08) !important; border-left: 3px solid {ORANGE} !important; color: #fcd34d !important; }}
    .stInfo    {{ background: rgba(59,130,246,0.08) !important; border-left: 3px solid {BLUE}  !important; color: #93c5fd !important; }}

    /* ── Form ── */
    [data-testid="stForm"] {{
        background: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }}

    /* ── Divider ── */
    hr {{ border-color: {BORDER} !important; margin: 20px 0 !important; }}

    /* ── Spinner ── */
    [data-testid="stSpinner"] > div {{ border-top-color: {BLUE} !important; }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track {{ background: {BG}; }}
    ::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {BLUE}; }}

    /* ── Caption / small ── */
    .stCaption, small {{ color: #475569 !important; }}

    /* ── Number input butonları ── */
    [data-testid="stNumberInput"] button {{
        background: {BORDER} !important;
        border-color: {BORDER} !important;
        color: {TEXT2} !important;
    }}

    /* ── Page link ── */
    [data-testid="stPageLink"] a {{
        background: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
        color: {BLUE} !important;
    }}

    /* ── Mobil ── */
    @media (max-width: 768px) {{
        .block-container {{
            padding: 12px 8px 32px 8px !important;
        }}
        [data-testid="stSidebar"] {{
            min-width: 0 !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)


def sidebar_header(kullanici=None):
    """Logo + kullanıcı profilini sidebar'a ekler."""
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:18px 16px 14px 16px; border-bottom:1px solid {BORDER}; margin-bottom:4px;">
            <div style="font-size:1.05rem; font-weight:800; color:{TEXT1}; letter-spacing:-0.01em;">
                BIST <span style="color:{BLUE};">Analytics</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if kullanici:
            ad = kullanici.get("kullanici_adi", "Kullanıcı")
            initials = ad[:2].upper()
            st.markdown(f"""
            <div style="padding:10px 12px; margin:8px 4px 4px 4px;
                background:rgba(59,130,246,0.06); border-radius:8px; border:1px solid {BORDER};">
                <div style="display:flex;align-items:center;gap:10px;">
                    <div style="width:32px;height:32px;border-radius:7px;
                        background:linear-gradient(135deg,{BLUE},#1d4ed8);
                        display:flex;align-items:center;justify-content:center;
                        font-weight:700;color:white;font-size:12px;flex-shrink:0;">{initials}</div>
                    <div>
                        <div style="color:{TEXT1};font-weight:600;font-size:0.85rem;line-height:1.3;">{ad}</div>
                        <div style="color:{TEXT3};font-size:0.72rem;">Pro Trader</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="padding:10px 14px; margin:8px 4px 4px 4px;
                background:{CARD}; border-radius:8px; border:1px solid {BORDER};">
                <div style="color:{TEXT3};font-size:0.8rem;text-align:center;">🔐 Giriş yapılmadı</div>
            </div>
            """, unsafe_allow_html=True)


def page_header(icon, title, subtitle=None, badge=None):
    """Sayfa üst başlığı."""
    badge_html = (f'<span style="background:{BORDER};color:{TEXT2};font-size:0.72rem;font-weight:600;'
                  f'padding:4px 10px;border-radius:6px;border:1px solid {BORDER2};">{badge}</span>') if badge else ""
    sub_html = (f'<p style="color:{TEXT3};font-size:0.85rem;margin:4px 0 0 0;">{subtitle}</p>') if subtitle else ""
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:24px;">
        <div style="display:flex;align-items:center;gap:12px;">
            <span style="font-size:1.8rem;">{icon}</span>
            <div>
                <h1 style="margin:0;font-size:1.75rem;font-weight:700;color:{TEXT1};
                    -webkit-text-fill-color:{TEXT1};background:none;">{title}</h1>
                {sub_html}
            </div>
        </div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)


def section_label(text):
    """Küçük bölüm etiketi (DEĞERLEME, FİNANSALLAR vb.)."""
    st.markdown(f"""
    <div style="color:{TEXT3};font-size:0.72rem;font-weight:600;
        text-transform:uppercase;letter-spacing:0.08em;margin:24px 0 12px 0;">{text}</div>
    """, unsafe_allow_html=True)


def plotly_cfg(**kwargs):
    """Standart plotly koyu tema layout kwargs."""
    cfg = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=CARD,
        font=dict(family="Inter, sans-serif", color=TEXT3, size=11),
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=TEXT3), zeroline=False),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=TEXT3), zeroline=False),
        margin=dict(l=8, r=8, t=48, b=8),
        legend=dict(font=dict(color=TEXT2, size=11), bgcolor="rgba(0,0,0,0)",
                    orientation="h", x=0, y=1.06, xanchor="left", yanchor="bottom"),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1e293b", bordercolor=BORDER, font=dict(color=TEXT1)),
    )
    cfg.update(kwargs)
    return cfg


def card_html(content, padding="20px 24px"):
    """HTML kart wrapper."""
    return (f'<div style="background:{CARD};border:1px solid {BORDER};'
            f'border-radius:12px;padding:{padding};">{content}</div>')
