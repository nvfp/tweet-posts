from mykit.kit.text import byteFmt
from mykit.kit.utils import printer


def get_text(
    tweet_id, masto_id,
    newton_power, newton_const,

    n_iter,
    ct,
    hue_offset,
    saturation,

    num_attempts, dur, std, file_size,

    xmin, xmax, ymin, ymax,

    edit_contrast,
    edit_brightness,
    edit_saturation,
    edit_gamma,
    edit_gamma_r,
    edit_gamma_g,
    edit_gamma_b,
    edit_vignette,
    edit_temp,
):
    return f"""tweet_id: {tweet_id}
masto_id: {masto_id}

newton_power: {newton_power}
newton_const: {newton_const}

n_iter: {n_iter}
ct: {ct}
hue_offset: {hue_offset}
saturation: {saturation}

num_attempts: {num_attempts}
dur: {dur}
std: {std}
size: {file_size} ({byteFmt(file_size)})

xmin: {xmin}
xmax: {xmax}
ymin: {ymin}
ymax: {ymax}

contrast: {edit_contrast}
brightness: {edit_brightness}
saturation: {edit_saturation}
gamma: {edit_gamma}
gamma_r: {edit_gamma_r}
gamma_g: {edit_gamma_g}
gamma_b: {edit_gamma_b}
vignette: {edit_vignette}
temp: {edit_temp}"""


def write_metadata(
    file_path, tweet_id, masto_id,
    newton_power, newton_const,

    n_iter,
    ct,
    hue_offset,
    saturation,

    num_attempts, dur, std, file_size,

    xmin, xmax, ymin, ymax,

    edit_contrast,
    edit_brightness,
    edit_saturation,
    edit_gamma,
    edit_gamma_r,
    edit_gamma_g,
    edit_gamma_b,
    edit_vignette,
    edit_temp,
):
    printer('DEBUG: Writing metadata file.')

    text = get_text(
        tweet_id, masto_id,
        newton_power, newton_const,

        n_iter,
        ct,
        hue_offset,
        saturation,

        num_attempts, dur, std, file_size,

        xmin, xmax, ymin, ymax,

        edit_contrast,
        edit_brightness,
        edit_saturation,
        edit_gamma,
        edit_gamma_r,
        edit_gamma_g,
        edit_gamma_b,
        edit_vignette,
        edit_temp,
    )
    with open(file_path, 'w') as f:
        f.write(text)
    
    printer(f'INFO: Done, metadata file created at {repr(file_path)}.')