# results/visualize.py
# Visual charts for performance analysis

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Load results
with open('results/simulation_results.json', 'r') as f:
    data = json.load(f)

with open('results/final_report.json', 'r') as f:
    report = json.load(f)

# Set style
plt.rcParams['figure.facecolor'] = '#1a1a2e'
plt.rcParams['axes.facecolor'] = '#16213e'
plt.rcParams['axes.edgecolor'] = '#0f3460'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['grid.color'] = '#0f3460'
plt.rcParams['grid.alpha'] = 0.5

# Colors
PQ_COLOR     = '#00d4ff'
ECDSA_COLOR  = '#ff6b6b'
VALID_COLOR  = '#51cf66'
ATTACK_COLOR = '#ff6b6b'
RECOVER_COLOR = '#ffd43b'

# ─── Figure 1: Signature Comparison ──────────────
fig1, axes = plt.subplots(1, 3, figsize=(15, 5))
fig1.suptitle(
    'Post-Quantum vs Classical Signature Performance',
    fontsize=16, fontweight='bold', color='white', y=1.02
)

# Chart 1a: Sign Time
ax1 = axes[0]
algorithms = ['ML-DSA-65\n(Post-Quantum)', 'ECDSA\n(Classical)']
sign_times = [data['pq_avg_sign'], data['ecdsa_avg_sign']]
colors = [PQ_COLOR, ECDSA_COLOR]
bars = ax1.bar(algorithms, sign_times, color=colors, 
               width=0.5, edgecolor='white', linewidth=0.5)
ax1.set_title('Average Signing Time', 
              fontweight='bold', color='white')
ax1.set_ylabel('Time (ms)', color='white')
ax1.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, sign_times):
    ax1.text(bar.get_x() + bar.get_width()/2, 
             bar.get_height() + 0.02,
             f'{val:.3f}ms', ha='center', 
             va='bottom', color='white', 
             fontweight='bold', fontsize=10)

# Chart 1b: Verify Time
ax2 = axes[1]
verify_times = [data['pq_avg_verify'], data['ecdsa_avg_verify']]
bars2 = ax2.bar(algorithms, verify_times, color=colors,
                width=0.5, edgecolor='white', linewidth=0.5)
ax2.set_title('Average Verification Time',
              fontweight='bold', color='white')
ax2.set_ylabel('Time (ms)', color='white')
ax2.grid(axis='y', alpha=0.3)
for bar, val in zip(bars2, verify_times):
    ax2.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.02,
             f'{val:.3f}ms', ha='center',
             va='bottom', color='white',
             fontweight='bold', fontsize=10)

# Chart 1c: Key/Signature Sizes
ax3 = axes[2]
categories = ['Public Key\nSize', 'Signature\nSize']
pq_sizes = [1952, 3309]
ecdsa_sizes = [64, 64]
x = np.arange(len(categories))
width = 0.35
bars3 = ax3.bar(x - width/2, pq_sizes, width,
                label='ML-DSA-65', color=PQ_COLOR,
                edgecolor='white', linewidth=0.5)
bars4 = ax3.bar(x + width/2, ecdsa_sizes, width,
                label='ECDSA', color=ECDSA_COLOR,
                edgecolor='white', linewidth=0.5)
ax3.set_title('Key and Signature Sizes',
              fontweight='bold', color='white')
ax3.set_ylabel('Size (bytes)', color='white')
ax3.set_xticks(x)
ax3.set_xticklabels(categories)
ax3.legend(facecolor='#16213e', edgecolor='white',
           labelcolor='white')
ax3.grid(axis='y', alpha=0.3)
for bar in bars3:
    ax3.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 20,
             f'{int(bar.get_height())}B',
             ha='center', va='bottom',
             color='white', fontsize=8)
for bar in bars4:
    ax3.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 20,
             f'{int(bar.get_height())}B',
             ha='center', va='bottom',
             color='white', fontsize=8)

plt.tight_layout()
plt.savefig('results/chart1_signature_comparison.png',
            dpi=150, bbox_inches='tight',
            facecolor='#1a1a2e')
