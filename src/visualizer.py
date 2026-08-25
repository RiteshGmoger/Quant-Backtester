import matplotlib.pyplot as plt;
import numpy as np;
import os;


def save_and_show(save_path, title):
    # results/charts is gitignored, so it won't exist on a fresh clone
    directory = os.path.dirname(save_path);
    if directory:
        os.makedirs(directory, exist_ok = True);

    plt.savefig(save_path, dpi = 150, bbox_inches = 'tight');
    print(f"\nsaved  -> {save_path}");
    print(f"showing [{title}] - close window to continue\n");
    plt.show();
    plt.close();


def plot_equity_curve(equity_curve, save_path = 'results/charts/equity.png'):
    fig, ax = plt.subplots(figsize = (12, 6));

    ax.plot(equity_curve, label = 'Portfolio', color = '#2196F3', linewidth = 2);

    ax.set_title('Equity Curve', fontsize = 14, fontweight = 'bold');
    ax.set_xlabel('Trade Number');
    ax.set_ylabel('Portfolio Value (₹)');
    ax.legend();
    ax.grid(True, alpha = 0.4);

    # annotate start and end value
    start_val = equity_curve[0];
    end_val   = equity_curve[-1];
    change    = ((end_val - start_val) / start_val) * 100;

    ax.annotate(
        f'Start: ₹{start_val:,.0f}',
        xy = (0, start_val),
        xytext = (10, 20),
        textcoords = 'offset points',
        fontsize = 9,
        color = 'gray'
    );
    ax.annotate(
        f'End: ₹{end_val:,.0f}  ({change:+.1f}%)',
        xy = (len(equity_curve) - 1, end_val),
        xytext = (-90, -25),
        textcoords = 'offset points',
        fontsize = 9,
        color = '#2196F3'
    );

    plt.tight_layout();
    save_and_show(save_path, 'Equity Curve');


def plot_drawdown(equity_curve, save_path = 'results/charts/drawdown.png'):
    equity   = np.array(equity_curve);
    peak     = np.maximum.accumulate(equity);
    drawdown = (equity - peak) / peak * 100;

    fig, ax = plt.subplots(figsize = (12, 6));

    ax.fill_between(range(len(drawdown)), drawdown, 0, color = 'red', alpha = 0.25);
    ax.plot(drawdown, color = 'darkred', linewidth = 2);

    # annotate max drawdown
    max_dd_val = drawdown.min();
    max_dd_idx = drawdown.argmin();
    ax.annotate(
        f'Max DD: {max_dd_val:.1f}%',
        xy = (max_dd_idx, max_dd_val),
        xytext = (20, 20),
        textcoords = 'offset points',
        fontsize = 9,
        color = 'darkred',
        arrowprops = dict(arrowstyle = '->', color = 'darkred', lw = 1.2)
    );

    ax.set_title('Drawdown Chart', fontsize = 14, fontweight = 'bold');
    ax.set_xlabel('Trade Number');
    ax.set_ylabel('Drawdown (%)');
    ax.grid(True, alpha = 0.4);

    plt.tight_layout();
    save_and_show(save_path, 'Drawdown Chart');


def plot_returns(returns, save_path = 'results/charts/returns.png'):
    returns = list(returns);
    colors  = ['#4CAF50' if r > 0 else '#F44336' for r in returns];

    fig, ax = plt.subplots(figsize = (12, 6));

    ax.bar(range(len(returns)), returns, color = colors, alpha = 0.75);

    # summary stats on chart
    pos_trades = [r for r in returns if r > 0];
    neg_trades = [r for r in returns if r < 0];
    avg_win    = np.mean(pos_trades) if pos_trades else 0;
    avg_loss   = np.mean(neg_trades) if neg_trades else 0;

    ax.axhline(0,           color = 'black',  linewidth = 1);
    ax.axhline(avg_win,     color = '#4CAF50', linewidth = 1, linestyle = '--', alpha = 0.7, label = f'Avg win  {avg_win:+.2f}%');
    ax.axhline(avg_loss,    color = '#F44336', linewidth = 1, linestyle = '--', alpha = 0.7, label = f'Avg loss {avg_loss:+.2f}%');

    ax.set_title('Trade Returns', fontsize = 14, fontweight = 'bold');
    ax.set_xlabel('Trade Number');
    ax.set_ylabel('Return (%)');
    ax.legend(fontsize = 9);
    ax.grid(True, axis = 'y', alpha = 0.4);

    plt.tight_layout();
    save_and_show(save_path, 'Trade Returns');
