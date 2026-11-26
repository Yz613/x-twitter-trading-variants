"""Registry of all 32 X/Twitter, Ablation, and Shlomo trading variants."""
from .variant_a import CONFIG as _variant_a_cfg
from .variant_b import CONFIG as _variant_b_cfg
from .variant_c import CONFIG as _variant_c_cfg
from .variant_f import CONFIG as _variant_f_cfg
from .variant_g import CONFIG as _variant_g_cfg
from .variant_h import CONFIG as _variant_h_cfg
from .variant_i import CONFIG as _variant_i_cfg
from .variant_j import CONFIG as _variant_j_cfg
from .variant_k import CONFIG as _variant_k_cfg
from .variant_l import CONFIG as _variant_l_cfg
from .variant_m import CONFIG as _variant_m_cfg
from .variant_n import CONFIG as _variant_n_cfg
from .variant_o import CONFIG as _variant_o_cfg
from .variant_p import CONFIG as _variant_p_cfg
from .variant_q import CONFIG as _variant_q_cfg
from .variant_r import CONFIG as _variant_r_cfg
from .variant_s import CONFIG as _variant_s_cfg
from .variant_t import CONFIG as _variant_t_cfg
from .variant_u import CONFIG as _variant_u_cfg
from .variant_v import CONFIG as _variant_v_cfg
from .variant_x import CONFIG as _variant_x_cfg
from .variant_r_mkt import CONFIG as _variant_r_mkt_cfg
from .variant_q_mkt import CONFIG as _variant_q_mkt_cfg
from .variant_k_mkt import CONFIG as _variant_k_mkt_cfg
from .variant_r_tw import CONFIG as _variant_r_tw_cfg
from .variant_q_tw import CONFIG as _variant_q_tw_cfg
from .variant_k_tw import CONFIG as _variant_k_tw_cfg
from .shlomo_30 import CONFIG as _shlomo_30_cfg
from .shlomo_sniper import CONFIG as _shlomo_sniper_cfg
from .shlomo_525 import CONFIG as _shlomo_525_cfg
from .shlomo_550 import CONFIG as _shlomo_550_cfg
from .shlomo_tiered import CONFIG as _shlomo_tiered_cfg

ALL_VARIANTS = {
    "variant_a": _variant_a_cfg,
    "variant_b": _variant_b_cfg,
    "variant_c": _variant_c_cfg,
    "variant_f": _variant_f_cfg,
    "variant_g": _variant_g_cfg,
    "variant_h": _variant_h_cfg,
    "variant_i": _variant_i_cfg,
    "variant_j": _variant_j_cfg,
    "variant_k": _variant_k_cfg,
    "variant_l": _variant_l_cfg,
    "variant_m": _variant_m_cfg,
    "variant_n": _variant_n_cfg,
    "variant_o": _variant_o_cfg,
    "variant_p": _variant_p_cfg,
    "variant_q": _variant_q_cfg,
    "variant_r": _variant_r_cfg,
    "variant_s": _variant_s_cfg,
    "variant_t": _variant_t_cfg,
    "variant_u": _variant_u_cfg,
    "variant_v": _variant_v_cfg,
    "variant_x": _variant_x_cfg,
    "variant_r_mkt": _variant_r_mkt_cfg,
    "variant_q_mkt": _variant_q_mkt_cfg,
    "variant_k_mkt": _variant_k_mkt_cfg,
    "variant_r_tw": _variant_r_tw_cfg,
    "variant_q_tw": _variant_q_tw_cfg,
    "variant_k_tw": _variant_k_tw_cfg,
    "shlomo_30": _shlomo_30_cfg,
    "shlomo_sniper": _shlomo_sniper_cfg,
    "shlomo_525": _shlomo_525_cfg,
    "shlomo_550": _shlomo_550_cfg,
    "shlomo_tiered": _shlomo_tiered_cfg,
}