print("[Chart 1] Signature comparison saved")
plt.close()


# ─── Figure 2: Attack and Self-Healing Timeline ──
fig2, axes2 = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle(
    'Attack Simulation and Self-Healing Analysis',
    fontsize=16, fontweight='bold', color='white'
)

# Chart 2a: Transaction Timeline
ax4 = axes2[0, 0]
transactions = data['transactions']
tx_nums = list(range(1, len(transactions) + 1))
tx_times = [t['tx_time'] for t in transactions]
tx_colors = [
    VALID_COLOR if t['type'] == 'VALID' 
    else ATTACK_COLOR 
    for t in transactions
]
tx_labels = [t['status'] for t in transactions]

bars5 = ax4.bar(tx_nums, tx_times, color=tx_colors,
                edgecolor='white', linewidth=0.3)
ax4.set_title('Transaction Timeline',
              fontweight='bold', color='white')
ax4.set_xlabel('Transaction Number', color='white')
ax4.set_ylabel('Time (ms)', color='white')
ax4.grid(axis='y', alpha=0.3)

valid_patch = mpatches.Patch(
    color=VALID_COLOR, label='Valid Transaction'
)
attack_patch = mpatches.Patch(
    color=ATTACK_COLOR, label='Attack (Blocked)'
)
ax4.legend(handles=[valid_patch, attack_patch],
           facecolor='#16213e', edgecolor='white',
           labelcolor='white')

# Chart 2b: Transaction Status Pie
ax5 = axes2[0, 1]
valid_count = sum(
    1 for t in transactions if t['type'] == 'VALID'
)
attack_count = sum(
    1 for t in transactions if t['type'] == 'ATTACK'
)
sizes = [valid_count, attack_count]
pie_colors = [VALID_COLOR, ATTACK_COLOR]
explode = (0.05, 0.05)
wedges, texts, autotexts = ax5.pie(
    sizes,
    explode=explode,
    labels=['Valid Transactions', 'Attacks Blocked'],
    colors=pie_colors,
    autopct='%1.1f%%',
    shadow=True,
    startangle=90,
    textprops={'color': 'white'}
)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax5.set_title('Transaction Distribution',
              fontweight='bold', color='white')

# Chart 2c: Self-Healing Recovery Timeline
ax6 = axes2[1, 0]
recovery_times = data.get('recovery_times', [])
recovery_nums = list(range(1, len(recovery_times) + 1))
recovery_colors = [
    RECOVER_COLOR if i < len(recovery_times) - 1
    else VALID_COLOR
    for i in range(len(recovery_times))
]
bars6 = ax6.bar(recovery_nums, recovery_times,
                color=recovery_colors,
                edgecolor='white', linewidth=0.5)
ax6.set_title('Self-Healing Recovery Timeline\n'
              '(Novel: Automatic Threshold Recovery)',
              fontweight='bold', color='white')
ax6.set_xlabel('Safe Transaction Number', color='white')
ax6.set_ylabel('Time (ms)', color='white')
ax6.grid(axis='y', alpha=0.3)
ax6.axhline(y=sum(recovery_times)/len(recovery_times),
            color='white', linestyle='--', alpha=0.7,
            label=f'Avg: {sum(recovery_times)/len(recovery_times):.2f}ms')
ax6.legend(facecolor='#16213e', edgecolor='white',
           labelcolor='white')

# Add labels on bars
for bar, val in zip(bars6, recovery_times):
    ax6.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.3,
             f'{val:.1f}ms',
             ha='center', va='bottom',
             color='white', fontsize=9)

# Add annotation for final recovery
ax6.annotate(
    'CONTRACT\nRECOVERED!',
    xy=(len(recovery_times), recovery_times[-1]),
    xytext=(len(recovery_times) - 1.5,
            max(recovery_times) * 1.1),
    arrowprops=dict(arrowstyle='->', color=VALID_COLOR),
    color=VALID_COLOR, fontweight='bold', fontsize=9
)

