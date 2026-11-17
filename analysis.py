import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Segoe UI', 'Arial', 'sans-serif']
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.0


def load_data():
    df1 = pd.read_csv(os.path.join(current_dir, 'table1.csv'))
    df2 = pd.read_csv(os.path.join(current_dir, 'table2.csv'))
    return df1, df2


def run_analysis():
    df1, df2 = load_data()

    rub_df = df1[df1['currency'] == 'RUB']
    elec_city = float(rub_df[rub_df['item_name'].str.contains('Городской')]['total_value'].iloc[0])
    elec_comm = float(rub_df[rub_df['item_name'].str.contains('Коммерческий')]['total_value'].iloc[0])
    rtx_cost = float(rub_df[rub_df['item_name'].str.contains('RTX 4090')]['total_value'].iloc[0])
    asic_cost = float(rub_df[rub_df['item_name'].str.contains('Antminer')]['total_value'].iloc[0])
    vps_month = float(rub_df[rub_df['item_name'].str.contains('VPS')]['total_value'].iloc[0])
    domain_year = float(rub_df[rub_df['item_name'].str.contains('Доменное')]['total_value'].iloc[0])

    vps_year = vps_month * 12.0
    infra_year = vps_year + domain_year
    hardware_total = rtx_cost + asic_cost
    sw_cost = float(df1[df1['category'] == 'software_components']['total_value'].iloc[0])

    crypto_df = df1[df1['category'] == 'market_baseline'].copy()

    loss_pct = float(df2[df2['item_name'].str.contains('сливших')]['quantity'].iloc[0])
    liq_days = float(df2[df2['item_name'].str.contains('ликвидации')]['quantity'].iloc[0])
    tam_users = float(df2[df2['item_name'].str.contains('Целевая аудитория')]['quantity'].iloc[0])
    avg_dep = float(df2[df2['item_name'].str.contains('первого депозита')]['total_value'].iloc[0])
    no_sl_pct = float(df2[df2['item_name'].str.contains('Stop-Loss')]['quantity'].iloc[0])
    conv_pct = float(df2[df2['item_name'].str.contains('Конверсия')]['quantity'].iloc[0])

    stud_row = df2[df2['provider'].str.contains('ИРНИТУ')].iloc[0]
    stud_yes = float(stud_row['quantity'])
    stud_total = float(stud_row['total_value'])
    stud_share = (stud_yes / stud_total) * 100.0

    infra_to_hw_ratio = np.round((infra_year / hardware_total) * 100, 2)

    print("=" * 82)
    print("        АНАЛИЗ ДАННЫХ (TABLE1.CSV И TABLE2.CSV) — ОБОСНОВАНИЕ SYNTHEX")
    print("=" * 82)
    print("\n1. ОБОСНОВАНИЕ ПОЛЕЗНОСТИ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ (данные table2.csv):")
    print(f"   • {loss_pct:.0f}% новичков теряют первый депозит в среднем размером ${avg_dep:.0f} USDT в первые 30 дней.")
    print(f"   • {no_sl_pct:.0f}% сделок совершаются без защитного ордера Stop-Loss, а при плече >50x")
    print(f"     среднее время до полной ликвидации составляет всего {liq_days:.0f} дней.")
    print(f"   • Потенциальная аудитория новичков (TAM) — {tam_users:,.0f} человек; локальный опрос")
    print(f"     в ИРНИТУ подтвердил, что {stud_yes:.0f} из {stud_total:.0f} ({stud_share:.0f}%) студентов хотят торговать,")
    print("     но опасаются потери реальных средств. Симулятор полностью снимает этот барьер.")

    print("\n2. ЭКОНОМИЧЕСКАЯ ЦЕЛЕСООБРАЗНОСТЬ И ДОСТУПНОСТЬ (данные table1.csv):")
    print(f"   • Покупка оборудования для изучения реального майнинга требует {hardware_total:,.0f} ₽")
    print(f"     (RTX 4090 — {rtx_cost:,.0f} ₽, ASIC Antminer S19 Pro — {asic_cost:,.0f} ₽) без учета")
    print(f"     тарифов на электроэнергию ({elec_city:.2f} ₽ город. / {elec_comm:.2f} ₽ комм. за кВт·ч).")
    print(f"   • Годовая поддержка всей платформы SynthEx (VPS + домен) стоит всего {infra_year:,.0f} ₽,")
    print(f"     что составляет {infra_to_hw_ratio:.2f}% от стоимости одного комплекта оборудования,")
    print(f"     а графический движок (Lightweight Charts) используется бесплатно (${sw_cost:.0f}).")

    print("\n3. ПЕРСПЕКТИВА ВОВЛЕЧЕНИЯ АУДИТОРИИ (данные table1.csv и table2.csv):")
    print(f"   • По статистике MOEX, {conv_pct:.0f}% пользователей переходят с демо-счета на реальный рынок.")
    print(f"   • Наличие реальных рыночных ориентиров по ключевым активам (BTC — ${crypto_df.iloc[0]['total_value']:,.2f},")
    print(f"     ETH — ${crypto_df.iloc[1]['total_value']:,.2f}, SOL — ${crypto_df.iloc[3]['total_value']:,.2f}, TON — ${crypto_df.iloc[2]['total_value']:,.2f})")
    print("     делает обучение максимально приближенным к практике и формирует сильный инженерный кейс.")

    fig = plt.figure(figsize=(16, 11.5), facecolor='#f8fafc')
    gs = fig.add_gridspec(2, 2, hspace=0.38, wspace=0.28)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#ffffff')
    y_labels = [
        'Конверсия с демо-счета\nна реальный (MOEX)',
        'Сделки новичков без\nStop-Loss (Kaggle)',
        'Новички, слившие 1-й депозит\nза < 30 дней (Binance Research)'
    ]
    y_vals = [conv_pct, no_sl_pct, loss_pct]
    colors1 = ['#3b82f6', '#f59e0b', '#ef4444']
    bars1 = ax1.barh(y_labels, y_vals, color=colors1, height=0.5, edgecolor='#475569', linewidth=0.8)
    ax1.set_xlim(0, 105)
    ax1.set_xlabel('Доля от исследуемой группы (%)', fontsize=10, color='#334155')
    ax1.set_title('1. Поведенческие показатели новичков (table2.csv)', fontsize=11.5, fontweight='bold', pad=12, color='#0f172a')
    ax1.grid(axis='x', linestyle='--', alpha=0.5, color='#cbd5e1')
    for bar in bars1:
        w = bar.get_width()
        ax1.text(w + 2, bar.get_y() + bar.get_height() / 2, f'{w:.0f}%',
                 va='center', ha='left', fontweight='bold', fontsize=10, color='#1e293b')

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#ffffff')
    cost_labels = [
        f'Видеокарта RTX 4090 ({int(rtx_cost):,} ₽)'.replace(',', ' '),
        f'ASIC Antminer S19 Pro ({int(asic_cost):,} ₽)'.replace(',', ' '),
        f'Запуск SynthEx: VPS + Домен/год ({int(infra_year):,} ₽)'.replace(',', ' '),
        f'Электроэнергия 1000 кВт·ч ({int(elec_comm):,} ₽)'.replace(',', ' ')
    ]
    cost_values = [rtx_cost, asic_cost, infra_year, elec_comm]
    colors2 = ['#6366f1', '#8b5cf6', '#10b981', '#94a3b8']
    wedges, _ = ax2.pie(
        cost_values,
        startangle=140,
        colors=colors2,
        wedgeprops=dict(width=0.42, edgecolor='white', linewidth=2)
    )
    ax2.legend(
        wedges,
        [f"{lbl} — {val / sum(cost_values) * 100:.1f}%" for lbl, val in zip(cost_labels, cost_values)],
        loc='lower center',
        bbox_to_anchor=(0.5, -0.22),
        ncol=1,
        frameon=True,
        facecolor='#ffffff',
        edgecolor='#cbd5e1',
        fontsize=8.5
    )
    ax2.set_title('2. Затраты: реальный майнинг vs запуск SynthEx (table1.csv)', fontsize=11.5, fontweight='bold', pad=12, color='#0f172a')
    ax2.text(0, 0, 'SynthEx\n4.1% от затрат\nна железо', ha='center', va='center', fontsize=9, fontweight='bold', color='#059669')

    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor('#ffffff')
    assets = crypto_df['item_name'].tolist()
    prices = crypto_df['total_value'].values
    x_pos = np.arange(len(assets))

    ax3.vlines(x=x_pos, ymin=0, ymax=prices, color='#0284c7', linewidth=3, alpha=0.8)
    ax3.scatter(x_pos, prices, color='#0369a1', s=110, zorder=3, label='Стартовая котировка (USDT)')
    ax3.set_yscale('log')
    ax3.set_ylim(1, 500000)
    ax3.set_xlim(-0.5, 3.6)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(assets, fontweight='bold', fontsize=10, color='#1e293b')
    ax3.set_ylabel('Цена актива, USDT (лог. шкала)', fontsize=10, color='#334155')
    ax3.set_title('3. Базовые котировки активов из API бирж (table1.csv)', fontsize=11.5, fontweight='bold', pad=12, color='#0f172a')
    ax3.grid(True, which='major', linestyle='--', alpha=0.5, color='#cbd5e1')
    ax3.legend(loc='upper right', frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=9)

    for x, p in zip(x_pos, prices):
        ax3.text(x, p * 1.4, f'${p:,.2f}', ha='center', va='bottom', fontweight='bold', fontsize=9.5, color='#0f172a')

    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor('#ffffff')
    metrics_names = [
        'Ср. время до ликвидации\nпри плече >50x (Bybit)',
        'Период слива 1-го депозита\nу 85% новичков (Binance)'
    ]
    metrics_days = [liq_days, 30.0]
    bars4 = ax4.bar(metrics_names, metrics_days, width=0.42, color=['#f97316', '#dc2626'], edgecolor='#475569', linewidth=0.8)
    ax4.set_ylim(0, 40)
    ax4.set_ylabel('Количество дней', fontsize=10, color='#334155')
    ax4.set_title('4. Скорость потери депозита и масштаб аудитории (table2.csv)', fontsize=11.5, fontweight='bold', pad=12, color='#0f172a')
    ax4.grid(axis='y', linestyle='--', alpha=0.5, color='#cbd5e1')

    for b in bars4:
        h = b.get_height()
        ax4.text(b.get_x() + b.get_width() / 2, h + 0.8, f'{h:.0f} дн.',
                 ha='center', va='bottom', fontweight='bold', fontsize=10, color='#1e293b')

    ax4.annotate(
        f'Средний 1-й депозит: ${avg_dep:.0f} USDT (Glassnode)\n'
        f'Целевая аудитория (TAM): {tam_users / 1e6:.0f} млн чел. (CoinGecko)\n'
        f'Опрос ИРНИТУ: {int(stud_yes)} из {int(stud_total)} чел. боятся потерь',
        xy=(0.18, 15.2), xytext=(0.02, 26.5),
        arrowprops=dict(facecolor='#334155', shrink=0.06, width=1.0, headwidth=5),
        fontsize=8.5, fontweight='bold', color='#1e293b',
        bbox=dict(boxstyle='round,pad=0.45', fc='#fef3c7', ec='#f59e0b')
    )

    plt.suptitle('Анализ входных данных (table1.csv и table2.csv) для обоснования проекта SynthEx',
                 fontsize=14.5, fontweight='bold', y=0.97, color='#0f172a')

    output_path = os.path.join(current_dir, 'synthex_clean_analysis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\n[OK] Графики сохранены: {output_path}")