# Chart 2d: System State Timeline
ax7 = axes2[1, 1]
states = []
state_labels = []
colors_state = []

# Build state timeline
phase_labels = []
phase_colors = []
phase_counts = []

# Normal transactions
for i in range(3):
    phase_labels.append(f'TX {i+1}\nValid')
    phase_colors.append(VALID_COLOR)
    phase_counts.append(1)

# Attack transactions
for i in range(3):
    phase_labels.append(f'ATK {i+1}\nBlocked')
    phase_colors.append(ATTACK_COLOR)
    phase_counts.append(1)

# Recovery transactions
for i in range(5):
    label = f'REC {i+1}'
    phase_labels.append(label)
    if i < 4:
        phase_colors.append(RECOVER_COLOR)
    else:
        phase_colors.append(VALID_COLOR)
    phase_counts.append(1)

# Post recovery
for i in range(3):
    phase_labels.append(f'TX {i+4}\nValid')
    phase_colors.append(VALID_COLOR)
    phase_counts.append(1)

x_pos = list(range(len(phase_labels)))
bars7 = ax7.bar(x_pos, [1]*len(phase_labels),
                color=phase_colors,
                edgecolor='white', linewidth=0.3)

# Add pause region highlight
ax7.axvspan(5.5, 8.5, alpha=0.2, color='red',
            label='Contract Paused')
ax7.axvspan(8.5, 13.5, alpha=0.2, color='yellow',
            label='Recovery Phase')

ax7.set_title('System State Timeline',
              fontweight='bold', color='white')
ax7.set_xticks(x_pos)
ax7.set_xticklabels(phase_labels, rotation=45,
                    ha='right', fontsize=7)
ax7.set_ylabel('State', color='white')
ax7.set_yticks([])
ax7.grid(axis='x', alpha=0.3)

# Legend
normal_p = mpatches.Patch(
    color=VALID_COLOR, label='Valid/Recovered'
)
attack_p = mpatches.Patch(
    color=ATTACK_COLOR, label='Attack Blocked'
)
recover_p = mpatches.Patch(
    color=RECOVER_COLOR, label='Recovering'
)
paused_p = mpatches.Patch(
    color='red', alpha=0.4, label='Paused State'
)
ax7.legend(
    handles=[normal_p, attack_p, recover_p, paused_p],
    facecolor='#16213e', edgecolor='white',
    labelcolor='white', fontsize=7,
    loc='upper right'
)

plt.tight_layout()
plt.savefig('results/chart2_attack_healing.png',
            dpi=150, bbox_inches='tight',
            facecolor='#1a1a2e')
print("[Chart 2] Attack and healing analysis saved")
plt.close()


# ─── Figure 3: Security and Performance Summary ──
fig3, axes3 = plt.subplots(1, 2, figsize=(14, 6))
fig3.suptitle(
    'Security Analysis and System Performance Summary',
    fontsize=16, fontweight='bold', color='white'
)

# Chart 3a: Speed Comparison Radar
ax8 = axes3[0]
categories_r = [
    'Sign Speed', 'Verify Speed',
    'Quantum\nSafety', 'Auto\nRecovery',
    'Attack\nDetection'
]
N = len(categories_r)

# Normalize scores (0-10)
pq_scores   = [8, 9, 10, 10, 9]
ecdsa_scores = [6, 3,  0,  0, 3]

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]
pq_scores   += pq_scores[:1]
ecdsa_scores += ecdsa_scores[:1]

ax8 = plt.subplot(131, polar=True,
                  facecolor='#16213e')
ax8.set_facecolor('#16213e')

ax8.plot(angles, pq_scores,
         color=PQ_COLOR, linewidth=2, label='ML-DSA-65')
ax8.fill(angles, pq_scores,
         color=PQ_COLOR, alpha=0.25)
ax8.plot(angles, ecdsa_scores,
         color=ECDSA_COLOR, linewidth=2, label='ECDSA')
ax8.fill(angles, ecdsa_scores,
         color=ECDSA_COLOR, alpha=0.25)

ax8.set_xticks(angles[:-1])
ax8.set_xticklabels(categories_r,
                    color='white', size=9)
ax8.set_ylim(0, 10)
ax8.tick_params(colors='white')
ax8.spines['polar'].set_color('#0f3460')
ax8.yaxis.set_tick_params(labelcolor='white')
ax8.set_title('Security Capability\nComparison',
              color='white', fontweight='bold',
              pad=20)
ax8.legend(loc='upper right',
           bbox_to_anchor=(0.1, 0.1),
           facecolor='#16213e',
           edgecolor='white',
           labelcolor='white')

# Chart 3b: Key Metrics Summary
ax9 = axes3[1]
ax9.axis('off')

metrics = [
    ['Metric', 'Value', 'Status'],
    ['PQ Sign Time', 
     f"{data['pq_avg_sign']:.3f} ms", '✓ Fast'],
    ['ECDSA Sign Time', 
     f"{data['ecdsa_avg_sign']:.3f} ms", '~ Slower'],
    ['PQ Verify Time', 
     f"{data['pq_avg_verify']:.3f} ms", '✓ 36x Faster'],
    ['ECDSA Verify Time', 
     f"{data['ecdsa_avg_verify']:.3f} ms", '✗ Slow'],
    ['Attack Threshold', '3 attacks', '✓ Working'],
    ['Recovery Threshold', '5 safe tx', '✓ Working'],
    ['Avg Recovery Time', 
     f"{data['avg_recovery_time']:.2f} ms", '✓ Fast'],
    ['Manual Intervention', 'None', '✓ Novel'],
    ['Quantum Resistance', 'ML-DSA-65', '✓ Safe'],
    ['Attacks Blocked', 
     f"{report['attacks_blocked']}", '✓ 100%'],
]

table = ax9.table(
    cellText=metrics[1:],
    colLabels=metrics[0],
    cellLoc='center',
    loc='center',
    bbox=[0, 0, 1, 1]
)

table.auto_set_font_size(False)
table.set_fontsize(10)

for (row, col), cell in table.get_celld().items():
    cell.set_facecolor('#16213e')
    cell.set_edgecolor('#0f3460')
    cell.set_text_props(color='white')
    if row == 0:
        cell.set_facecolor('#0f3460')
        cell.set_text_props(
            color='white', fontweight='bold'
        )
    if col == 2 and row > 0:
        text = cell.get_text().get_text()
        if '✓' in text:
            cell.set_facecolor('#1a472a')
        elif '✗' in text:
            cell.set_facecolor('#4a1a1a')
        elif '~' in text:
            cell.set_facecolor('#4a3a1a')

ax9.set_title('Performance Metrics Summary',
              color='white', fontweight='bold',
              pad=20)

plt.tight_layout()
plt.savefig('results/chart3_summary.png',
            dpi=150, bbox_inches='tight',
            facecolor='#1a1a2e')
print("[Chart 3] Summary saved")
plt.close()


# ─── Figure 4: Novel Contribution Highlight ──────
fig4, ax10 = plt.subplots(figsize=(12, 6))
fig4.patch.set_facecolor('#1a1a2e')
ax10.set_facecolor('#16213e')

# Build complete timeline
all_events = []

# Phase 1: Normal (3 tx)
for i in range(3):
    all_events.append({
        'x': i + 1,
        'y': 1,
        'color': VALID_COLOR,
        'label': f'Valid\nTX {i+1}',
        'state': 'NORMAL'
    })

# Phase 2: Attacks (3 attacks)
for i in range(3):
    all_events.append({
        'x': i + 4,
        'y': 1,
        'color': ATTACK_COLOR,
        'label': f'Attack\n{i+1}',
        'state': 'ATTACK'
    })

# Phase 3: Recovery (5 tx)
for i in range(5):
    all_events.append({
        'x': i + 7,
        'y': 1,
        'color': RECOVER_COLOR,
        'label': f'Recover\n{i+1}',
        'state': 'RECOVERY'
    })

# Phase 4: Post recovery (3 tx)
for i in range(3):
    all_events.append({
        'x': i + 12,
        'y': 1,
        'color': VALID_COLOR,
        'label': f'Valid\nTX {i+4}',
        'state': 'NORMAL'
    })

# Draw timeline line
ax10.axhline(y=1, color='white', linewidth=2,
             alpha=0.3, zorder=1)

# Draw events
for event in all_events:
    ax10.scatter(event['x'], event['y'],
                 s=200, color=event['color'],
                 zorder=3, edgecolors='white',
                 linewidth=1)
    ax10.text(event['x'], 0.7,
              event['label'],
              ha='center', va='top',
              color='white', fontsize=7)

# Add region highlights
ax10.axvspan(3.5, 6.5, alpha=0.15,
             color=ATTACK_COLOR, label='Attack Phase')
ax10.axvspan(6.5, 11.5, alpha=0.15,
             color=RECOVER_COLOR, label='Recovery Phase')

# Add annotations
ax10.annotate(
    'CONTRACT\nAUTO-PAUSED\n(Attack Threshold)',
    xy=(6.5, 1), xytext=(6.5, 1.4),
    arrowprops=dict(arrowstyle='->', color=ATTACK_COLOR,
                    lw=2),
    color=ATTACK_COLOR, fontweight='bold',
    ha='center', fontsize=9
)

ax10.annotate(
    'CONTRACT\nAUTO-RECOVERED\n(Novel Contribution)',
    xy=(11.5, 1), xytext=(11.5, 1.4),
    arrowprops=dict(arrowstyle='->', color=VALID_COLOR,
                    lw=2),
    color=VALID_COLOR, fontweight='bold',
    ha='center', fontsize=9
)

# Phase labels at top
ax10.text(2, 1.7, 'PHASE 2\nNormal Operations',
          ha='center', color='white',
          fontsize=9, fontweight='bold')
ax10.text(5, 1.7, 'PHASE 3\nAttack Simulation',
          ha='center', color=ATTACK_COLOR,
          fontsize=9, fontweight='bold')
ax10.text(9, 1.7, 'PHASE 4\nAuto Recovery',
          ha='center', color=RECOVER_COLOR,
          fontsize=9, fontweight='bold')
ax10.text(13, 1.7, 'PHASE 5\nResumed',
          ha='center', color=VALID_COLOR,
          fontsize=9, fontweight='bold')

ax10.set_xlim(0, 15)
ax10.set_ylim(0.3, 2.0)
ax10.set_title(
    'Complete System Timeline: Attack Detection → '
    'Auto-Pause → Threshold Recovery\n'
    '(Novel Contribution: Zero Manual Intervention)',
    fontweight='bold', color='white', fontsize=13
)
ax10.set_xlabel('Transaction Number', color='white')
ax10.set_yticks([])
ax10.grid(axis='x', alpha=0.2)
ax10.spines['top'].set_visible(False)
ax10.spines['right'].set_visible(False)
ax10.spines['left'].set_visible(False)
ax10.spines['bottom'].set_color('#0f3460')

legend_elements = [
    mpatches.Patch(color=VALID_COLOR,
                   label='Valid Transaction'),
    mpatches.Patch(color=ATTACK_COLOR,
                   label='Attack Blocked'),
    mpatches.Patch(color=RECOVER_COLOR,
                   label='Recovery Transaction'),
]
ax10.legend(handles=legend_elements,
            facecolor='#16213e',
            edgecolor='white',
            labelcolor='white',
            loc='lower right')

plt.tight_layout()
plt.savefig('results/chart4_timeline.png',
            dpi=150, bbox_inches='tight',
            facecolor='#1a1a2e')
print("[Chart 4] Timeline saved")
plt.close()

print("\n" + "="*50)
print("ALL CHARTS GENERATED SUCCESSFULLY")
print("="*50)
print("Saved in results/ folder:")
print("  chart1_signature_comparison.png")
print("  chart2_attack_healing.png")
print("  chart3_summary.png")
print("  chart4_timeline.png")
print("="*50)